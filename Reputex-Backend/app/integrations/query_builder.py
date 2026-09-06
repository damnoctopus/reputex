"""Platform-aware search query builder for RepuTex data acquisition."""

import re
from collections.abc import Sequence

from app.models.business import BrandKeyword
from app.schemas.ingestion import PlatformQuery


class PlatformQueryBuilder:
    """Constructs deterministic, syntax-compliant search queries tailored per external platform."""

    @staticmethod
    def _extract_clean_keywords(
        business_name: str,
        keywords: Sequence[BrandKeyword | str] | None = None,
        aliases: list[str] | None = None,
    ) -> list[str]:
        """Normalize, clean, and deduplicate keyword tokens deterministically."""
        cleaned_set: set[str] = set()
        ordered_list: list[str] = []

        def _add_token(token: str):
            # Normalize whitespace and strip special wrapper punctuation
            t = re.sub(r"\s+", " ", token.strip())
            if t and t.lower() not in cleaned_set:
                cleaned_set.add(t.lower())
                ordered_list.append(t)

        # Primary business name
        if business_name:
            _add_token(business_name)

        # Aliases
        if aliases:
            for a in aliases:
                _add_token(a)

        # Keyword items
        if keywords:
            for kw in keywords:
                val = kw.keyword if isinstance(kw, BrandKeyword) else str(kw)
                _add_token(val)

        return ordered_list

    @classmethod
    def build_query(
        cls,
        platform: str,
        business_name: str,
        keywords: Sequence[BrandKeyword | str] | None = None,
        location: str | None = None,
        aliases: list[str] | None = None,
    ) -> PlatformQuery:
        """Generate platform-specific boolean search query."""
        tokens = cls._extract_clean_keywords(business_name, keywords, aliases)
        if not tokens:
            tokens = [business_name or "Business"]

        norm_platform = platform.lower().strip()

        if norm_platform in ["google", "google_places", "google_maps"]:
            # Google search query: primary brand name + location + product terms
            primary = tokens[0]
            extra_terms = [t for t in tokens[1:4] if t.lower() != primary.lower()]
            parts = [f'"{primary}"']
            if location and location.strip():
                parts.append(location.strip())
            if extra_terms:
                parts.append(" ".join(extra_terms))
            query_str = " ".join(parts)
            return PlatformQuery(
                platform="Google",
                query_string=query_str,
                keywords_used=tokens,
                filters={"location": location} if location else {},
            )

        elif norm_platform in ["reddit"]:
            # Reddit search: ("Term 1" OR "Term 2")
            quoted = [f'"{t}"' if " " in t else t for t in tokens[:6]]
            bool_query = " OR ".join(quoted)
            if len(quoted) > 1:
                bool_query = f"({bool_query})"

            filters = {}
            if location and location.strip():
                # Extract city or clean token for subreddits
                city = location.split(",")[0].strip()
                filters["suggested_subreddit"] = f"r/{city.lower()}"

            return PlatformQuery(
                platform="Reddit",
                query_string=bool_query,
                keywords_used=tokens,
                filters=filters,
            )

        elif norm_platform in ["x", "twitter"]:
            # X API v2 syntax: ("Brand" OR "Alias") -is:retweet lang:en
            quoted = [f'"{t}"' if " " in t else t for t in tokens[:6]]
            bool_query = " OR ".join(quoted)
            if len(quoted) > 1:
                bool_query = f"({bool_query})"

            final_query = f"{bool_query} -is:retweet lang:en"
            return PlatformQuery(
                platform="X",
                query_string=final_query,
                keywords_used=tokens,
                filters={"lang": "en", "exclude_retweets": True},
            )

        elif norm_platform in [
            "google_ai_overview",
            "google ai overview",
            "google_ai",
            "google ai",
            "google_ai_summary",
            "google ai summary",
        ]:
            # Google AI Overview prompt / search phrase
            primary = tokens[0]
            loc_str = f" in {location.strip()}" if location and location.strip() else ""
            query_str = f'"{primary}"{loc_str} customer reviews and reputation'
            return PlatformQuery(
                platform="Google AI Overview",
                query_string=query_str,
                keywords_used=tokens,
                filters={"target": "ai_overview"},
            )

        else:
            # Generic fallback
            query_str = " OR ".join([f'"{t}"' if " " in t else t for t in tokens[:5]])
            return PlatformQuery(
                platform=platform,
                query_string=query_str,
                keywords_used=tokens,
                filters={},
            )
