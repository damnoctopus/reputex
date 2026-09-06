"""Fraud detection analysis SQLAlchemy ORM model."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_fraud_id() -> str:
    return f"frd_{uuid.uuid4().hex[:16]}"


class FraudAnalysis(Base):
    __tablename__ = "fraud_analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_fraud_id)
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    is_fraudulent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(32), default="low", nullable=False, index=True)
    reasons: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    patterns: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
