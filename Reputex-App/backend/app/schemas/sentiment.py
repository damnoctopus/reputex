"""Sentiment and Aspect analysis Pydantic schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SentimentAnalysisSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sentiment: str
    confidence: float
    positive_score: float = 0.0
    neutral_score: float = 0.0
    negative_score: float = 0.0
    emotions: dict[str, float] = Field(default_factory=dict)
    analyzed_at: datetime | None = None


class AspectSentimentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    aspect: str
    sentiment: str
    confidence: float = 0.8
    positive_percentage: float = 0.0
    negative_percentage: float = 0.0
    neutral_percentage: float = 0.0
    sample_count: int = 0
