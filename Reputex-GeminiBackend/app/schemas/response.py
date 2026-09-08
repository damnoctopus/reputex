"""ResponseDraft and AlertItem schemas matching Flutter models."""
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field


class ResponseGenerateRequest(BaseModel):
    mention_id: str
    tone: str = "professional"
    custom_instructions: Optional[str] = None


class ResponseApproveRequest(BaseModel):
    response_text: str


class ResponseDraftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    mention_id: str
    response_text: str
    tone: str
    status: str
    created_at: datetime
    approved_at: Optional[datetime] = None
    dispatched_at: Optional[datetime] = None


class AlertItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    business_id: str
    title: str
    message: str
    severity: str = "medium"
    type: str = "system"
    alert_type: Optional[str] = None
    is_read: bool = False
    timestamp: datetime
    created_at: Optional[datetime] = None
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
