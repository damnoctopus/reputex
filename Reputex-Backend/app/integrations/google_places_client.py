"""Async HTTP client for Google Places API (New).

Wraps the `places.googleapis.com/v1/` REST surface:
  - Text Search (POST places:searchText) — discover place_id from business name + location
  - Place Details (GET places/{place_id}) — fetch reviews and metadata

Implements the GoogleReviewProvider protocol for use by GoogleConnector.

Key design decisions:
  - Uses httpx.AsyncClient with configurable timeout and retries
  - All URLs come from Google's response (googleMapsUri), never constructed
  - published_at is parsed from the review's publishTime, never set to ingestion time
  - The Places API (New) returns at most 5 reviews per request — this is accepted for MVP
"""

from datetime import UTC, datetime
from typing import Any

import httpx

from app.core.logging import logger
from app.schemas.ingestion import RawMentionRecord

# Google Places API (New) base URL
_BASE_URL = "https://places.googleapis.com/v1"

# Default timeout for API requests
_DEFAULT_TIMEOUT = 15.0

# Maximum retries for transient failures
_MAX_RETRIES = 2


class GooglePlacesApiError(Exception):
    """Raised when the Google Places API returns an error response."""

    def __init__(self, status_code: int, message: str, detail: Any = None):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Google Places API error {status_code}: {message}")


class GooglePlacesClient:
    """Async HTTP client for Google Places API (New).

    Implements the GoogleReviewProvider protocol.
    """

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _MAX_RETRIES,
    ):
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries

    async def discover_place(
        self,
        business_name: str,
        location: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Discover a Google place using Text Search.

        POST https://places.googleapis.com/v1/places:searchText

        Returns dict with place_id, google_maps_uri, display_name, or None if not found.
        """
        effective_key = api_key or self._api_key
        if not effective_key:
            logger.warning("GooglePlacesClient.discover_place: no API key provided.")
            return None

        # Build the text query: business name + location for locality targeting
        text_query = business_name
        if location and location.strip():
            text_query = f"{business_name} {location.strip()}"

        request_body = {
            "textQuery": text_query,
            "pageSize": 1,  # Only need the top match
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": effective_key,
            "X-Goog-FieldMask": (
                "places.id,"
                "places.displayName,"
                "places.googleMapsUri,"
                "places.formattedAddress,"
                "places.rating,"
                "places.userRatingCount"
            ),
        }

        url = f"{_BASE_URL}/places:searchText"

        for attempt in range(1, self._max_retries + 2):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=request_body, headers=headers)

                if resp.status_code == 200:
                    data = resp.json()
                    places = data.get("places", [])
                    if not places:
                        logger.info(f"Google Text Search returned no results for '{text_query}'.")
                        return None

                    place = places[0]
                    place_id = place.get("id", "")
                    google_maps_uri = place.get("googleMapsUri", "")
                    display_name = place.get("displayName", {}).get("text", business_name)
                    formatted_address = place.get("formattedAddress", "")
                    rating = place.get("rating")
                    user_rating_count = place.get("userRatingCount", 0)

                    logger.info(
                        f"Google Text Search found: '{display_name}' (place_id={place_id}, "
                        f"rating={rating}, reviews={user_rating_count})"
                    )

                    return {
                        "place_id": place_id,
                        "google_maps_uri": google_maps_uri,
                        "display_name": display_name,
                        "formatted_address": formatted_address,
                        "rating": rating,
                        "user_rating_count": user_rating_count,
                    }

                elif resp.status_code in (429, 500, 502, 503):
                    logger.warning(
                        f"Google Text Search returned {resp.status_code} (attempt {attempt}/{self._max_retries + 1}). Retrying..."
                    )
                    continue

                else:
                    error_body = resp.text
                    logger.error(f"Google Text Search failed with {resp.status_code}: {error_body}")
                    raise GooglePlacesApiError(resp.status_code, error_body)

            except httpx.TimeoutException:
                logger.warning(
                    f"Google Text Search timed out (attempt {attempt}/{self._max_retries + 1})."
                )
                if attempt > self._max_retries:
                    raise
                continue

            except GooglePlacesApiError:
                raise

            except Exception as e:
                logger.error(f"Unexpected error in Google Text Search: {e}")
                if attempt > self._max_retries:
                    raise
                continue

        return None

    async def fetch_reviews(
        self,
        place_id: str,
        google_maps_uri: str,
        api_key: str | None = None,
    ) -> list[RawMentionRecord]:
        """Fetch reviews for a known place_id via Place Details.

        GET https://places.googleapis.com/v1/places/{place_id}

        NOTE: The official Places API (New) returns at most 5 recent reviews.
        This is a known API limitation — results should NOT be treated as
        a complete review history.
        """
        effective_key = api_key or self._api_key
        if not effective_key:
            logger.warning("GooglePlacesClient.fetch_reviews: no API key provided.")
            return []

        headers = {
            "X-Goog-Api-Key": effective_key,
            "X-Goog-FieldMask": (
                "reviews.name,"
                "reviews.relativePublishTimeDescription,"
                "reviews.rating,"
                "reviews.text,"
                "reviews.originalText,"
                "reviews.authorAttribution,"
                "reviews.publishTime,"
                "reviews.googleMapsUri"
            ),
        }

        url = f"{_BASE_URL}/places/{place_id}"

        for attempt in range(1, self._max_retries + 2):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.get(url, headers=headers)

                if resp.status_code == 200:
                    data = resp.json()
                    raw_reviews = data.get("reviews", [])

                    if not raw_reviews:
                        logger.info(f"No reviews returned for place_id={place_id}.")
                        return []

                    records = self._parse_reviews(raw_reviews, place_id, google_maps_uri)
                    logger.info(
                        f"Parsed {len(records)} reviews from Google for place_id={place_id} "
                        f"(API returns max 5 recent reviews)."
                    )
                    return records

                elif resp.status_code in (429, 500, 502, 503):
                    logger.warning(
                        f"Google Place Details returned {resp.status_code} "
                        f"(attempt {attempt}/{self._max_retries + 1}). Retrying..."
                    )
                    continue

                else:
                    error_body = resp.text
                    logger.error(f"Google Place Details failed with {resp.status_code}: {error_body}")
                    raise GooglePlacesApiError(resp.status_code, error_body)

            except httpx.TimeoutException:
                logger.warning(
                    f"Google Place Details timed out (attempt {attempt}/{self._max_retries + 1})."
                )
                if attempt > self._max_retries:
                    raise
                continue

            except GooglePlacesApiError:
                raise

            except Exception as e:
                logger.error(f"Unexpected error in Google Place Details: {e}")
                if attempt > self._max_retries:
                    raise
                continue

        return []

    @staticmethod
    def _parse_reviews(
        raw_reviews: list[dict[str, Any]],
        place_id: str,
        google_maps_uri: str,
    ) -> list[RawMentionRecord]:
        """Transform Google Places API review objects into RawMentionRecords.

        Key invariants:
        - source_url uses review's googleMapsUri (falls back to place's googleMapsUri)
        - published_at is parsed from the review's publishTime field
        - external_id is derived from the review's resource name (stable identifier)
        """
        records: list[RawMentionRecord] = []
        now = datetime.now(UTC)

        for review in raw_reviews:
            try:
                # Extract review resource name as stable external ID
                # Format: "places/{place_id}/reviews/{review_id}"
                review_name = review.get("name", "")
                external_id = review_name.replace("/", "_") if review_name else None

                # Use the review's own googleMapsUri, fall back to place-level URI
                review_maps_uri = review.get("googleMapsUri") or google_maps_uri

                # Parse the actual review publication timestamp
                publish_time_str = review.get("publishTime")
                published_at = _parse_publish_time(publish_time_str)

                # Extract review text — prefer originalText, fall back to text
                original_text = review.get("originalText", {})
                text_obj = review.get("text", {})
                content = (
                    original_text.get("text", "")
                    or text_obj.get("text", "")
                    or ""
                )

                if not content.strip():
                    # Skip reviews with no text content (rating-only reviews)
                    continue

                # Author attribution
                author_attr = review.get("authorAttribution", {})
                author_name = author_attr.get("displayName", "Anonymous")
                author_uri = author_attr.get("uri", "")
                author_photo = author_attr.get("photoUri")

                # Rating
                rating = review.get("rating")

                records.append(
                    RawMentionRecord(
                        platform="Google",
                        external_id=external_id,
                        source_url=review_maps_uri,
                        title=None,
                        content=content,
                        author=author_name,
                        author_id=author_uri or None,
                        author_avatar=author_photo,
                        published_at=published_at,
                        collected_at=now,
                        rating=float(rating) if rating is not None else None,
                        engagement={"likes": 0, "shares": 0, "comments": 0},
                        metadata={
                            "place_id": place_id,
                            "review_name": review_name,
                            "relative_time": review.get("relativePublishTimeDescription", ""),
                        },
                        raw_payload=review,
                    )
                )
            except Exception as e:
                logger.warning(f"Failed to parse Google review: {e}")
                continue

        return records


def _parse_publish_time(publish_time_str: str | None) -> datetime | None:
    """Parse Google's publishTime (RFC 3339) into a timezone-aware datetime.

    Returns None if the string is missing or unparseable — the normalizer
    will fall back to datetime.now(UTC), which is acceptable for reviews
    where Google omits the timestamp. But this should be rare; the Places API
    (New) reliably includes publishTime.
    """
    if not publish_time_str:
        return None

    try:
        # Google returns ISO 8601 / RFC 3339: "2024-08-15T10:30:00Z"
        return datetime.fromisoformat(publish_time_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        logger.warning(f"Could not parse Google review publishTime: '{publish_time_str}'")
        return None
