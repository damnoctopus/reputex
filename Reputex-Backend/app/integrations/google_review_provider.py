"""Provider protocol for Google review acquisition.

Defines the interface that any Google review source must implement.
The default implementation uses the official Google Places API (New).
Future providers (e.g., Outscraper, SerpApi) can be swapped in via this protocol
without modifying the GoogleConnector or ingestion pipeline.
"""

from typing import Any, Protocol, runtime_checkable

from app.schemas.ingestion import RawMentionRecord


@runtime_checkable
class GoogleReviewProvider(Protocol):
    """Protocol for acquiring Google reviews from any underlying source.

    Implementations MUST:
    - Return reviews as RawMentionRecord instances
    - Set published_at from the source's actual review timestamp, NEVER ingestion time
    - Set source_url from the source's googleMapsUri, NEVER construct synthetic URLs
    - Set external_id to a stable, unique identifier per review
    """

    async def discover_place(
        self,
        business_name: str,
        location: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Discover a Google place_id for the given business.

        Returns a dict with at minimum:
          - place_id: str
          - google_maps_uri: str
          - display_name: str
        or None if no match found.
        """
        ...

    async def fetch_reviews(
        self,
        place_id: str,
        google_maps_uri: str,
        api_key: str | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch available reviews for a known place_id.

        NOTE: The official Places API (New) returns at most 5 recent reviews
        per request. This is a known limitation—do NOT treat the result as
        a complete review history.
        """
        ...
