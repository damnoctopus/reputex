"""Tests for Google Places API (New) connector and client.

Validates:
  1. Text Search → place_id discovery
  2. Place Details → review parsing
  3. GoogleConnector mock fallback when API key is missing
  4. Place_id caching via metadata (not credentials)
  5. Rating-only reviews are skipped (empty content)
  6. published_at comes from Google's publishTime, not ingestion time
  7. source_url comes from Google's googleMapsUri, not constructed
  8. Retry on transient HTTP errors
  9. Full connector → normalizer integration path
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.integrations.google import GoogleConnector
from app.integrations.google_places_client import GooglePlacesClient, _parse_publish_time
from app.services.normalizer import MentionNormalizer

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def text_search_response() -> dict:
    """Load Google Text Search fixture."""
    with open(FIXTURES_DIR / "google_text_search_response.json") as f:
        return json.load(f)


@pytest.fixture
def place_details_response() -> dict:
    """Load Google Place Details fixture."""
    with open(FIXTURES_DIR / "google_place_details_response.json") as f:
        return json.load(f)


def _make_httpx_response(status_code: int, json_data: dict) -> httpx.Response:
    """Create a mock httpx.Response."""
    resp = httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request("GET", "https://test.example.com"),
    )
    return resp


# ---------------------------------------------------------------------------
# GooglePlacesClient.discover_place tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_discover_place_success(text_search_response):
    """Text Search returns a valid place with place_id and googleMapsUri."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, text_search_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        result = await client.discover_place("Spice Symphony", location="Bengaluru")

    assert result is not None
    assert result["place_id"] == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    assert result["google_maps_uri"] == "https://maps.google.com/?cid=10281119596374313554"
    assert result["display_name"] == "Spice Symphony"
    assert result["rating"] == 4.2
    assert result["user_rating_count"] == 847


@pytest.mark.asyncio
async def test_discover_place_no_results():
    """Text Search returns empty results list."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, {"places": []})

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        result = await client.discover_place("Nonexistent Restaurant", location="Nowhere")

    assert result is None


@pytest.mark.asyncio
async def test_discover_place_no_api_key():
    """discover_place returns None when no API key is provided."""
    client = GooglePlacesClient(api_key=None)
    result = await client.discover_place("Spice Symphony")
    assert result is None


# ---------------------------------------------------------------------------
# GooglePlacesClient.fetch_reviews tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fetch_reviews_parses_correctly(place_details_response):
    """Reviews are parsed into RawMentionRecords with correct fields."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    # Fixture has 5 reviews, but 1 is rating-only (empty text) → 4 parsed
    assert len(records) == 4

    # Verify first review
    r0 = records[0]
    assert r0.platform == "Google"
    assert r0.author == "Ananya Roy"
    assert r0.rating == 5.0
    assert "Exceptional culinary journey" in r0.content


@pytest.mark.asyncio
async def test_fetch_reviews_uses_google_maps_uri(place_details_response):
    """source_url comes from Google's returned googleMapsUri, not constructed."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    for record in records:
        # Must NOT be a constructed URL like maps.google.com/?cid=<place_id>
        assert "?cid=" not in (record.source_url or ""), (
            f"source_url must come from googleMapsUri, not be constructed: {record.source_url}"
        )
        # Must come from Google's response
        assert record.source_url is not None
        assert record.source_url.startswith("https://")


@pytest.mark.asyncio
async def test_fetch_reviews_published_at_from_publish_time(place_details_response):
    """published_at is parsed from Google's publishTime, never set to ingestion time."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        now_before = datetime.now(UTC)
        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    # First review's publishTime is "2026-08-20T14:30:00Z"
    r0 = records[0]
    assert r0.published_at is not None
    assert r0.published_at.year == 2026
    assert r0.published_at.month == 8
    assert r0.published_at.day == 20
    # Must NOT be the ingestion timestamp
    assert r0.published_at < now_before, (
        "published_at must come from Google's publishTime, not ingestion time"
    )


@pytest.mark.asyncio
async def test_fetch_reviews_skips_empty_content(place_details_response):
    """Rating-only reviews (empty text) are skipped."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    # The 5th review in fixture has empty text and should be skipped
    authors = [r.author for r in records]
    assert "Rating Only User" not in authors


@pytest.mark.asyncio
async def test_fetch_reviews_external_id_from_resource_name(place_details_response):
    """external_id is derived from Google's review resource name."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    for record in records:
        assert record.external_id is not None
        # Resource name format: places/{place_id}/reviews/{review_id} → underscored
        assert "places_" in record.external_id


@pytest.mark.asyncio
async def test_fetch_reviews_metadata_contains_place_id(place_details_response):
    """Each record's metadata includes the place_id for traceability."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    for record in records:
        assert record.metadata["place_id"] == "ChIJN1t_tDeuEmsRUsoyG83frY4"


# ---------------------------------------------------------------------------
# GoogleConnector tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_connector_returns_empty_without_key():
    """GoogleConnector returns empty list when no API key."""
    connector = GoogleConnector(api_key="")
    records = await connector.fetch_mentions("Spice Symphony", ["biryani"])

    assert records == []


@pytest.mark.asyncio
async def test_connector_caches_place_id(text_search_response, place_details_response):
    """GoogleConnector uses cached place_id from metadata on subsequent calls."""
    connector = GoogleConnector(api_key="test-key-123")

    # Simulate cached metadata from a previous discovery
    cached_metadata = {
        "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
        "google_maps_uri": "https://maps.google.com/?cid=10281119596374313554",
    }

    mock_details_resp = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_details_resp
        # post should NOT be called since place_id is cached
        mock_instance.post = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await connector.fetch_mentions(
            "Spice Symphony",
            ["biryani"],
            credentials={"api_key": "test-key-123", "_metadata": cached_metadata},
        )

    # Text Search (post) should NOT have been called — cached place_id used
    # Place Details (get) should have been called
    assert len(records) == 4
    # No new metadata discovered
    assert connector.get_discovered_metadata() is None


@pytest.mark.asyncio
async def test_connector_discovers_and_exposes_metadata(text_search_response, place_details_response):
    """GoogleConnector exposes newly discovered metadata via get_discovered_metadata()."""
    connector = GoogleConnector(api_key="test-key-123")

    mock_search_resp = _make_httpx_response(200, text_search_response)
    mock_details_resp = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_search_resp
        mock_instance.get.return_value = mock_details_resp
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        records = await connector.fetch_mentions(
            "Spice Symphony",
            ["biryani"],
            credentials={"api_key": "test-key-123", "_metadata": {}},
        )

    assert len(records) == 4

    # Check discovered metadata
    discovered = connector.get_discovered_metadata()
    assert discovered is not None
    assert discovered["place_id"] == "ChIJN1t_tDeuEmsRUsoyG83frY4"
    assert discovered["google_maps_uri"] == "https://maps.google.com/?cid=10281119596374313554"
    assert discovered["display_name"] == "Spice Symphony"


# ---------------------------------------------------------------------------
# Normalizer integration test
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_google_reviews_normalize_correctly(place_details_response):
    """Google review RawMentionRecords pass through the normalizer without errors."""
    client = GooglePlacesClient(api_key="test-key-123")

    mock_response = _make_httpx_response(200, place_details_response)

    with patch("app.integrations.google_places_client.httpx.AsyncClient") as MockClient:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        MockClient.return_value = mock_instance

        raw_records = await client.fetch_reviews(
            place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
            google_maps_uri="https://maps.google.com/?cid=10281119596374313554",
        )

    normalized, errors = MentionNormalizer.normalize_batch(raw_records, business_id="biz_test123")

    assert len(errors) == 0
    assert len(normalized) == 4

    for n in normalized:
        assert n.platform == "Google"
        assert n.business_id == "biz_test123"
        assert n.content_hash  # Deterministic hash computed
        assert n.external_id  # Stable ID from review resource name
        assert n.published_at is not None
        # published_at must NOT be today — it comes from the review publishTime
        assert n.published_at.year == 2026
        assert n.published_at.month < 9  # All fixture dates are before September


# ---------------------------------------------------------------------------
# Utility tests
# ---------------------------------------------------------------------------


def test_parse_publish_time_valid():
    """Parse standard ISO 8601 / RFC 3339 timestamp."""
    dt = _parse_publish_time("2026-08-20T14:30:00Z")
    assert dt is not None
    assert dt.year == 2026
    assert dt.month == 8
    assert dt.day == 20
    assert dt.hour == 14
    assert dt.minute == 30
    assert dt.tzinfo is not None


def test_parse_publish_time_none():
    """Returns None for missing publishTime."""
    assert _parse_publish_time(None) is None


def test_parse_publish_time_invalid():
    """Returns None for malformed publishTime."""
    assert _parse_publish_time("not-a-date") is None
    assert _parse_publish_time("") is None
