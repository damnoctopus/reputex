"""Raw and normalized domain schemas for data acquisition pipeline."""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RawMentionRecord(BaseModel):
    """Raw record emitted directly by platform connectors / scrapers."""

    model_config = ConfigDict(extra="ignore")

    platform: str
    external_id: str | None = None
    source_url: str | None = None
    title: str | None = None
    content: str
    author: str = "Anonymous"
    author_id: str | None = None
    author_avatar: str | None = None
    published_at: datetime | None = None
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    rating: float | None = None
    engagement: dict[str, Any] = Field(default_factory=lambda: {"likes": 0, "shares": 0, "comments": 0})
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_payload: dict[str, Any] = Field(default_factory=dict)


class NormalizedMention(BaseModel):
    """Cleaned, validated, and normalized mention ready for idempotent repository upsert."""

    model_config = ConfigDict(from_attributes=True)

    business_id: str
    platform: str
    external_id: str
    content_hash: str
    author: str
    author_avatar: str | None = None
    content: str
    url: str | None = None
    rating: float | None = None
    language: str = "en"
    engagement: dict[str, Any] = Field(default_factory=lambda: {"likes": 0, "shares": 0, "comments": 0})
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    published_at: datetime
    collected_at: datetime


class PlatformQuery(BaseModel):
    """Search query formulated for a specific external platform."""

    platform: str
    query_string: str
    keywords_used: list[str]
    filters: dict[str, Any] = Field(default_factory=dict)


class IngestionJobSchema(BaseModel):
    """Status and telemetry representation of an ingestion execution."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    platform: str
    status: str
    started_at: datetime
    completed_at: datetime | None = None
    records_fetched: int = 0
    records_normalized: int = 0
    records_inserted: int = 0
    records_skipped: int = 0
    error_message: str | None = None
    retry_count: int = 0
    created_at: datetime


class PlatformConnectionSchema(BaseModel):
    """Public representation of an active platform data connection."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    platform: str
    is_active: bool
    last_polled_at: datetime | None = None
    last_success_at: datetime | None = None
    status: str
    records_fetched: int = 0
    records_inserted: int = 0
    records_skipped: int = 0
    error_count: int = 0
    last_error: str | None = None
    cursor: str | None = None


class IngestionBatchResult(BaseModel):
    """Summary result returned by an ingestion run."""

    job_id: str
    business_id: str
    platform: str
    status: str
    records_fetched: int
    records_normalized: int
    records_inserted: int
    records_skipped: int
    errors: list[str] = Field(default_factory=list)
