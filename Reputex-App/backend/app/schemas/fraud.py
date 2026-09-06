"""Fraud Detection Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SuspiciousPatternSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pattern_name: str
    description: str
    severity: str = "medium"


class FraudResultSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mention_id: str
    is_fraudulent: bool
    confidence: float
    risk_level: str
    reasons: list[str] = Field(default_factory=list)
    patterns: list[SuspiciousPatternSchema] = Field(default_factory=list)
    review_content: str | None = None
    author: str | None = None
    platform: str | None = None
    timestamp: datetime | None = None
