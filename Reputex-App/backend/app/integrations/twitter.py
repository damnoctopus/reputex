"""X / Twitter API v2 connector skeleton.

Supports permitted Twitter API v2 Recent Search and filtered stream collection.
"""

from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.schemas.ingestion import RawMentionRecord


class TwitterConnector(PlatformConnector):
    platform_name = "X"

    def __init__(self):
        self.bearer_token = settings.TWITTER_BEARER_TOKEN

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch X tweets matching query."""
        _ = PlatformQueryBuilder.build_query(
            platform="X",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        creds = credentials or {}
        bearer_token = creds.get("bearer_token") or self.bearer_token

        if not bearer_token:
            logger.warning("Twitter bearer token not set. Falling back to mock connector.")
            from app.integrations.mock_connector import MockPlatformConnector

            return await MockPlatformConnector("X").fetch_mentions(
                business_name, keywords, since=since, cursor=cursor, location=location
            )
        # Real Twitter API v2 search endpoint wired in Phase 4
        return []

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        return []

    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        logger.info(f"Tweeting reply to {external_mention_id}")
        return True
