"""Primary web discovery provider using Gemini Google Search Grounding."""
import hashlib
from datetime import datetime, timezone
from typing import List, Optional
from app.acquisition.base import AcquisitionProvider, RawMentionRecord
from app.acquisition.normalizer import Normalizer
from app.acquisition.search_cache import SearchCache
from app.ai.gemini_client import GeminiClient
from app.core.config import settings


class GeminiSearchProvider(AcquisitionProvider):
    """Performs bounded Google Search Grounding to discover recent public Google, Reddit, and X mentions."""

    def __init__(self, client: Optional[GeminiClient] = None):
        self.client = client or GeminiClient()

    def acquire(
        self,
        business_name: str,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        last_scan_time: Optional[datetime] = None,
    ) -> List[RawMentionRecord]:
        # If mock mode is explicitly enabled or Gemini key is absent, use mock provider
        if settings.USE_MOCK_ACQUISITION or not self.client.is_available:
            from app.acquisition.mock_provider import MockAcquisitionProvider
            return MockAcquisitionProvider().acquire(business_name, location, keywords, last_scan_time)

        # Build bounded queries (max 3-4 to control costs)
        loc_str = f" {location}" if location else ""
        queries = [
            f"\"{business_name}\"{loc_str} reviews",
            f"\"{business_name}\"{loc_str} complaints customer service",
            f"\"{business_name}\" site:reddit.com",
            f"\"{business_name}\" (site:x.com OR site:twitter.com)",
        ]

        # Add top custom keyword if provided
        if keywords:
            top_kw = keywords[0]
            if top_kw.lower() not in queries[0].lower():
                queries.append(f"\"{business_name}\" {top_kw}")

        queries = queries[:settings.MAX_SEARCH_QUERIES_PER_SCAN]

        all_records: List[RawMentionRecord] = []
        seen_urls = set()

        for q in queries:
            # Check search cache first
            cached = SearchCache.get(business_name, q)
            if cached is not None:
                for rec in cached:
                    if rec.source_url and rec.source_url not in seen_urls:
                        seen_urls.add(rec.source_url)
                        all_records.append(rec)
                continue

            citations = self.client.search_with_grounding(
                query=q,
                business_name=business_name,
                location=location,
            )

            query_records: List[RawMentionRecord] = []
            for c in citations:
                url = c.get('url', '')
                if url in seen_urls:
                    continue
                seen_urls.add(url)

                snippet = c.get('snippet', '')
                if not snippet or len(snippet.strip()) < 10:
                    continue

                platform = Normalizer.infer_platform_from_url(url)
                # Generate deterministic external ID
                ext_id = hashlib.md5(url.encode('utf-8')).hexdigest()[:16]

                record = RawMentionRecord(
                    platform=platform,
                    external_id=ext_id,
                    content=snippet,
                    author="Public Web Contributor",
                    source_url=url,
                    published_at=datetime.now(timezone.utc),
                    engagement={"views": 10, "relevance": 1.0},
                    metadata={"query": q, "title": c.get('title', '')},
                    raw_payload=c,
                )
                query_records.append(record)
                all_records.append(record)

            SearchCache.set(business_name, q, query_records)

        if not all_records:
            from app.acquisition.mock_provider import MockAcquisitionProvider
            return MockAcquisitionProvider().acquire(business_name, location, keywords, last_scan_time)
        return all_records
