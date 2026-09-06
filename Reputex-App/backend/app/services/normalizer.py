"""Mention Normalization Pipeline transforming raw external records into clean domain models."""

import hashlib
import re
from datetime import UTC, datetime
from typing import Any

from app.core.logging import logger
from app.schemas.ingestion import NormalizedMention, RawMentionRecord


class NormalizationError(Exception):
    """Raised when a raw record cannot be normalized into a valid mention."""

    pass


class MentionNormalizer:
    """Sanitizes, validates, and normalizes disparate raw platform feeds into standard mentions."""

    PLATFORM_NAME_MAP = {
        "google": "Google",
        "google_places": "Google",
        "google_maps": "Google",
        "google maps": "Google",
        "reddit": "Reddit",
        "twitter": "X",
        "x": "X",
        "google_ai_overview": "Google AI Overview",
        "google ai overview": "Google AI Overview",
        "google ai summary": "Google AI Overview",
    }

    @classmethod
    def normalize_platform_name(cls, raw_platform: str) -> str:
        key = raw_platform.strip().lower()
        return cls.PLATFORM_NAME_MAP.get(key, raw_platform.strip().capitalize())

    @staticmethod
    def normalize_content(raw_text: str) -> str:
        """Strip control characters, collapse excess whitespace, and ensure minimum length."""
        if not raw_text:
            raise NormalizationError("Record content cannot be empty.")
        # Remove null bytes and non-printable control chars
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", raw_text)
        # Normalize line breaks and trim per line
        cleaned = re.sub(r"\r\n|\r", "\n", cleaned)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in cleaned.split("\n")]
        cleaned = "\n".join(lines)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
        if not cleaned:
            raise NormalizationError("Cleaned record content resulted in empty text.")
        return cleaned

    @staticmethod
    def compute_content_hash(content: str) -> str:
        """Compute deterministic SHA-256 hash of normalized text."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def normalize_timestamp(dt: datetime | None) -> datetime:
        """Ensure datetime is UTC timezone-aware."""
        if dt is None:
            return datetime.now(UTC)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)

    @staticmethod
    def normalize_engagement(raw_eng: dict[str, Any] | None) -> dict[str, int]:
        """Ensure engagement contains integer values for likes, shares, comments."""
        if not isinstance(raw_eng, dict):
            return {"likes": 0, "shares": 0, "comments": 0}

        def _to_int(val: Any) -> int:
            try:
                return max(0, int(val))
            except (ValueError, TypeError):
                return 0

        return {
            "likes": _to_int(raw_eng.get("likes", raw_eng.get("upvotes", 0))),
            "shares": _to_int(raw_eng.get("shares", raw_eng.get("retweets", 0))),
            "comments": _to_int(raw_eng.get("comments", raw_eng.get("replies", 0))),
        }

    @staticmethod
    def normalize_rating(rating: float | None) -> float | None:
        """Clamp ratings between 1.0 and 5.0 rounded to 1 decimal place."""
        if rating is None:
            return None
        try:
            r = float(rating)
            return round(min(5.0, max(1.0, r)), 1)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def normalize_url(url: str | None) -> str | None:
        """Validate and clean URL."""
        if not url or not isinstance(url, str):
            return None
        cleaned = url.strip()
        if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
            return None
        return cleaned

    @classmethod
    def normalize_record(cls, raw: RawMentionRecord, business_id: str) -> NormalizedMention:
        """Transform a single RawMentionRecord into a NormalizedMention."""
        content = cls.normalize_content(raw.content)
        content_hash = cls.compute_content_hash(content)
        platform = cls.normalize_platform_name(raw.platform)

        # External ID resolution
        external_id = raw.external_id
        if not external_id or not str(external_id).strip():
            # Deterministic fallback ID based on platform and content hash
            external_id = f"{platform.lower().replace(' ', '_')}_{content_hash[:16]}"
        else:
            external_id = str(external_id).strip()

        # Author resolution
        author = (raw.author or "Anonymous").strip() or "Anonymous"

        # Build clean metadata combining raw metadata and audit trail
        clean_metadata = dict(raw.metadata or {})
        if raw.title:
            clean_metadata["source_title"] = raw.title.strip()
        if raw.author_id:
            clean_metadata["author_id"] = str(raw.author_id).strip()

        return NormalizedMention(
            business_id=business_id,
            platform=platform,
            external_id=external_id,
            content_hash=content_hash,
            author=author,
            author_avatar=cls.normalize_url(raw.author_avatar),
            content=content,
            url=cls.normalize_url(raw.source_url),
            rating=cls.normalize_rating(raw.rating),
            language="en",
            engagement=cls.normalize_engagement(raw.engagement),
            metadata_json=clean_metadata,
            published_at=cls.normalize_timestamp(raw.published_at),
            collected_at=cls.normalize_timestamp(raw.collected_at),
        )

    @classmethod
    def normalize_batch(
        cls, records: list[RawMentionRecord], business_id: str
    ) -> tuple[list[NormalizedMention], list[str]]:
        """Safely normalize a batch of raw records without failing on individual errors."""
        normalized: list[NormalizedMention] = []
        errors: list[str] = []

        for idx, rec in enumerate(records):
            try:
                norm = cls.normalize_record(rec, business_id)
                normalized.append(norm)
            except Exception as e:
                err_msg = f"Record #{idx} ({rec.platform}:{rec.external_id or 'unknown'}): {e}"
                logger.warning(f"Normalization failed for {err_msg}")
                errors.append(err_msg)

        return normalized, errors
