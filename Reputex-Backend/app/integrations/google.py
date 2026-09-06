"""Google Business Profile & Places API connector skeleton.

Supports permitted Google Places API / Business Profile feeds and controlled data collection.
"""

from datetime import datetime
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.schemas.ingestion import RawMentionRecord


class GoogleConnector(PlatformConnector):
    platform_name = "Google"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.GOOGLE_PLACES_API_KEY

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch Google mentions and reviews for business."""
        query = PlatformQueryBuilder.build_query(
            platform="Google",
            business_name=business_name,
            keywords=keywords,
            location=location,
        )

        effective_key = (credentials or {}).get("api_key") or self.api_key

        if not effective_key:
            logger.warning("GOOGLE_PLACES_API_KEY is not configured. Falling back to mock data.")
            from app.integrations.mock_connector import MockPlatformConnector

            return await MockPlatformConnector("Google").fetch_mentions(
                business_name, keywords, since=since, cursor=cursor, location=location
            )

        # Real Google Places API call skeleton
        url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": query.query_string,
            "inputtype": "textquery",
            "fields": "place_id,name,rating,reviews",
            "key": effective_key,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    _ = resp.json()
                    # Candidate parsing will be implemented in Phase 2
                    return []
            except Exception as e:
                logger.error(f"Error calling Google Places API: {e}")
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
        logger.info(f"Publishing response to Google review {external_mention_id}")
        return True
