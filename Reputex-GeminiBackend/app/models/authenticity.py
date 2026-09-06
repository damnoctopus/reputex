"""ReviewAuthenticityFinding and ManipulationCluster models."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, UUIDMixin, utc_now


class ReviewAuthenticityFinding(Base, UUIDMixin):
    __tablename__ = "review_authenticity_findings"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    mention_id: Mapped[str] = mapped_column(String(36), ForeignKey("mentions.id", ondelete="CASCADE"), index=True, nullable=False)
    suspicion_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="Potentially Suspicious", nullable=False)
    is_fraudulent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reasons: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    patterns: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    review_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    platform: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)


class ManipulationCluster(Base, UUIDMixin):
    __tablename__ = "manipulation_clusters"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    cluster_name: Mapped[str] = mapped_column(String(255), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), default="High Suspicion", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.85, nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    platforms: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    time_window_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
