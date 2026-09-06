"""Unit tests for MentionNormalizer pipeline."""

from datetime import UTC, datetime

import pytest

from app.schemas.ingestion import RawMentionRecord
from app.services.normalizer import MentionNormalizer, NormalizationError


def test_platform_name_normalization():
    """Verify platform alias mapping to standard casing."""
    assert MentionNormalizer.normalize_platform_name("google_places") == "Google"
    assert MentionNormalizer.normalize_platform_name("GOOGLE MAPS") == "Google"
    assert MentionNormalizer.normalize_platform_name("twitter") == "X"
    assert MentionNormalizer.normalize_platform_name("x") == "X"
    assert MentionNormalizer.normalize_platform_name("reddit") == "Reddit"
    assert MentionNormalizer.normalize_platform_name("google ai overview") == "Google AI Overview"
    assert MentionNormalizer.normalize_platform_name("custom_source") == "Custom_source"


def test_content_normalization_and_hash():
    """Verify whitespace collapsing, control character removal, and SHA-256 hash generation."""
    dirty_text = "  Great   food! \r\n\r\n\r\n\r\n Loved the \t paneer \x00 tikka!  "
    cleaned = MentionNormalizer.normalize_content(dirty_text)
    assert cleaned == "Great food!\n\nLoved the paneer tikka!"

    hash_1 = MentionNormalizer.compute_content_hash(cleaned)
    hash_2 = MentionNormalizer.compute_content_hash(cleaned)
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # SHA-256 hex string

    with pytest.raises(NormalizationError):
        MentionNormalizer.normalize_content("   \n\t  ")


def test_rating_normalization_and_clamp():
    """Verify rating values are clamped within 1.0 and 5.0 range."""
    assert MentionNormalizer.normalize_rating(4.5) == 4.5
    assert MentionNormalizer.normalize_rating(7.5) == 5.0
    assert MentionNormalizer.normalize_rating(0.2) == 1.0
    assert MentionNormalizer.normalize_rating("4.8") == 4.8
    assert MentionNormalizer.normalize_rating("invalid") is None
    assert MentionNormalizer.normalize_rating(None) is None


def test_url_normalization():
    """Verify URL validation strips and rejects non-HTTP schemes."""
    assert MentionNormalizer.normalize_url("  https://google.com/review/123  ") == "https://google.com/review/123"
    assert MentionNormalizer.normalize_url("http://reddit.com/post") == "http://reddit.com/post"
    assert MentionNormalizer.normalize_url("javascript:alert(1)") is None
    assert MentionNormalizer.normalize_url("ftp://server/file") is None
    assert MentionNormalizer.normalize_url(None) is None


def test_engagement_normalization():
    """Verify engagement metrics parsing, integer conversion, and alias fallback."""
    raw = {"upvotes": 45, "retweets": "12", "replies": 3}
    eng = MentionNormalizer.normalize_engagement(raw)
    assert eng == {"likes": 45, "shares": 12, "comments": 3}

    bad_raw = {"likes": "not_a_number", "shares": -5}
    bad_eng = MentionNormalizer.normalize_engagement(bad_raw)
    assert bad_eng == {"likes": 0, "shares": 0, "comments": 0}


def test_timestamp_utc_normalization():
    """Verify naive and aware datetimes are converted to UTC."""
    naive = datetime(2026, 9, 1, 10, 0, 0)
    utc_dt = MentionNormalizer.normalize_timestamp(naive)
    assert utc_dt.tzinfo == UTC
    assert utc_dt.hour == 10

    none_dt = MentionNormalizer.normalize_timestamp(None)
    assert none_dt.tzinfo == UTC


def test_fallback_external_id_generation():
    """Verify deterministic fallback ID when external_id is missing."""
    raw = RawMentionRecord(
        platform="Reddit",
        external_id=None,
        content="Testing fallback external ID generation.",
        author="u/tester",
    )
    normalized = MentionNormalizer.normalize_record(raw, business_id="biz_123")
    assert normalized.external_id.startswith("reddit_")
    assert len(normalized.external_id) > 10
    assert normalized.business_id == "biz_123"


def test_batch_normalization_fault_tolerance():
    """Verify individual malformed record does not crash the entire batch."""
    records = [
        RawMentionRecord(
            platform="Google",
            external_id="goog_valid_1",
            content="Delicious food and prompt service!",
            author="Customer A",
            rating=5.0,
        ),
        RawMentionRecord(
            platform="X",
            external_id="tw_invalid_empty",
            content="   \t   ",  # Invalid empty content
            author="Customer B",
        ),
        RawMentionRecord(
            platform="Reddit",
            external_id="red_valid_2",
            content="Decent ambiance and clean tables.",
            author="Customer C",
            rating=4.0,
        ),
    ]

    normalized, errors = MentionNormalizer.normalize_batch(records, business_id="biz_123")
    assert len(normalized) == 2
    assert len(errors) == 1
    assert "tw_invalid_empty" in errors[0]
    assert normalized[0].external_id == "goog_valid_1"
    assert normalized[1].external_id == "red_valid_2"
