"""Centralized Async HTTP client for Firecrawl web search and scrape operations.

Provides structured search and extraction across public web content (primarily
Reddit discussions and X posts) with bounded retries, rate-limit backoff,
and error taxonomy.
"""

import asyncio
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import logger

_DEFAULT_TIMEOUT = 15.0
_MAX_RETRIES = 2
_BASE_BACKOFF_SECONDS = 1.0


class FirecrawlApiError(Exception):
    """Base exception for Firecrawl API failures."""

    def __init__(self, status_code: int, message: str, detail: Any = None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Firecrawl API error {status_code}: {message}")


class FirecrawlAuthError(FirecrawlApiError):
    """Raised on invalid or missing Firecrawl API key (401/403)."""


class FirecrawlRateLimitError(FirecrawlApiError):
    """Raised when Firecrawl rate limit or quota is exceeded (429)."""


class FirecrawlClient:
    """Async client wrapping the Firecrawl REST API (/v1/search and /v1/scrape)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _MAX_RETRIES,
    ):
        self._api_key = api_key if api_key is not None else settings.FIRECRAWL_API_KEY
        self._base_url = (base_url or settings.FIRECRAWL_BASE_URL).rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

    def is_configured(self, api_key: str | None = None) -> bool:
        """Check whether Firecrawl credentials are present and enabled."""
        key = api_key if api_key is not None else (self._api_key if self._api_key is not None else settings.FIRECRAWL_API_KEY)
        if not key:
            return False
        # If an explicit key was provided, treat as configured. Otherwise check settings flag
        return bool(settings.FIRECRAWL_ENABLED or api_key or self._api_key)

    def _get_headers(self, api_key: str | None = None) -> dict[str, str]:
        key = api_key if api_key is not None else (self._api_key if self._api_key is not None else settings.FIRECRAWL_API_KEY)
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        }

    async def search(
        self,
        query: str,
        limit: int = 5,
        scrape_options: dict[str, Any] | None = None,
        api_key: str | None = None,
    ) -> list[dict[str, Any]]:
        """Search the public web via Firecrawl /v1/search.

        Returns a list of search result dictionaries containing URLs, titles,
        markdown content, and metadata.
        """
        effective_key = api_key if api_key is not None else (self._api_key if self._api_key is not None else settings.FIRECRAWL_API_KEY)
        if not effective_key:
            logger.warning("FirecrawlClient.search: no API key configured.")
            return []

        # Bound the query limit according to settings
        max_allowed = settings.FIRECRAWL_MAX_RESULTS_PER_QUERY
        bounded_limit = min(max(1, limit), max_allowed)

        endpoint = f"{self._base_url}/v1/search"
        payload = {
            "query": query,
            "limit": bounded_limit,
            "scrapeOptions": scrape_options or {"formats": ["markdown"]},
        }
        headers = self._get_headers(effective_key)

        last_exc: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(endpoint, json=payload, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    results = data.get("data", [])
                    if isinstance(results, list):
                        return results
                    return []

                if response.status_code in (401, 403):
                    err_msg = f"Authentication failed: {response.text}"
                    logger.error(f"Firecrawl search auth error: {response.status_code}")
                    raise FirecrawlAuthError(response.status_code, err_msg)

                if response.status_code == 429:
                    err_msg = f"Rate limit exceeded: {response.text}"
                    logger.warning("Firecrawl rate limit (429) hit during search.")
                    if attempt < self._max_retries:
                        backoff = _BASE_BACKOFF_SECONDS * (2**attempt)
                        await asyncio.sleep(backoff)
                        continue
                    raise FirecrawlRateLimitError(429, err_msg)

                if response.status_code >= 500:
                    logger.warning(
                        f"Firecrawl server error {response.status_code} on search attempt {attempt + 1}"
                    )
                    if attempt < self._max_retries:
                        backoff = _BASE_BACKOFF_SECONDS * (2**attempt)
                        await asyncio.sleep(backoff)
                        continue
                    raise FirecrawlApiError(response.status_code, f"Server error: {response.text}")

                # 4xx client errors (non-retryable)
                logger.error(f"Firecrawl search error {response.status_code}: {response.text}")
                return []

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                logger.warning(f"Firecrawl network error on attempt {attempt + 1}: {exc}")
                if attempt < self._max_retries:
                    backoff = _BASE_BACKOFF_SECONDS * (2**attempt)
                    await asyncio.sleep(backoff)
                    continue
                break
            except (FirecrawlAuthError, FirecrawlRateLimitError, FirecrawlApiError):
                raise
            except Exception as exc:
                logger.error(f"Unexpected error in Firecrawl search: {exc}")
                return []

        if last_exc:
            logger.error(f"Firecrawl search failed after {self._max_retries + 1} attempts: {last_exc}")
        return []

    async def scrape(
        self,
        url: str,
        formats: list[str] | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Scrape a specific URL via Firecrawl /v1/scrape.

        Returns a dictionary containing markdown and metadata, or None on failure.
        """
        effective_key = api_key if api_key is not None else (self._api_key if self._api_key is not None else settings.FIRECRAWL_API_KEY)
        if not effective_key:
            logger.warning("FirecrawlClient.scrape: no API key configured.")
            return None

        endpoint = f"{self._base_url}/v1/scrape"
        payload = {
            "url": url,
            "formats": formats or ["markdown"],
        }
        headers = self._get_headers(effective_key)

        for attempt in range(self._max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(endpoint, json=payload, headers=headers)

                if response.status_code == 200:
                    body = response.json()
                    return body.get("data")

                if response.status_code in (401, 403):
                    raise FirecrawlAuthError(response.status_code, f"Auth error: {response.text}")

                if response.status_code == 429:
                    if attempt < self._max_retries:
                        await asyncio.sleep(_BASE_BACKOFF_SECONDS * (2**attempt))
                        continue
                    raise FirecrawlRateLimitError(429, f"Rate limited: {response.text}")

                if response.status_code >= 500:
                    if attempt < self._max_retries:
                        await asyncio.sleep(_BASE_BACKOFF_SECONDS * (2**attempt))
                        continue
                    return None

                logger.warning(f"Firecrawl scrape failed {response.status_code} for {url}")
                return None

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt < self._max_retries:
                    await asyncio.sleep(_BASE_BACKOFF_SECONDS * (2**attempt))
                    continue
                logger.warning(f"Firecrawl scrape network error for {url}: {exc}")
                return None
            except (FirecrawlAuthError, FirecrawlRateLimitError):
                raise
            except Exception as exc:
                logger.error(f"Unexpected error scraping {url}: {exc}")
                return None

        return None
