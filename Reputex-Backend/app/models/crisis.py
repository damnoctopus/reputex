"""Crisis Event SQLAlchemy ORM model matching Flutter domain specifications."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_crisis_id() -> str:
    return f"crs_{uuid.uuid4().hex[:16]}"


class CrisisEvent(Base):
    __tablename__ = "crisis_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_crisis_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False, index=True)
    trigger_reason: Mapped[str] = mapped_column(String(512), nullable=False)
    velocity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    negative_mentions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    affected_platforms: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    suggested_actions: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    estimated_reach: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    peak_volume_per_hour: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
