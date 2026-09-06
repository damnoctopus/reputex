"""Tests for acquisition, normalizer, and deduplication."""
from datetime import datetime, timezone
import pytest
from app.acquisition.base import RawMentionRecord
from app.acquisition.mock_provider import MockAcquisitionProvider
from app.acquisition.normalizer import Normalizer
from app.services.mention_service import MentionService


def test_normalizer_platform_and_hash():
    p1 = Normalizer.infer_platform_from_url("https://www.reddit.com/r/food/comments/123")
    assert p1 == "reddit"

    p2 = Normalizer.infer_platform_from_url("https://x.com/user/status/456")
    assert p2 == "twitter"

    p3 = Normalizer.infer_platform_from_url("https://maps.google.com/?cid=789")
    assert p3 == "google"

    hash1 = Normalizer.compute_content_hash("google", "John Doe", "Great food and quick service!")
    hash2 = Normalizer.compute_content_hash("google", "John Doe", "Great  food and   quick service!  ")
    assert hash1 == hash2


def test_mock_acquisition_75_mentions():
    provider = MockAcquisitionProvider()
    records = provider.acquire("Spice Symphony")
    assert len(records) == 75

    platforms = {r.platform for r in records}
    assert "google" in platforms
    assert "reddit" in platforms
    assert "twitter" in platforms


@pytest.mark.asyncio
async def test_atomic_deduplication(db_session, test_business):
    records = [
        RawMentionRecord(
            platform="google",
            external_id="ext_test_1",
            content="First time review for Spice Symphony.",
            author="UserA",
            published_at=datetime.now(timezone.utc),
        ),
        RawMentionRecord(
            platform="google",
            external_id="ext_test_2",
            content="Second review for Spice Symphony.",
            author="UserB",
            published_at=datetime.now(timezone.utc),
        ),
    ]

    # First ingestion
    found, added = await MentionService.upsert_raw_mentions(db_session, test_business.id, records)
    assert found == 2
    assert added == 2

    # Repeated ingestion of same records
    found_2, added_2 = await MentionService.upsert_raw_mentions(db_session, test_business.id, records)
    assert found_2 == 2
    assert added_2 == 0  # Deduplicated!
