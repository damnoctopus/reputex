"""JustDial connector skeleton for Indian business directory monitoring."""

from datetime import datetime
from typing import Any

from app.integrations.base import PlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.schemas.ingestion import RawMentionRecord


class JustDialConnector(PlatformConnector):
    platform_name = "JustDial"

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        _ = PlatformQueryBuilder.build_query(
            platform="JustDial",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )
        from app.integrations.mock_connector import MockPlatformConnector

        return await MockPlatformConnector("JustDial").fetch_mentions(
            business_name, keywords, since=since, cursor=cursor, location=location
        )

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        return await self.fetch_mentions(business_identifier, [], since=since, cursor=cursor, credentials=credentials)

    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        return True
