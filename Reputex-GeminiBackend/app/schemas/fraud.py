"""Fraud and authenticity schemas matching Flutter FraudResult and SuspiciousPattern."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SuspiciousPattern(BaseModel):
    pattern_name: str
    description: str
    severity: str = "medium"


class FraudResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mention_id: str
    is_fraudulent: bool = False
    confidence: float = 0.8
    risk_level: str = "Potentially Suspicious"
    reasons: List[str] = Field(default_factory=list)
    patterns: List[SuspiciousPattern] = Field(default_factory=list)
    review_content: Optional[str] = None
    author: Optional[str] = None
    platform: Optional[str] = None
    timestamp: Optional[datetime] = None


class FraudListResponse(BaseModel):
    items: List[FraudResult]
    total: int = 0
