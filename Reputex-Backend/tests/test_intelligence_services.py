"""Tests for IssueDetectionService, ReviewAuthenticityService, CrisisService, and ReputationService."""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.mention import Mention
from app.models.user import User
from app.services.authenticity_service import ReviewAuthenticityService
from app.services.crisis_service import CrisisService
from app.services.issue_detection_service import IssueDetectionService
from app.services.reputation_service import ReputationService


@pytest.mark.asyncio
async def test_issue_detection_service(db_session: AsyncSession):
    # Setup test user and business
    user = User(
        id="usr_owner_1",
        email="owner1@test.com",
        password_hash="fakehash",
        full_name="Owner One",
    )
    db_session.add(user)
    await db_session.flush()

    biz = Business(
        id="biz_test_issues",
        name="Test Cafe",
        category="Restaurant",
        owner_id=user.id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(biz)
    await db_session.flush()

    # Create mentions representing customer service wait times and food quality issues
    now = datetime.now(UTC)
    mentions = [
        Mention(
            business_id=biz.id,
            platform="Google",
            external_id="m_g1",
            author="User A",
            content="We waited forever for our table, slow service and cold food.",
            rating=1.0,
            sentiment="negative",
            sentiment_score=-0.85,
            published_at=now - timedelta(hours=2),
            created_at=now,
        ),
        Mention(
            business_id=biz.id,
            platform="Reddit",
            external_id="m_r1",
            author="User B",
            content="Slow service and terrible line. Waited 45 minutes for drinks.",
            rating=2.0,
            sentiment="negative",
            sentiment_score=-0.7,
            published_at=now - timedelta(hours=4),
            created_at=now,
        ),
        Mention(
            business_id=biz.id,
            platform="Twitter",
            external_id="m_t1",
            author="User C",
            content="@TestCafe table not ready and long wait times! Disappointing delay.",
            rating=None,
            sentiment="negative",
            sentiment_score=-0.6,
            published_at=now - timedelta(hours=6),
            created_at=now,
        ),
        Mention(
            business_id=biz.id,
            platform="Google",
            external_id="m_g2",
            author="User D",
            content="Great ambiance and delicious coffee, highly enjoy this place!",
            rating=5.0,
            sentiment="positive",
            sentiment_score=0.9,
            published_at=now - timedelta(hours=1),
            created_at=now,
        ),
    ]
    for m in mentions:
        db_session.add(m)
    await db_session.commit()

    service = IssueDetectionService(db_session)
    issues = await service.detect_and_persist_issues(biz.id)

    assert len(issues) >= 1
    wait_issue = next((i for i in issues if "Wait" in i.subtopic or "Customer Service" in i.category), None)
    assert wait_issue is not None
    assert wait_issue.mention_count >= 2
    # Verify cross-platform breakdown
    assert "Google" in wait_issue.platforms_breakdown or "Reddit" in wait_issue.platforms_breakdown
    assert len(wait_issue.evidence) >= 2
    assert wait_issue.evidence[0].excerpt is not None


@pytest.mark.asyncio
async def test_review_authenticity_and_cluster_detection(db_session: AsyncSession):
    user = User(
        id="usr_owner_2",
        email="owner2@test.com",
        password_hash="fakehash",
        full_name="Owner Two",
    )
    db_session.add(user)
    await db_session.flush()

    biz = Business(
        id="biz_test_auth",
        name="Artisan Burgers",
        category="Restaurant",
        owner_id=user.id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(biz)
    await db_session.flush()

    now = datetime.now(UTC)
    # 3 reviews with identical template posted within 15 minutes (coordinated cluster)
    template = "Best place in the world! Ten stars if i could, absolute perfection must visit for everyone!"
    cluster_mentions = [
        Mention(
            business_id=biz.id,
            platform="Google",
            external_id=f"auth_g_{i}",
            author=f"PromoBot_{i}",
            content=template,
            rating=5.0,
            sentiment="positive",
            sentiment_score=0.95,
            published_at=now - timedelta(minutes=5 * i),
            created_at=now,
        )
        for i in range(3)
    ]
    for m in cluster_mentions:
        db_session.add(m)
    await db_session.commit()

    auth_service = ReviewAuthenticityService(db_session)
    findings = await auth_service.analyze_business_authenticity(biz.id)

    assert len(findings) >= 1
    # Check individual reviews flagged with safe terminology
    review_findings = [f for f in findings if f.finding_type == "review_authenticity"]
    assert len(review_findings) == 3
    assert any(
        f.metadata_json.get("label") in ["Likely Suspicious", "High Suspicion", "Potentially Suspicious"]
        for f in review_findings
    )
    # Check coordinated cluster detected
    cluster_findings = [f for f in findings if f.finding_type == "manipulation_cluster"]
    assert len(cluster_findings) == 1
    assert cluster_findings[0].metadata_json["cluster_size"] == 3
    assert len(cluster_findings[0].evidence) == 3


@pytest.mark.asyncio
async def test_crisis_evaluation_and_reputation_scoring(db_session: AsyncSession):
    user = User(
        id="usr_owner_3",
        email="owner3@test.com",
        password_hash="fakehash",
        full_name="Owner Three",
    )
    db_session.add(user)
    await db_session.flush()

    biz = Business(
        id="biz_test_crisis_rep",
        name="Seafood Bistro",
        category="Restaurant",
        owner_id=user.id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    db_session.add(biz)
    await db_session.flush()

    now = datetime.now(UTC)
    # Surge of 5 negative mentions citing food poisoning and sickness
    mentions = [
        Mention(
            business_id=biz.id,
            platform="Google",
            external_id=f"cr_m_{i}",
            author=f"Diner_{i}",
            content="Got severely sick after eating here! Filthy restroom and food poisoning!",
            rating=1.0,
            sentiment="negative",
            sentiment_score=-0.9,
            published_at=now - timedelta(hours=i),
            created_at=now,
        )
        for i in range(5)
    ]
    for m in mentions:
        db_session.add(m)
    await db_session.commit()

    # Test Crisis Service
    crisis_service = CrisisService(db_session)
    res = await crisis_service.evaluate_crisis_for_business(biz.id)

    assert res["warning_level"] in ["High Risk", "Crisis Active"]
    assert res["negative_count"] == 5
    assert any("Health" in d or "Hygiene" in d for d in res["drivers"])

    # Test Reputation Service
    rep_service = ReputationService(db_session)
    score_res = await rep_service.compute_score_for_business(biz.id)

    assert score_res["score"] < 60.0  # Penalized by negative sentiment, ratings, and crisis penalty
    assert score_res["components"]["crisis_penalty"] > 0
