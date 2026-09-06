"""Optional secondary Reddit API provider (OAuth2 / Reddit Data API).

Skeleton adapter satisfying the RedditProvider protocol. Used only when explicit
Reddit API client credentials are provided and live API mode is desired.
"""

from datetime import datetime
from typing import Any

from app.core.logging import logger
from app.integrations.reddit_provider import RedditProvider
from app.schemas.ingestion import PlatformQuery, RawMentionRecord


class RedditApiProvider(RedditProvider):
    """Optional official Reddit API adapter. Secondary to Firecrawl."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        user_agent: str | None = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch mentions via official Reddit OAuth2 API (stub / future extension)."""
        logger.info(f"RedditApiProvider: Live API called for query '{query.query_string}'. Optional adapter.")
        return []
