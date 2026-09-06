"""Crisis Event Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CrisisEventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    severity: str = "medium"
    status: str = "active"
    trigger_reason: str
    velocity: float = 0.0
    negative_mentions_count: int = 0
    affected_platforms: list[str] = Field(default_factory=list)
    started_at: datetime
    resolved_at: datetime | None = None
    suggested_actions: list[str] = Field(default_factory=list)
    estimated_reach: int = 0
    peak_volume_per_hour: int = 0


class CrisisEventUpdateSchema(BaseModel):
    status: str | None = None
    resolved_at: datetime | None = None
    suggested_actions: list[str] | None = None
