"""Tests for deterministic crisis math and reputation score calculation."""
from datetime import datetime, timedelta, timezone
import pytest
from app.acquisition.base import RawMentionRecord
from app.models.business import Business
from app.services.crisis_service import CrisisService
from app.services.intelligence_service import IntelligenceService
from app.services.issue_detection_service import IssueDetectionService
from app.services.mention_service import MentionService
from app.services.reputation_service import ReputationService
from app.services.time_series_service import TimeSeriesService


@pytest.mark.asyncio
async def test_deterministic_crisis_and_reputation(db_session):
    # Create isolated business for clean crisis test
    biz = Business(
        name="Crisis Diner",
        category="Restaurant",
        monitored_platforms=["twitter", "reddit"],
    )
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    now = datetime.now(timezone.utc)
    # 10 recent negative crisis mentions alleging poisoning on Twitter and Reddit
    records = [
        RawMentionRecord(
            platform="twitter" if i % 2 == 0 else "reddit",
            external_id=f"crisis_test_{i}",
            content="Severe food poisoning after eating here. Hospitalized! Contamination emergency!",
            rating=1.0,
            published_at=now - timedelta(hours=i * 2),
            engagement={"retweets": 20, "likes": 50},
        )
        for i in range(10)
    ]
    await MentionService.upsert_raw_mentions(db_session, biz.id, records)
    await IntelligenceService.analyze_pending_mentions(db_session, biz.id)
    await IssueDetectionService.cluster_and_aggregate_issues(db_session, biz.id)

    metrics = await TimeSeriesService.compute_metrics_for_crisis(db_session, biz.id)
    assert metrics["negative_ratio"] > 0.5
    assert metrics["complaint_velocity"] > 0.0

    # Crisis evaluation
    event = await CrisisService.evaluate_crisis(db_session, biz.id)
    assert event is not None
    assert event.severity in ["high", "critical"]

    # Reputation score calculation
    score = await ReputationService.compute_reputation_score(db_session, biz.id)
    assert score.current_score < 75.0
    assert score.trend == "declining"
