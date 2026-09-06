"""Finding schemas matching Flutter FindingItem and FindingEvidenceItem models."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class FindingEvidenceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    finding_id: str
    mention_id: str
    evidence_type: str = "review"
    snippet: Optional[str] = None
    relevance_score: float = 1.0
    created_at: datetime


class FindingItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    finding_type: str
    severity: str = "medium"
    confidence: float = 0.8
    score: float = 0.0
    title: str
    description: str
    detected_at: datetime
    first_seen_at: datetime
    last_seen_at: datetime
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    evidence: List[FindingEvidenceItemResponse] = Field(default_factory=list)


class FindingsListResponse(BaseModel):
    items: List[FindingItemResponse]
    total: int = 0
