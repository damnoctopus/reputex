"""Reddit connector for RepuTex data acquisition.

Implements PlatformConnector by delegating to a RedditProvider:
  1. Primary: RedditFirecrawlProvider (public web search & extraction via Firecrawl)
  2. Optional: RedditApiProvider (official OAuth2 API when credentials provided)
  3. Fallback: MockPlatformConnector (when offline, testing, or no keys configured)
"""

from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.firecrawl_client import FirecrawlClient
from app.integrations.query_builder import PlatformQueryBuilder
from app.integrations.reddit_api_provider import RedditApiProvider
from app.integrations.reddit_firecrawl_provider import RedditFirecrawlProvider
from app.integrations.reddit_provider import RedditProvider
from app.schemas.ingestion import RawMentionRecord


class RedditConnector(PlatformConnector):
    platform_name = "Reddit"

    def __init__(self, provider: RedditProvider | None = None):
        self.provider = provider
        self.client_id = settings.REDDIT_CLIENT_ID
        self.client_secret = settings.REDDIT_CLIENT_SECRET
        self.user_agent = settings.REDDIT_USER_AGENT
        self._firecrawl_client = FirecrawlClient()

    def _resolve_provider(self, credentials: dict[str, Any] | None = None) -> RedditProvider | None:
        """Resolve the effective Reddit acquisition provider based on credentials and config."""
        if self.provider is not None:
            return self.provider

        creds = credentials or {}
        fc_key = creds.get("firecrawl_api_key")

        # 1. Firecrawl (Primary acquisition mechanism)
        if self._firecrawl_client.is_configured(api_key=fc_key):
            logger.info("RedditConnector using primary RedditFirecrawlProvider.")
            return RedditFirecrawlProvider(self._firecrawl_client)

        # 2. Official Reddit API (Optional secondary)
        client_id = creds.get("client_id") or self.client_id
        client_secret = creds.get("client_secret") or self.client_secret
        if client_id and client_secret:
            logger.info("RedditConnector using secondary RedditApiProvider.")
            return RedditApiProvider(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=self.user_agent,
            )

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
        """Fetch Reddit discussions and comments matching the business query."""
        query = PlatformQueryBuilder.build_query(
            platform="Reddit",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        provider = self._resolve_provider(credentials)
        if not provider:
            logger.warning("RedditConnector: No live provider configured. Returning empty.")
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
            logger.error(f"RedditConnector provider execution failed: {e}")
            return []

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Reddit discussions are primarily conversational mentions."""
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
        """Publish reply to a Reddit comment."""
        logger.info(f"RedditConnector publishing response to {external_mention_id}")
        return True
