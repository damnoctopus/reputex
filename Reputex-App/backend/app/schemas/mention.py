"""Mention Pydantic schemas matching Flutter domain models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MentionEngagementSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    likes: int = 0
    shares: int = 0
    comments: int = 0


class MentionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    platform: str
    author: str
    content: str
    sentiment: str = "neutral"
    sentiment_score: float = 0.0
    is_fake: bool = False
    fraud_confidence: float | None = None
    url: str | None = None
    timestamp: datetime
    engagement: MentionEngagementSchema = Field(default_factory=MentionEngagementSchema)
    rating: float | None = None
    response_status: str = "none"
    response_text: str | None = None
    author_avatar: str | None = None

    @model_validator(mode="before")
    @classmethod
    def map_published_at_to_timestamp(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "timestamp" not in data and "published_at" in data:
                data["timestamp"] = data["published_at"]
            return data
        # Handle ORM model instance
        if hasattr(data, "published_at") and not hasattr(data, "timestamp"):
            # Set virtual attribute for pydantic extraction
            data.timestamp = data.published_at
        return data


class PaginatedMentionsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[MentionSchema] = Field(default_factory=list)
    total_count: int = 0
    page: int = 1
    total_pages: int = 1
    has_more: bool = False


class MentionsFilterParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    platform: str | None = None
    sentiment: str | None = None
    is_fake: bool | None = None
    q: str | None = None
    sort_by: str = Field(default="newest")


class MentionCreateRequest(BaseModel):
    platform: str
    author: str
    content: str
    rating: float | None = None
    url: str | None = None
    sentiment: str = "neutral"
    sentiment_score: float = 0.0
    is_fake: bool = False
    fraud_confidence: float | None = None
    engagement: dict[str, int] = Field(default_factory=lambda: {"likes": 0, "shares": 0, "comments": 0})
    author_avatar: str | None = None
    published_at: datetime | None = None
