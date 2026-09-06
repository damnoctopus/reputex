"""Issue and IssueMention Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IssueMentionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    issue_id: str
    mention_id: str
    relevance_score: float = 1.0
    excerpt: str | None = None
    created_at: datetime


class IssueSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    category: str
    subtopic: str
    severity: str
    status: str
    mention_count: int
    platforms_breakdown: dict[str, int] = Field(default_factory=dict)
    sentiment_breakdown: dict[str, int] = Field(default_factory=dict)
    first_seen_at: datetime
    last_seen_at: datetime
    evidence: list[IssueMentionSchema] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class IssuesListResponse(BaseModel):
    items: list[IssueSchema]
    total_count: int
