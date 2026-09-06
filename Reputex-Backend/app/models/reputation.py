"""Reputation Score History SQLAlchemy ORM model."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_score_history_id() -> str:
    return f"rsh_{uuid.uuid4().hex[:16]}"


class ReputationScoreHistory(Base):
    __tablename__ = "reputation_score_history"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_score_history_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    current_score: Mapped[float] = mapped_column(Float, nullable=False)
    previous_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    change: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    trend: Mapped[str] = mapped_column(String(16), default="stable", nullable=False)
    components: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True
    )
