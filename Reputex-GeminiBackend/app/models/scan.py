"""Scan model tracking state machine and progress for asynchronous scanning."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, utc_now


class Scan(Base, UUIDMixin):
    __tablename__ = "scans"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    # State Machine: PENDING -> RUNNING -> ACQUIRING -> ANALYZING -> AGGREGATING -> COMPLETED (or FAILED, PARTIAL, CANCELLED)
    status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True, nullable=False)
    current_step: Mapped[str] = mapped_column(String(100), default="Queued", nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    google_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    reddit_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    x_status: Mapped[str] = mapped_column(String(32), default="PENDING", nullable=False)
    mentions_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mentions_added: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress_pct: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
