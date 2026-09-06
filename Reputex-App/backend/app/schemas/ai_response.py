"""AI Response Studio Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResponseDraftSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    mention_id: str
    original_review: str
    generated_response: str
    tone: str = "empathetic"
    status: str = "drafted"
    created_at: datetime
    approved_at: datetime | None = None
    dispatched_at: datetime | None = None


class GenerateResponseRequest(BaseModel):
    mention_id: str
    tone: str = Field(default="empathetic")
    custom_instructions: str | None = None


class ApproveResponseRequest(BaseModel):
    response_text: str


class UpdateResponseRequest(BaseModel):
    response_text: str | None = None
    tone: str | None = None
