"""Tests for Gemini-driven Future Reputation Deterioration Assessment."""
from datetime import datetime, timezone
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.mock_gemini import MockGeminiClient
from app.models.business import Business
from app.models.mention import Mention, SentimentAnalysis
from app.services.deterioration_service import DeteriorationService


@pytest.mark.asyncio
async def test_mock_gemini_assessment_direct():
    """Test MockGeminiClient assess_reputation_deterioration directly."""
    mock = MockGeminiClient()
    sample_reviews = [
        {"content": "Terrible food, rude waiter rolled his eyes at us.", "rating": 1.0, "platform": "google"},
        {"content": "Worst experience ever. Waited 45 mins and cold food.", "rating": 1.0, "platform": "reddit"},
        {"content": "Horrible attitude from staff.", "rating": 2.0, "platform": "twitter"},
    ]
    resp = await mock.assess_reputation_deterioration(
        business_name="Spice Symphony",
        business_category="Restaurant",
        review_summary="3 recent negative mentions",
        recent_reviews=sample_reviews,
        horizon_days=14,
    )

    assert 0.0 <= resp.deterioration_probability <= 1.0
    assert resp.risk_level in ["HIGH", "CRITICAL"]
    assert resp.is_sustained_decline is True
    assert len(resp.key_drivers) > 0
    assert len(resp.recommended_actions) > 0
    assert "Spice Symphony" in resp.expert_opinion


@pytest.mark.asyncio
async def test_blip_vs_sustained_decline():
    """Test that Gemini distinguishes between an isolated blip and a sustained decline."""
    mock = MockGeminiClient()

    # Scenario A: Temporary blip (mostly happy customers, 1 noisy complaint)
    mostly_positive = [
        {"content": "Amazing curry, great service!", "rating": 5.0, "platform": "google"},
        {"content": "Loved the biryani, our favorite spot.", "rating": 5.0, "platform": "google"},
        {"content": "Delicious naan and cocktails.", "rating": 5.0, "platform": "reddit"},
        {"content": "Super friendly staff.", "rating": 5.0, "platform": "google"},
        {"content": "The soup was slightly salty today.", "rating": 3.0, "platform": "google"},
    ]
    blip_resp = await mock.assess_reputation_deterioration(
        business_name="Spice Symphony",
        business_category="Restaurant",
        review_summary="Mostly positive",
        recent_reviews=mostly_positive,
        horizon_days=14,
    )
    assert blip_resp.is_sustained_decline is False
    assert blip_resp.deterioration_probability < 0.35
    assert blip_resp.risk_level in ["LOW", "MODERATE"]

    # Scenario B: Sustained decline (run of bad reviews converging on service)
    mostly_negative = [
        {"content": "Rude manager, horrible service.", "rating": 1.0, "platform": "google"},
        {"content": "Avoid this place, worst food ever.", "rating": 1.0, "platform": "reddit"},
        {"content": "Terrible wait times and cold dishes.", "rating": 1.0, "platform": "twitter"},
        {"content": "Dirty tables and unhelpful staff.", "rating": 1.0, "platform": "google"},
        {"content": "Horrible experience last night.", "rating": 1.0, "platform": "google"},
    ]
    sustained_resp = await mock.assess_reputation_deterioration(
        business_name="Spice Symphony",
        business_category="Restaurant",
        review_summary="Multiple bad reviews",
        recent_reviews=mostly_negative,
        horizon_days=14,
    )
    assert sustained_resp.is_sustained_decline is True
    assert sustained_resp.deterioration_probability >= 0.60
    assert sustained_resp.risk_level in ["HIGH", "CRITICAL"]


@pytest.mark.asyncio
async def test_deterioration_service_with_database(db_session: AsyncSession):
    """Test DeteriorationService querying mentions and producing DeteriorationAssessment."""
    # Create business
    biz = Business(name="Bistro Paris", category="Cafe")
    db_session.add(biz)
    await db_session.flush()

    # Create mentions with valid non-null fields
    now = datetime.now(timezone.utc)
    for i in range(5):
        m = Mention(
            business_id=biz.id,
            platform="google",
            external_id=f"ext_mention_{i}",
            content_hash=f"hash_mention_{i}",
            author=f"Customer_{i}",
            content="Rude waiter, terrible service!",
            rating=1.0,
            published_at=now,
        )
        db_session.add(m)
        await db_session.flush()
        s = SentimentAnalysis(mention_id=m.id, sentiment_label="negative", compound_score=-0.8)
        db_session.add(s)

    await db_session.commit()

    assessment = await DeteriorationService.get_deterioration_assessment(
        session=db_session,
        business_id=str(biz.id),
        horizon_days=14,
    )

    assert assessment.business_id == str(biz.id)
    assert assessment.business_name == "Bistro Paris"
    assert assessment.deterioration_probability > 0.50
    assert assessment.is_sustained_decline is True
    assert len(assessment.key_drivers) > 0


@pytest.mark.asyncio
async def test_deterioration_api_endpoints(client):
    """Test GET /api/reputation/deterioration-prediction and REST parity."""
    # Flutter endpoint
    resp = await client.get("/api/reputation/deterioration-prediction")
    assert resp.status_code == 200
    data = resp.json()
    assert "deterioration_probability" in data
    assert "risk_level" in data
    assert "is_sustained_decline" in data
    assert "expert_opinion" in data
    assert "recommended_actions" in data

    # REST v1 endpoint
    resp_v1 = await client.get("/api/v1/reputation/deterioration-prediction")
    assert resp_v1.status_code == 200
    assert resp_v1.json()["deterioration_probability"] == data["deterioration_probability"]


@pytest.mark.asyncio
async def test_dashboard_includes_deterioration(client):
    """Test that GET /api/dashboard includes the deterioration assessment."""
    resp = await client.get("/api/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert "deterioration_assessment" in data
    if data["deterioration_assessment"]:
        assert "deterioration_probability" in data["deterioration_assessment"]
        assert "is_sustained_decline" in data["deterioration_assessment"]
