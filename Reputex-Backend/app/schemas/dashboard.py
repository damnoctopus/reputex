"""Dashboard and Aggregated Analytics Pydantic schemas matching Flutter domain models."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.mention import MentionSchema


class ReputationScoreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_score: float
    previous_score: float | None = None
    change: float = 0.0
    trend: str = "stable"
    calculated_at: datetime | None = None


class SentimentDistributionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    positive: int = 0
    neutral: int = 0
    negative: int = 0
    total: int = 0
    positive_percentage: float = 0.0
    neutral_percentage: float = 0.0
    negative_percentage: float = 0.0


class SentimentTrendSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str
    positive: int = 0
    neutral: int = 0
    negative: int = 0
    score: float = 0.0


class PlatformStatisticsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    platform: str
    count: int = 0
    positive_percentage: float = 0.0
    negative_percentage: float = 0.0
    neutral_percentage: float = 0.0
    average_rating: float | None = None


class DashboardSummarySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reputation_score: ReputationScoreSchema
    sentiment_distribution: SentimentDistributionSchema
    total_mentions: int = 0
    crisis_active: bool = False
    crisis_count: int = 0
    crisis_risk_level: str = "Normal"
    pending_responses_count: int = 0
    fraud_alerts_count: int = 0
    suspicious_reviews_count: int = 0
    active_clusters_count: int = 0
    top_issues: list[dict[str, Any]] = Field(default_factory=list)
    recent_mentions: list[MentionSchema] = Field(default_factory=list)


class SentimentAnalyticsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    distribution: SentimentDistributionSchema
    trends: list[SentimentTrendSchema] = Field(default_factory=list)
    platform_breakdown: list[PlatformStatisticsSchema] = Field(default_factory=list)
    overall_score: float = 0.0
    total_reviews_analyzed: int = 0
