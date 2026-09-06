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
    severity: str
    alert_type: str
    is_read: bool
    metadata_json: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
