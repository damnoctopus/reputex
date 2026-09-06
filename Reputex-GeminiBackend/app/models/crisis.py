"""CrisisEvent model for real-time risk alerts and mitigation."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, utc_now


class CrisisEvent(Base, UUIDMixin):
    __tablename__ = "crisis_events"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="active", nullable=False)  # active, resolved, monitoring
    trigger_reason: Mapped[str] = mapped_column(Text, nullable=False)
    velocity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    negative_mentions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    affected_platforms: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    suggested_actions: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    estimated_reach: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    peak_volume_per_hour: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    drivers: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
