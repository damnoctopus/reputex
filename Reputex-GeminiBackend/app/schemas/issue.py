"""CustomerIssue schemas matching Flutter CustomerIssue and IssueEvidence models."""
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class IssueEvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mention_id: str
    relevance_score: float = 1.0
    excerpt: Optional[str] = None
    created_at: datetime


class CustomerIssueResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    category: str
    subtopic: str
    severity: str = "medium"
    status: str = "emerging"
    mention_count: int = 0
    platforms_breakdown: Dict[str, int] = Field(default_factory=dict)
    sentiment_breakdown: Dict[str, int] = Field(default_factory=dict)
    first_seen_at: datetime
    last_seen_at: datetime
    evidence: List[IssueEvidenceResponse] = Field(default_factory=list)


class CustomerIssuesListResponse(BaseModel):
    items: List[CustomerIssueResponse]
    total: int = 0
