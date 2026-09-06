"""Scan triggering and status response schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ScanTriggerResponse(BaseModel):
    business_id: str
    status: str = "triggered"
    task_id: str | None = None
    message: str = "Scan initiated across all platforms"


class ScanStatusResponse(BaseModel):
    business_id: str
    status: str
    active_platforms: list[str] = Field(default_factory=list)
    jobs: list[dict[str, Any]] = Field(default_factory=list)
    issues_count: int = 0
    findings_count: int = 0
    reputation_score: float | None = None
    last_scanned_at: datetime | None = None
