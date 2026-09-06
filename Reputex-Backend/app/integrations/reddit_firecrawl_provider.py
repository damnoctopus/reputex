"""Primary Reddit acquisition provider using Firecrawl web search and extraction.

Implements the RedditProvider protocol by:
  1. Executing site-scoped Firecrawl searches for public Reddit discussions
  2. Extracting reliable submission and comment IDs from canonical Reddit URLs
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

# Regex matching standard Reddit submission and comment permalinks
_REDDIT_URL_REGEX = re.compile(
    r"reddit\.com/r/(?P<subreddit>[^/]+)/comments/(?P<post_id>[a-zA-Z0-9]+)(?:/[^/]+/?(?P<comment_id>[a-zA-Z0-9]+)?)?",
    re.IGNORECASE,
)

# Regex to detect author handle in text/markdown (e.g., "u/username" or "Posted by u/username")
_AUTHOR_REGEX = re.compile(r"(?:Posted by\s+)?u/(?P<author>[a-zA-Z0-9_-]+)", re.IGNORECASE)

# Regex to extract upvotes or score from markdown snippet
_SCORE_REGEX = re.compile(r"(?P<score>\d+)\s*(?:points|upvotes|votes)", re.IGNORECASE)

# Regex to extract comment count from markdown snippet
_COMMENTS_REGEX = re.compile(r"(?P<comments>\d+)\s*comments?", re.IGNORECASE)


def _parse_published_time(raw_time: Any) -> datetime | None:
    """Parse ISO 8601 or RFC date string into UTC datetime. Never returns current time."""
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


class RedditFirecrawlProvider:
    """Acquires public Reddit discussions and comments via Firecrawl."""

    def __init__(self, firecrawl_client: FirecrawlClient | None = None):
        self._client = firecrawl_client or FirecrawlClient()

    async def search_mentions(
        self,
        query: PlatformQuery,
        limit: int = 5,
        since: datetime | None = None,
        credentials: dict[str, Any] | None = None,
    ) -> list[RawMentionRecord]:
        """Search public Reddit content matching query via Firecrawl."""
        api_key = (credentials or {}).get("firecrawl_api_key")
        if not self._client.is_configured(api_key=api_key):
            logger.warning("RedditFirecrawlProvider: Firecrawl is not configured or disabled.")
            return []

        # Formulate search restricted to Reddit
        scoped_query = f"site:reddit.com {query.query_string.strip()}"
        logger.info(f"RedditFirecrawlProvider executing search: {scoped_query} (limit={limit})")

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
                # If since filter is provided and published_at is known, respect cutoff
                if since and record.published_at and record.published_at < since:
                    continue
                records.append(record)

        logger.info(f"RedditFirecrawlProvider extracted {len(records)} mentions.")
        return records

    def _parse_result_item(self, item: dict[str, Any]) -> RawMentionRecord | None:
        """Parse a single Firecrawl search result into a RawMentionRecord."""
        url = item.get("url") or ""
        markdown = item.get("markdown") or ""
        title = item.get("title") or ""
        metadata = item.get("metadata") or {}

        # 1. Parse URL to extract subreddit, post_id, comment_id
        match = _REDDIT_URL_REGEX.search(url)
        subreddit = match.group("subreddit") if match else "reddit"
        post_id = match.group("post_id") if match else None
        comment_id = match.group("comment_id") if match else None

        # 2. Derive stable external ID (never generate random UUID)
        if comment_id:
            external_id = f"reddit_c_{comment_id}"
            is_comment = True
        elif post_id:
            external_id = f"reddit_t3_{post_id}"
            is_comment = False
        else:
            # Deterministic fallback based on canonical URL hash
            if not url:
                return None
            url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
            external_id = f"reddit_{url_hash}"
            is_comment = False

        # 3. Extract Author
        author = "Anonymous"
        if metadata.get("author"):
            author = str(metadata["author"])
        elif metadata.get("article:author"):
            author = str(metadata["article:author"])
        else:
            author_match = _AUTHOR_REGEX.search(markdown)
            if author_match:
                author = f"u/{author_match.group('author')}"

        # 4. Extract Content (prefer markdown text body, fallback to description or title)
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

        # 6. Extract Engagement Metrics (upvotes / score / comments)
        likes = 0
        comments = 0
        score_match = _SCORE_REGEX.search(markdown)
        if score_match:
            try:
                likes = int(score_match.group("score"))
            except ValueError:
                likes = 0

        comments_match = _COMMENTS_REGEX.search(markdown)
        if comments_match:
            try:
                comments = int(comments_match.group("comments"))
            except ValueError:
                comments = 0

        engagement = {
            "likes": likes,
            "shares": 0,
            "comments": comments,
        }

        # 7. Build custom metadata dictionary
        mention_meta = {
            "subreddit": subreddit,
            "post_id": post_id,
            "comment_id": comment_id,
            "is_comment": is_comment,
            "provider": "firecrawl",
            "extracted_title": title,
        }

        return RawMentionRecord(
            platform="Reddit",
            external_id=external_id,
            source_url=url,
            title=title or None,
            content=content_text,
            author=author,
            published_at=published_at,
            rating=None,
            engagement=engagement,
            metadata=mention_meta,
            raw_payload=item,
        )
