"""Mention schemas matching Flutter Mention and PaginatedMentions models."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MentionEngagement(BaseModel):
    likes: int = 0
    comments: int = 0
    shares: int = 0
    retweets: int = 0
    upvotes: int = 0
    downvotes: int = 0


class MentionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    platform: str
    author: str
    content: str
    sentiment: str
    sentiment_score: float = 0.0
    is_fake: bool = False
    fraud_confidence: Optional[float] = None
    url: Optional[str] = None
    timestamp: datetime = Field(description="Maps to published_at in backend")
    engagement: MentionEngagement = Field(default_factory=MentionEngagement)
    rating: Optional[float] = None
    response_status: str = "none"
    response_text: Optional[str] = None
    author_avatar: Optional[str] = None


class PaginatedMentions(BaseModel):
    items: List[MentionResponse]
    total: int
    page: int
    limit: int
    total_pages: int
