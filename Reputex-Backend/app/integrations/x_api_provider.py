"""Optional secondary X / Twitter API v2 Recent Search provider.

Skeleton adapter satisfying the XProvider protocol. Used only when explicit
Twitter API Bearer Token credentials are provided and live API mode is desired.
"""

from datetime import datetime
from typing import Any

from app.core.logging import logger
from app.integrations.x_provider import XProvider
from app.schemas.ingestion import PlatformQuery, RawMentionRecord


class XApiProvider(XProvider):
    """Optional official Twitter API v2 adapter. Secondary to Firecrawl."""

    def __init__(self, bearer_token: str | None = None):
        self.bearer_token = bearer_token

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch mentions via official Twitter API v2 search endpoint (stub / future extension)."""
        logger.info(f"XApiProvider: Live Twitter API called for query '{query.query_string}'. Optional adapter.")
        return []
