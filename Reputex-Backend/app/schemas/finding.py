"""Finding and FindingEvidence Pydantic schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FindingEvidenceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    finding_id: str
    mention_id: str
    evidence_type: str = "review"
    snippet: str | None = None
    relevance_score: float = 1.0
    created_at: datetime


class FindingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    finding_type: str
    severity: str
    confidence: float
    score: float
    title: str
    description: str
    detected_at: datetime
    first_seen_at: datetime
    last_seen_at: datetime
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    evidence: list[FindingEvidenceSchema] = Field(default_factory=list)
    created_at: datetime


class FindingsListResponse(BaseModel):
    items: list[FindingSchema]
    total_count: int
