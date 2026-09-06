"""Tests for FirecrawlClient async HTTP search and scrape operations."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.integrations.firecrawl_client import (
    FirecrawlApiError,
    FirecrawlAuthError,
    FirecrawlClient,
    FirecrawlRateLimitError,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def reddit_fixture():
    with open(FIXTURES_DIR / "firecrawl_reddit_search_response.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def scrape_fixture():
    with open(FIXTURES_DIR / "firecrawl_scrape_response.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_firecrawl_search_success(reddit_fixture):
    client = FirecrawlClient(api_key="test-key")

    mock_resp = httpx.Response(200, json=reddit_fixture, request=httpx.Request("POST", "https://api.firecrawl.dev/v1/search"))
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        results = await client.search("Spice Symphony", limit=5)

    assert len(results) == 3
    assert "bangalore" in results[0]["url"]


@pytest.mark.asyncio
async def test_firecrawl_scrape_success(scrape_fixture):
    client = FirecrawlClient(api_key="test-key")

    mock_resp = httpx.Response(200, json=scrape_fixture, request=httpx.Request("POST", "https://api.firecrawl.dev/v1/scrape"))
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        result = await client.scrape("https://example.com/review/123")

    assert result is not None
    assert "Spice Symphony Experience" in result["markdown"]


@pytest.mark.asyncio
async def test_firecrawl_search_auth_error():
    client = FirecrawlClient(api_key="invalid-key")

    mock_resp = httpx.Response(401, text="Unauthorized", request=httpx.Request("POST", "https://api.firecrawl.dev/v1/search"))
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with pytest.raises(FirecrawlAuthError):
            await client.search("Test Query")


@pytest.mark.asyncio
async def test_firecrawl_search_rate_limit():
    client = FirecrawlClient(api_key="test-key", max_retries=1)

    mock_resp = httpx.Response(429, text="Rate limited", request=httpx.Request("POST", "https://api.firecrawl.dev/v1/search"))
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with pytest.raises(FirecrawlRateLimitError):
            await client.search("Test Query")


@pytest.mark.asyncio
async def test_firecrawl_search_server_error():
    client = FirecrawlClient(api_key="test-key", max_retries=1)

    mock_resp = httpx.Response(500, text="Internal server error", request=httpx.Request("POST", "https://api.firecrawl.dev/v1/search"))
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        with pytest.raises(FirecrawlApiError):
            await client.search("Test Query")


@pytest.mark.asyncio
async def test_firecrawl_search_timeout_recovers():
    client = FirecrawlClient(api_key="test-key", max_retries=1)

    mock_success = httpx.Response(200, json={"success": True, "data": [{"url": "https://reddit.com", "title": "Test"}]})
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        # First attempt raises timeout, second succeeds
        mock_post.side_effect = [
            httpx.TimeoutException("Timeout"),
            mock_success,
        ]
        results = await client.search("Test Query")

    assert len(results) == 1
    assert results[0]["url"] == "https://reddit.com"


def test_firecrawl_is_configured():
    client_no_key = FirecrawlClient(api_key="")
    assert not client_no_key.is_configured()

    client_with_key = FirecrawlClient(api_key="fc-live-key")
    assert client_with_key.is_configured()
