"""Primary X / Twitter acquisition provider using Firecrawl web search and extraction.

Implements the XProvider protocol by:
  1. Executing site-scoped Firecrawl searches for public X/Twitter posts
  2. Extracting reliable status IDs from canonical post URLs
  3. Parsing author attribution, true publication timestamps, and engagement
  4. Emitting typed RawMentionRecord instances into the existing pipeline
"""

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from dateutil import parser as date_parser

from app.core.logging import logger
from app.integrations.firecrawl_client import FirecrawlClient
from app.schemas.ingestion import PlatformQuery, RawMentionRecord

# Regex matching standard X / Twitter post permalinks
_X_URL_REGEX = re.compile(
    r"(?:x\.com|twitter\.com)/(?P<username>[^/]+)/status/(?P<status_id>\d+)",
    re.IGNORECASE,
)

# Regex to extract metric mentions in post text or markdown
_LIKES_REGEX = re.compile(r"(?P<likes>\d+)\s*likes?", re.IGNORECASE)
_RETWEETS_REGEX = re.compile(r"(?P<retweets>\d+)\s*(?:reposts?|retweets?)", re.IGNORECASE)
_REPLIES_REGEX = re.compile(r"(?P<replies>\d+)\s*(?:replies|quotes?|comments?)", re.IGNORECASE)


def _parse_published_time(raw_time: Any) -> datetime | None:
    """Parse ISO 8601 date string into UTC datetime. Never returns current time."""
    if not raw_time or not isinstance(raw_time, str):
        return None
    try:
        dt = date_parser.parse(raw_time)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        else:
            dt = dt.astimezone(UTC)
        return dt
    except Exception:
        return None


class XFirecrawlProvider:
    """Acquires public X / Twitter posts via Firecrawl."""

    def __init__(self, firecrawl_client: FirecrawlClient | None = None):
        self._client = firecrawl_client or FirecrawlClient()

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Search public X / Twitter content matching query via Firecrawl."""
        api_key = (credentials or {}).get("firecrawl_api_key")
        if not self._client.is_configured(api_key=api_key):
            logger.warning("XFirecrawlProvider: Firecrawl is not configured or disabled.")
            return []

        # Formulate search restricted to x.com and twitter.com
        scoped_query = f"(site:x.com OR site:twitter.com) {query.query_string.strip()}"
        logger.info(f"XFirecrawlProvider executing search: {scoped_query} (limit={limit})")

        results = await self._client.search(
            query=scoped_query,
            limit=limit,
            scrape_options={"formats": ["markdown"]},
            api_key=api_key,
        )

        records: list[RawMentionRecord] = []
        for item in results:
            record = self._parse_result_item(item)
            if record:
                if since and record.published_at and record.published_at < since:
                    continue
                records.append(record)

        logger.info(f"XFirecrawlProvider extracted {len(records)} mentions.")
        return records

    def _parse_result_item(self, item: dict[str, Any]) -> RawMentionRecord | None:
        """Parse a single Firecrawl search result into a RawMentionRecord."""
        url = item.get("url") or ""
        markdown = item.get("markdown") or ""
        title = item.get("title") or ""
        metadata = item.get("metadata") or {}

        # 1. Parse URL to extract username and status_id
        match = _X_URL_REGEX.search(url)
        username = match.group("username") if match else None
        status_id = match.group("status_id") if match else None

        # 2. Derive stable external ID (never generate random UUID)
        if status_id:
            external_id = f"x_{status_id}"
        else:
            if not url:
                return None
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            external_id = f"x_{url_hash}"

        # 3. Extract Author handle or display name
        author = "Anonymous"
        if username and username.lower() not in ("i", "status", "intent", "search"):
            author = f"@{username}"
        elif metadata.get("author"):
            author = str(metadata["author"])
        elif metadata.get("ogTitle"):
            # Often formatted as "Name on X: '...'"
            og = str(metadata["ogTitle"])
            if " on X:" in og:
                author = og.split(" on X:")[0].strip()
            elif " on Twitter:" in og:
                author = og.split(" on Twitter:")[0].strip()

        # 4. Extract Content (tweet text)
        content_text = markdown.strip()
        if not content_text:
            content_text = item.get("description") or metadata.get("description") or title

        if not content_text:
            return None

        # 5. Extract published_at from metadata (never substitute ingestion time)
        raw_published = (
            metadata.get("article:published_time")
            or metadata.get("publishedTime")
            or metadata.get("date")
            or metadata.get("pubdate")
        )
        published_at = _parse_published_time(raw_published)

        # 6. Extract Engagement Metrics (likes, retweets, replies)
        likes = 0
        retweets = 0
        replies = 0

        likes_match = _LIKES_REGEX.search(markdown)
        if likes_match:
            try:
                likes = int(likes_match.group("likes"))
            except ValueError:
                likes = 0

        rt_match = _RETWEETS_REGEX.search(markdown)
        if rt_match:
            try:
                retweets = int(rt_match.group("retweets"))
            except ValueError:
                retweets = 0

        rep_match = _REPLIES_REGEX.search(markdown)
        if rep_match:
            try:
                replies = int(rep_match.group("replies"))
            except ValueError:
                replies = 0

        engagement = {
            "likes": likes,
            "shares": retweets,
            "comments": replies,
        }

        # 7. Build custom metadata dictionary
        mention_meta = {
            "username": username,
            "status_id": status_id,
            "provider": "firecrawl",
            "source_type": "post",
        }

        return RawMentionRecord(
            platform="X",
            external_id=external_id,
            source_url=url,
            title=None,
            content=content_text,
            author=author,
            published_at=published_at,
            rating=None,
            engagement=engagement,
            metadata=mention_meta,
            raw_payload=item,
        )
