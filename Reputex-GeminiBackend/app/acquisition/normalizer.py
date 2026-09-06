"""Content normalization, platform inference, and cryptographic deduplication hashing."""
import hashlib
import re
from datetime import datetime, timezone
from typing import Optional
from app.acquisition.base import RawMentionRecord
from app.models.mention import Mention


class Normalizer:
    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Normalize whitespace and strip control characters
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def compute_content_hash(platform: str, author: str, content: str) -> str:
        normalized_content = Normalizer.clean_text(content).lower()
        key = f"{platform.lower()}:{author.lower()}:{normalized_content}"
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @staticmethod
    def infer_platform_from_url(url: Optional[str]) -> str:
        if not url:
            return "web"
        url_lower = url.lower()
        if "reddit.com" in url_lower or "redd.it" in url_lower:
            return "reddit"
        elif "twitter.com" in url_lower or "x.com" in url_lower:
            return "twitter"
        elif "google.com" in url_lower or "maps.google" in url_lower or "goo.gl" in url_lower:
            return "google"
        return "web"

    @staticmethod
    def to_mention_model(record: RawMentionRecord, business_id: str) -> Mention:
        cleaned_content = Normalizer.clean_text(record.content)
        content_hash = Normalizer.compute_content_hash(
            platform=record.platform,
            author=record.author,
            content=cleaned_content,
        )

        return Mention(
            business_id=business_id,
            platform=record.platform.lower(),
            external_id=str(record.external_id),
            author=record.author or "Anonymous",
            author_avatar=record.author_avatar,
            content=cleaned_content,
            rating=record.rating,
            sentiment="neutral",
            sentiment_score=0.0,
            is_fake=False,
            url=record.source_url,
            published_at=record.published_at if record.published_at.tzinfo else record.published_at.replace(tzinfo=timezone.utc),
            ingested_at=datetime.now(timezone.utc),
            engagement=record.engagement or {},
            metadata_json=record.metadata or {},
            content_hash=content_hash,
            ai_status="PENDING",
        )
