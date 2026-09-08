"""Pydantic schemas for Future Reputation Deterioration Assessment.

Inspired by the research question from TTRF-Net:
"Is a run of bad reviews just a blip or the start of a sustained reputation decline?"
Gemini provides an expert opinion on near-term reputation deterioration probability,
differentiating between temporary noise and systemic decline.
"""
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class DeteriorationAssessment(BaseModel):
    business_id: str
    business_name: str
    deterioration_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated probability (0.0 to 1.0) of near-term reputation deterioration in the coming weeks",
    )
    risk_level: str = Field(
        ...,
        description="Categorical risk level: LOW (<0.35), MODERATE (0.35-0.60), HIGH (0.60-0.80), CRITICAL (>0.80)",
    )
    is_sustained_decline: bool = Field(
        ...,
        description="True if feedback reflects a systemic trend, False if it is an isolated, temporary blip",
    )
    confidence: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Gemini confidence in the assessment",
    )
    key_drivers: List[str] = Field(
        default_factory=list,
        description="Top warning signs / factors driving the assessment",
    )
    converging_complaints: List[str] = Field(
        default_factory=list,
        description="Specific themes or complaint areas customers are converging around",
    )
    expert_opinion: str = Field(
        ...,
        description="Detailed analytical assessment and reasoning from Gemini",
    )
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Immediate proactive mitigation steps for the business owner",
    )
    evaluated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp of evaluation",
    )
    horizon_days: int = Field(
        default=14,
        description="Prediction horizon in days (e.g. 7 or 14 days)",
    )
