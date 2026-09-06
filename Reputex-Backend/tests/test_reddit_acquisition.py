"""Tests for Reddit acquisition via Firecrawl and RedditConnector."""

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from app.integrations.firecrawl_client import FirecrawlClient
from app.integrations.query_builder import PlatformQueryBuilder
from app.integrations.reddit import RedditConnector
from app.integrations.reddit_firecrawl_provider import RedditFirecrawlProvider
from app.schemas.ingestion import PlatformQuery
from app.services.normalizer import MentionNormalizer

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def reddit_fixture():
    with open(FIXTURES_DIR / "firecrawl_reddit_search_response.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_reddit_firecrawl_parses_submissions_and_comments(reddit_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = RedditFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = reddit_fixture["data"]
        query = PlatformQuery(
            platform="Reddit",
            query_string="Spice Symphony",
            keywords_used=["Spice Symphony"],
        )
        records = await provider.search_mentions(query, limit=5)

    assert len(records) == 3

    # Submission 1
    sub1 = records[0]
    assert sub1.platform == "Reddit"
    assert sub1.external_id == "reddit_t3_18xyzab"
    assert sub1.author == "bangalore_foodie"
    assert "Spice Symphony" in sub1.content
    assert sub1.published_at == datetime(2026, 8, 15, 18, 45, 0, tzinfo=UTC)
    assert sub1.engagement["likes"] == 42
    assert sub1.engagement["comments"] == 18
    assert sub1.metadata["subreddit"] == "bangalore"
    assert sub1.metadata["is_comment"] is False

    # Comment 2
    comment2 = records[1]
    assert comment2.external_id == "reddit_c_k9z1234"
    assert comment2.author == "curry_connoisseur"
    assert comment2.published_at == datetime(2026, 8, 16, 10, 15, 30, tzinfo=UTC)
    assert comment2.metadata["is_comment"] is True


@pytest.mark.asyncio
async def test_reddit_published_at_is_source_time_not_ingestion_time(reddit_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = RedditFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = [reddit_fixture["data"][0]]
        query = PlatformQuery(platform="Reddit", query_string="Spice Symphony", keywords_used=["Spice Symphony"])
        records = await provider.search_mentions(query)

    rec = records[0]
    # Invariant: Must not equal current time
    now_utc = datetime.now(UTC)
    assert rec.published_at is not None
    assert (now_utc - rec.published_at).total_seconds() > 3600  # published in past
    assert rec.published_at.year == 2026
    assert rec.published_at.month == 8


@pytest.mark.asyncio
async def test_reddit_connector_delegates_to_firecrawl_when_configured(reddit_fixture):
    connector = RedditConnector()

    with patch.object(connector._firecrawl_client, "is_configured", return_value=True):
        with patch.object(connector._firecrawl_client, "search", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = reddit_fixture["data"]
            records = await connector.fetch_mentions(
                business_name="Spice Symphony",
                keywords=["biryani", "service"],
                credentials={"firecrawl_api_key": "fc-override"},
            )

    assert len(records) == 3
    assert records[0].external_id.startswith("reddit_")


@pytest.mark.asyncio
async def test_reddit_connector_falls_back_to_mock_without_keys():
    connector = RedditConnector()

    with patch.object(connector._firecrawl_client, "is_configured", return_value=False):
        records = await connector.fetch_mentions(
            business_name="Spice Symphony",
            keywords=["biryani"],
            credentials={},
        )

    # Falls back to MockPlatformConnector("Reddit")
    assert len(records) > 0
    assert records[0].platform == "Reddit"


@pytest.mark.asyncio
async def test_reddit_normalization_e2e(reddit_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = RedditFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = reddit_fixture["data"]
        query = PlatformQueryBuilder.build_query("Reddit", "Spice Symphony", ["food"])
        raw_records = await provider.search_mentions(query)

    normalized, errors = MentionNormalizer.normalize_batch(raw_records, business_id="biz_test123")
    assert len(errors) == 0
    assert len(normalized) == 3
    assert normalized[0].business_id == "biz_test123"
    assert normalized[0].platform == "Reddit"
    assert len(normalized[0].content_hash) == 64
