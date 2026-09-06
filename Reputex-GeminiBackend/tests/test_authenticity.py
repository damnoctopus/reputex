"""Tests for review authenticity scoring and manipulation cluster detection."""
from datetime import datetime, timedelta, timezone
import pytest
from app.acquisition.base import RawMentionRecord
from app.services.authenticity_service import ReviewAuthenticityService
from app.services.intelligence_service import IntelligenceService
from app.services.mention_service import MentionService


@pytest.mark.asyncio
async def test_manipulation_cluster_detection(db_session, test_business):
    now = datetime.now(timezone.utc)
    # 5 promotional reviews from different reviewer accounts within 20 minutes
    records = [
        RawMentionRecord(
            platform="google",
            external_id=f"burst_{i}",
            author=f"Promo_User_{i}",
            content="Best place in town! Highly recommended to all. 5 stars! Simply the best.",
            rating=5.0,
            published_at=now - timedelta(minutes=i * 4),
        )
        for i in range(5)
    ]
    await MentionService.upsert_raw_mentions(db_session, test_business.id, records)
    await IntelligenceService.analyze_pending_mentions(db_session, test_business.id)

    await ReviewAuthenticityService.evaluate_authenticity(db_session, test_business.id)

    fraud_reviews = await ReviewAuthenticityService.get_fraud_reviews(db_session, test_business.id)
    assert len(fraud_reviews) >= 3
    # Check safe terminology
    assert any(f.risk_level in ["High Suspicion", "Likely Suspicious", "Potentially Suspicious"] for f in fraud_reviews)
