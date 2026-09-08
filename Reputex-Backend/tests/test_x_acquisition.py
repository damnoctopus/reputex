"""Tests for X / Twitter acquisition via Firecrawl and TwitterConnector."""

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from app.integrations.firecrawl_client import FirecrawlClient
from app.integrations.query_builder import PlatformQueryBuilder
from app.integrations.twitter import TwitterConnector
from app.integrations.x_firecrawl_provider import XFirecrawlProvider
from app.schemas.ingestion import PlatformQuery
from app.services.normalizer import MentionNormalizer

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def x_fixture():
    with open(FIXTURES_DIR / "firecrawl_x_search_response.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_x_firecrawl_parses_posts(x_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = XFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = x_fixture["data"]
        query = PlatformQuery(
            platform="X",
            query_string="Spice Symphony",
            keywords_used=["Spice Symphony"],
        )
        records = await provider.search_mentions(query, limit=5)

    assert len(records) == 2

    post1 = records[0]
    assert post1.platform == "X"
    assert post1.external_id == "x_1789012345678901234"
    assert post1.author == "@techie_in_blr"
    assert "Spice Symphony" in post1.content
    assert post1.published_at == datetime(2026, 8, 18, 19, 30, 0, tzinfo=UTC)
    assert post1.engagement["likes"] == 28
    assert post1.engagement["shares"] == 4
    assert post1.engagement["comments"] == 7
    assert post1.metadata["username"] == "techie_in_blr"

    post2 = records[1]
    assert post2.external_id == "x_1789012345678901235"
    assert post2.author == "@blr_eats"
    assert post2.engagement["likes"] == 45
    assert post2.engagement["shares"] == 12
    assert post2.engagement["comments"] == 19


@pytest.mark.asyncio
async def test_x_published_at_is_source_time_not_ingestion_time(x_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = XFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = [x_fixture["data"][0]]
        query = PlatformQuery(platform="X", query_string="Spice Symphony", keywords_used=["Spice Symphony"])
        records = await provider.search_mentions(query)

    rec = records[0]
    now_utc = datetime.now(UTC)
    assert rec.published_at is not None
    assert (now_utc - rec.published_at).total_seconds() > 3600
    assert rec.published_at.year == 2026
    assert rec.published_at.month == 8


@pytest.mark.asyncio
async def test_x_connector_delegates_to_firecrawl_when_configured(x_fixture):
    connector = TwitterConnector()

    with patch.object(connector._firecrawl_client, "is_configured", return_value=True):
        with patch.object(connector._firecrawl_client, "search", new_callable=AsyncMock) as mock_search:
            mock_search.return_value = x_fixture["data"]
            records = await connector.fetch_mentions(
                business_name="Spice Symphony",
                keywords=["food"],
                credentials={"firecrawl_api_key": "fc-key"},
            )

    assert len(records) == 2
    assert records[0].external_id.startswith("x_")


@pytest.mark.asyncio
async def test_x_connector_returns_empty_without_keys():
    connector = TwitterConnector()

    with patch.object(connector._firecrawl_client, "is_configured", return_value=False):
        records = await connector.fetch_mentions(
            business_name="Spice Symphony",
            keywords=["food"],
            credentials={},
        )

    assert records == []


@pytest.mark.asyncio
async def test_x_normalization_e2e(x_fixture):
    client = FirecrawlClient(api_key="fc-test-key")
    provider = XFirecrawlProvider(client)

    with patch.object(client, "search", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = x_fixture["data"]
        query = PlatformQueryBuilder.build_query("X", "Spice Symphony", ["food"])
        raw_records = await provider.search_mentions(query)

    normalized, errors = MentionNormalizer.normalize_batch(raw_records, business_id="biz_test456")
    assert len(errors) == 0
    assert len(normalized) == 2
    assert normalized[0].business_id == "biz_test456"
    assert normalized[0].platform == "X"
    assert len(normalized[0].content_hash) == 64
