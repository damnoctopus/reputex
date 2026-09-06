"""Tests for batched intelligence and sentiment processing."""
from datetime import datetime, timezone
import pytest
from app.acquisition.base import RawMentionRecord
from app.services.intelligence_service import IntelligenceService
from app.services.mention_service import MentionService


@pytest.mark.asyncio
async def test_intelligence_batch_processing(db_session, test_business):
    records = [
        RawMentionRecord(
            platform="google",
            external_id="intel_1",
            content="Super delicious meal at Spice Symphony!",
            rating=5.0,
            published_at=datetime.now(timezone.utc),
        ),
        RawMentionRecord(
            platform="google",
            external_id="intel_2",
            content="Rude waiter and terrible slow service!",
            rating=1.0,
            published_at=datetime.now(timezone.utc),
        ),
    ]
    await MentionService.upsert_raw_mentions(db_session, test_business.id, records)

    processed = await IntelligenceService.analyze_pending_mentions(db_session, test_business.id)
    assert processed == 2

    # Check updated mentions
    res = await MentionService.get_paginated(db_session, test_business.id)
    m1 = next(m for m in res.items if m.id)
    assert m1.sentiment in ["positive", "negative", "neutral"]
