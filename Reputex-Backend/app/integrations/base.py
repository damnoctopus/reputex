"""Abstract base connector for external platforms (Google, Reddit, X, Google AI Overview)."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from app.schemas.ingestion import RawMentionRecord


class PlatformConnector(ABC):
    """Abstract interface that every platform adapter/scraper must implement."""

    platform_name: str = "Base"

    @abstractmethod
    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch brand mentions and social discussions from the external platform."""
        pass

    @abstractmethod
    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch customer ratings and reviews from the platform."""
        pass

    @abstractmethod
    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        """Publish an approved business reply/comment back to the original platform."""
        pass
