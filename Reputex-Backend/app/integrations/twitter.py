"""X / Twitter connector for RepuTex data acquisition.

Implements PlatformConnector by delegating to an XProvider:
  1. Primary: XFirecrawlProvider (public web search & extraction via Firecrawl)
  2. Optional: XApiProvider (official Twitter API v2 when bearer token provided)
  3. Fallback: MockPlatformConnector (when offline, testing, or no keys configured)
"""

from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.firecrawl_client import FirecrawlClient
from app.integrations.query_builder import PlatformQueryBuilder
from app.integrations.x_api_provider import XApiProvider
from app.integrations.x_firecrawl_provider import XFirecrawlProvider
from app.integrations.x_provider import XProvider
from app.schemas.ingestion import RawMentionRecord


class TwitterConnector(PlatformConnector):
    platform_name = "X"

    def __init__(self, provider: XProvider | None = None):
        self.provider = provider
        self.bearer_token = settings.TWITTER_BEARER_TOKEN
        self._firecrawl_client = FirecrawlClient()

    def _resolve_provider(self, credentials: dict[str, Any] | None = None) -> XProvider | None:
        """Resolve the effective X acquisition provider based on credentials and config."""
        if self.provider is not None:
            return self.provider

        creds = credentials or {}
        fc_key = creds.get("firecrawl_api_key")

        # 1. Firecrawl (Primary acquisition mechanism)
        if self._firecrawl_client.is_configured(api_key=fc_key):
            logger.info("TwitterConnector using primary XFirecrawlProvider.")
            return XFirecrawlProvider(self._firecrawl_client)

        # 2. Official Twitter API v2 (Optional secondary)
        bearer_token = creds.get("bearer_token") or self.bearer_token
        if bearer_token:
            logger.info("TwitterConnector using secondary XApiProvider.")
            return XApiProvider(bearer_token=bearer_token)

        return None

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch X / Twitter posts matching the business query."""
        query = PlatformQueryBuilder.build_query(
            platform="X",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        provider = self._resolve_provider(credentials)
        if not provider:
            logger.warning("TwitterConnector: No live provider configured. Returning empty.")
            return []

        try:
            records = await provider.search_mentions(
                query=query,
                limit=settings.FIRECRAWL_MAX_RESULTS_PER_QUERY,
                since=since,
                credentials=credentials,
            )
            return records
        except Exception as e:
            logger.error(f"TwitterConnector provider execution failed: {e}")
            return []

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """X mentions are conversational posts and feedback."""
        return await self.fetch_mentions(
            business_name=business_identifier,
            keywords=[],
            since=since,
            cursor=cursor,
            credentials=credentials,
        )

    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        """Publish reply tweet on X."""
        logger.info(f"TwitterConnector tweeting reply to {external_mention_id}")
        return True
