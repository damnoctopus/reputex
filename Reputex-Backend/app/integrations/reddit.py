"""Reddit API connector skeleton.

Supports Reddit OAuth2 API discussions and comments collection.
"""

from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.schemas.ingestion import RawMentionRecord


class RedditConnector(PlatformConnector):
    platform_name = "Reddit"

    def __init__(self):
        self.client_id = settings.REDDIT_CLIENT_ID
        self.client_secret = settings.REDDIT_CLIENT_SECRET
        self.user_agent = settings.REDDIT_USER_AGENT

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch Reddit posts and comments matching brand query."""
        _ = PlatformQueryBuilder.build_query(
            platform="Reddit",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        creds = credentials or {}
        client_id = creds.get("client_id") or self.client_id
        client_secret = creds.get("client_secret") or self.client_secret

        if not client_id or not client_secret:
            logger.warning("Reddit API credentials not set. Falling back to mock connector.")
            from app.integrations.mock_connector import MockPlatformConnector

            return await MockPlatformConnector("Reddit").fetch_mentions(
                business_name, keywords, since=since, cursor=cursor, location=location
            )
        # Real Reddit OAuth2 client execution will be wired in Phase 3
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
        logger.info(f"Replying to Reddit comment {external_mention_id}")
        return True
