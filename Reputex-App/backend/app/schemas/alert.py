"""Alert Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class AlertItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    type: str
    title: str
    message: str
    severity: str = "medium"
    timestamp: datetime
    is_read: bool = False
    reference_id: str | None = None
    reference_type: str | None = None

    @model_validator(mode="before")
    @classmethod
    def populate_timestamp(cls, data: any) -> any:
        if hasattr(data, "created_at") and not hasattr(data, "timestamp"):
            # ORM instance
            return {
                "id": data.id,
                "type": data.type,
                "title": data.title,
                "message": data.message,
                "severity": data.severity,
                "timestamp": data.created_at,
                "is_read": data.is_read,
                "reference_id": data.reference_id,
                "reference_type": data.reference_type,
            }
        elif isinstance(data, dict) and "created_at" in data and "timestamp" not in data:
            data["timestamp"] = data["created_at"]
        return data
