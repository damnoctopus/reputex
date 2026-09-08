"""Pydantic schemas for structured Gemini semantic intelligence with batching support."""
from typing import List, Optional
from pydantic import BaseModel, Field


class GeminiLinguisticSignals(BaseModel):
    templated_language: float = Field(default=0.0, ge=0.0, le=1.0)
    excessive_superlatives: float = Field(default=0.0, ge=0.0, le=1.0)
    operational_detail: float = Field(default=0.5, ge=0.0, le=1.0)
    unusual_patterns: float = Field(default=0.0, ge=0.0, le=1.0)


class GeminiIssueItem(BaseModel):
    category: str = Field(description="General category e.g. Customer Service, Billing, Food Quality, Wait Times, Cleanliness")
    subtopic: str = Field(description="Specific subtopic e.g. Rude Staff, Hidden Surcharge, Cold Food, Slow Service")
    severity: str = Field(default="medium", description="low, medium, high, critical")
    excerpt: Optional[str] = Field(default=None, description="Direct verbatim quote from mention supporting this issue")


class GeminiAspectItem(BaseModel):
    aspect: str = Field(description="Service, Food, Price, Atmosphere, Cleanliness, Delivery")
    sentiment: str = Field(default="neutral", description="positive, neutral, negative")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)


class GeminiMentionAnalysis(BaseModel):
    mention_index: int = Field(default=0, description="Index of the mention in the provided batch")
    sentiment_label: str = Field(default="neutral", description="positive, neutral, negative")
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    sentiment_score: float = Field(default=0.0, ge=-1.0, le=1.0, description="-1.0 to 1.0")
    intent: str = Field(default="feedback", description="complaint, praise, inquiry, recommendation, neutral_feedback")
    issues: List[GeminiIssueItem] = Field(default_factory=list)
    aspects: List[GeminiAspectItem] = Field(default_factory=list)
    linguistic_signals: GeminiLinguisticSignals = Field(default_factory=GeminiLinguisticSignals)
    summary: str = Field(default="", description="Concise one-sentence summary of the mention")


class GeminiBatchMentionAnalysis(BaseModel):
    analyses: List[GeminiMentionAnalysis] = Field(default_factory=list)


class GeminiDeteriorationResponse(BaseModel):
    deterioration_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated probability of near-term reputation deterioration (0.0 to 1.0)",
    )
    risk_level: str = Field(
        ...,
        description="LOW, MODERATE, HIGH, or CRITICAL",
    )
    is_sustained_decline: bool = Field(
        ...,
        description="True if feedback reflects a systemic trend, False if it is an isolated, temporary blip",
    )
    confidence: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0",
    )
    key_drivers: List[str] = Field(
        default_factory=list,
        description="Main factors contributing to this deterioration risk",
    )
    converging_complaints: List[str] = Field(
        default_factory=list,
        description="Specific recurring complaint topics emerging across reviews",
    )
    expert_opinion: str = Field(
        ...,
        description="Analytical reasoning and qualitative opinion from Gemini",
    )
    recommended_actions: List[str] = Field(
        default_factory=list,
        description="Recommended proactive mitigation actions",
    )
