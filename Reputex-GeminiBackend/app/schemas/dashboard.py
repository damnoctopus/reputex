"""Dashboard summary and analytics schemas matching Flutter models."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.schemas.mention import MentionResponse


class ReputationScore(BaseModel):
    current_score: float
    previous_score: Optional[float] = None
    change: float = 0.0
    trend: str = "stable"
    calculated_at: Optional[datetime] = None


class SentimentDistribution(BaseModel):
    positive: int = 0
    neutral: int = 0
    negative: int = 0
    total: int = 0
    positive_percentage: float = 0.0
    neutral_percentage: float = 0.0
    negative_percentage: float = 0.0


class PlatformStatistics(BaseModel):
    platform: str
    count: int = 0
    average_rating: float = 0.0
    positive_percentage: float = 0.0
    negative_percentage: float = 0.0


class SentimentTrend(BaseModel):
    date: str
    positive: int = 0
    neutral: int = 0
    negative: int = 0
    average_score: float = 0.0


class DashboardSummary(BaseModel):
    reputation_score: ReputationScore
    sentiment_distribution: SentimentDistribution
    total_mentions: int = 0
    crisis_active: bool = False
    crisis_count: int = 0
    pending_responses_count: int = 0
    fraud_alerts_count: int = 0
    crisis_risk_level: str = "Normal"
    suspicious_reviews_count: int = 0
    active_clusters_count: int = 0
    top_issues: List[Dict[str, Any]] = Field(default_factory=list)
    recent_mentions: List[MentionResponse] = Field(default_factory=list)
