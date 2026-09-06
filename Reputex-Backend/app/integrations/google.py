"""Google Places API (New) connector for RepuTex data acquisition.

Implements the PlatformConnector interface using GooglePlacesClient
(which satisfies the GoogleReviewProvider protocol) to:
  1. Discover a business's place_id via Text Search
  2. Cache place_id in PlatformConnection.metadata (NOT credentials)
  3. Fetch reviews via Place Details
  4. Emit RawMentionRecords for the existing normalization pipeline

Design invariants:
  - source_url comes from Google's returned googleMapsUri, never constructed
  - published_at is the review's actual publishTime, never ingestion time
  - credentials stores API secrets only; metadata stores place_id and related state
  - The Places API (New) returns at most 5 recent reviews per request
  - Falls back to MockPlatformConnector when no API key is configured
"""

from datetime import datetime
from typing import Any

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.google_places_client import GooglePlacesClient
from app.schemas.ingestion import RawMentionRecord


class GoogleConnector(PlatformConnector):
    platform_name = "Google"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.GOOGLE_PLACES_API_KEY
        self._client = GooglePlacesClient(api_key=self.api_key)

    async def fetch_mentions(
        self,
        business_name: str,
        keywords: list[str],
        since: datetime | None = None,
        cursor: str | None = None,
        location: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch Google reviews for a business.

        Flow:
          1. Resolve the effective API key from credentials (secrets) or instance config
          2. Check metadata for a cached place_id
          3. If no cached place_id, run Text Search to discover it
          4. Fetch reviews via Place Details
          5. Return RawMentionRecords for the normalization pipeline
        """
        # Resolve API key: credentials hold secrets, instance key is fallback
        effective_key = (credentials or {}).get("api_key") or self.api_key

        if not effective_key:
            logger.warning("GOOGLE_PLACES_API_KEY is not configured. Falling back to mock data.")
            from app.integrations.mock_connector import MockPlatformConnector

            return await MockPlatformConnector("Google").fetch_mentions(
                business_name, keywords, since=since, cursor=cursor, location=location
            )

        # Update client with the effective key for this request
        client = GooglePlacesClient(api_key=effective_key)

        # Check for cached place_id in metadata (not credentials)
        # The caller (IngestionService) passes conn.metadata via the metadata parameter
        # We receive it through the credentials parameter but extract place data from metadata
        metadata = (credentials or {}).get("_metadata", {})
        cached_place_id = metadata.get("place_id")
        cached_maps_uri = metadata.get("google_maps_uri", "")

        if cached_place_id:
            logger.info(f"Using cached place_id={cached_place_id} for '{business_name}'.")
            place_id = cached_place_id
            google_maps_uri = cached_maps_uri
        else:
            # Discover via Text Search
            logger.info(f"Discovering Google place for '{business_name}' (location={location}).")
            discovery = await client.discover_place(
                business_name=business_name,
                location=location,
                api_key=effective_key,
            )

            if not discovery:
                logger.warning(f"No Google place found for '{business_name}'. Returning empty.")
                return []

            place_id = discovery["place_id"]
            google_maps_uri = discovery["google_maps_uri"]

            # Signal to IngestionService that metadata should be updated
            # We embed this in a special key that IngestionService can detect
            self._discovered_metadata = {
                "place_id": place_id,
                "google_maps_uri": google_maps_uri,
                "display_name": discovery.get("display_name", business_name),
                "formatted_address": discovery.get("formatted_address", ""),
                "aggregate_rating": discovery.get("rating"),
                "user_rating_count": discovery.get("user_rating_count", 0),
            }

        # Fetch reviews
        reviews = await client.fetch_reviews(
            place_id=place_id,
            google_maps_uri=google_maps_uri,
            api_key=effective_key,
        )

        return reviews

    def get_discovered_metadata(self) -> dict[str, Any] | None:
        """Return metadata discovered during the last fetch_mentions call.

        Called by IngestionService after fetch_mentions to update
        PlatformConnection.metadata with the discovered place_id.
        Returns None if no new discovery was made (place_id was cached).
        """
        return getattr(self, "_discovered_metadata", None)

    async def fetch_reviews(
        self,
        business_identifier: str,
        since: datetime | None = None,
        cursor: str | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch reviews by business name (delegates to fetch_mentions)."""
        return await self.fetch_mentions(
            business_identifier, [], since=since, cursor=cursor, credentials=credentials
        )

    async def publish_response(
        self,
        external_mention_id: str,
        response_text: str,
    ) -> bool:
        """Publish a response to a Google review.

        Not yet implemented — requires Google Business Profile API
        which is separate from Places API and needs OAuth2 authorization.
        """
        logger.info(f"publish_response not yet implemented for Google review {external_mention_id}")
        return False
