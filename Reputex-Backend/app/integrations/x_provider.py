"""Provider protocol for X / Twitter data acquisition.

Defines the contract that any X / Twitter data source (Firecrawl-first, official API, or mock)
must implement to feed into the RepuTex normalization and deduplication pipeline.
"""

from datetime import datetime
from typing import Any, Protocol, runtime_checkable

from app.schemas.ingestion import PlatformQuery, RawMentionRecord


@runtime_checkable
class XProvider(Protocol):
    """Protocol for acquiring public X / Twitter posts and discussions.

    Implementations MUST:
    - Return mentions as RawMentionRecord instances
    - Set published_at from the source's actual timestamp, NEVER ingestion time
    - Set source_url from the canonical post URL (x.com/... or twitter.com/...)
    - Set external_id to a deterministic identifier (x_{status_id})
    """

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Search and extract public X posts matching query."""
        ...
