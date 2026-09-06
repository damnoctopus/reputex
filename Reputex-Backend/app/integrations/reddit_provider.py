"""Provider protocol for Reddit data acquisition.

Defines the contract that any Reddit data source (Firecrawl-first, official API, or mock)
must implement to feed into the RepuTex normalization and deduplication pipeline.
"""

from datetime import datetime
from typing import Any, Protocol, runtime_checkable

from app.schemas.ingestion import PlatformQuery, RawMentionRecord


@runtime_checkable
class RedditProvider(Protocol):
    """Protocol for acquiring public Reddit discussions and comments.

    Implementations MUST:
    - Return mentions as RawMentionRecord instances
    - Set published_at from the source's actual timestamp, NEVER ingestion time
    - Set source_url from the Reddit permalink
    - Set external_id to a deterministic, unique identifier (reddit_t3_..., reddit_c_...)
    """

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Search and extract public Reddit posts and comments matching query."""
        ...
