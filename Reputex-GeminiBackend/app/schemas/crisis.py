"""Crisis schemas matching Flutter CrisisEvent model."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class CrisisEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    severity: str
    status: str = "active"
    trigger_reason: str
    velocity: float = 0.0
    negative_mentions_count: int = 0
    affected_platforms: List[str] = Field(default_factory=list)
    started_at: datetime
    resolved_at: Optional[datetime] = None
    suggested_actions: List[str] = Field(default_factory=list)
    estimated_reach: int = 0
    peak_volume_per_hour: int = 0


class CrisisEventListResponse(BaseModel):
    items: List[CrisisEventResponse]
    total: int = 0
