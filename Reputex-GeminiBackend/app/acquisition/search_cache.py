"""Search-level caching to prevent repeated grounding requests for identical queries."""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from app.acquisition.base import RawMentionRecord
from app.core.config import settings


class SearchCache:
    _cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def _make_key(cls, business_name: str, query: str) -> str:
        norm = f"{business_name.strip().lower()}:{query.strip().lower()}"
        return hashlib.sha256(norm.encode('utf-8')).hexdigest()

    @classmethod
    def get(cls, business_name: str, query: str) -> Optional[List[RawMentionRecord]]:
        key = cls._make_key(business_name, query)
        entry = cls._cache.get(key)
        if not entry:
            return None
        expires_at = entry.get('expires_at')
        if expires_at and datetime.now(timezone.utc) > expires_at:
            del cls._cache[key]
            return None
        return entry.get('records')

    @classmethod
    def set(cls, business_name: str, query: str, records: List[RawMentionRecord]) -> None:
        key = cls._make_key(business_name, query)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=settings.SEARCH_CACHE_TTL_HOURS)
        cls._cache[key] = {
            'records': records,
            'expires_at': expires_at,
        }

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()
