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
        from app.integrations.firecrawl_client import FirecrawlClient

        fc_client = FirecrawlClient()
        if not fc_client.is_configured():
            return []

        search_query = f"site:justdial.com {business_name}"
        if location:
            search_query += f" {location}"

        try:
            results = await fc_client.search(query=search_query, limit=3)
            records: list[RawMentionRecord] = []
            for item in results:
                url = item.get("url") or ""
                title = item.get("title") or ""
                content = item.get("description") or item.get("markdown") or title
                if not content:
                    continue
                records.append(
                    RawMentionRecord(
                        platform="JustDial",
                        external_id=f"justdial_{hash(url) & 0xFFFFFFFF}",
                        source_url=url,
                        title=title or None,
                        content=content,
                        author="JustDial Reviewer",
                        published_at=datetime.now(),
                        collected_at=datetime.now(),
                        rating=None,
                        engagement={"likes": 0, "shares": 0, "comments": 0},
                        metadata={"provider": "firecrawl"},
                        raw_payload=item,
                    )
                )
            return records
        except Exception:
            return []

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
