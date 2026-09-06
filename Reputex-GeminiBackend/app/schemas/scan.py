"""Scan status schemas with state machine progression."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ScanTriggerResponse(BaseModel):
    scan_id: str
    status: str
    message: str = "Scan initiated successfully"
    business_id: str


class ScanStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    scan_id: str
    business_id: str
    status: str  # PENDING, RUNNING, ACQUIRING, ANALYZING, AGGREGATING, COMPLETED, FAILED, PARTIAL, CANCELLED
    current_step: str
    google_status: str
    reddit_status: str
    x_status: str
    mentions_found: int
    mentions_added: int
    progress_pct: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_summary: Optional[str] = None
