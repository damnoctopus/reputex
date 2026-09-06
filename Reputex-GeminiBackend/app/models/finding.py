"""Finding and FindingEvidence models answering 'Why did RepuTex say this?'."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, utc_now


class Finding(Base, UUIDMixin):
    __tablename__ = "findings"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    finding_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # ISSUE, SUSPICIOUS_REVIEW, MANIPULATION_CLUSTER, CRISIS, REPUTATION_CHANGE
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    evidence: Mapped[List["FindingEvidence"]] = relationship("FindingEvidence", back_populates="finding", cascade="all, delete-orphan")


class FindingEvidence(Base, UUIDMixin):
    __tablename__ = "finding_evidences"

    finding_id: Mapped[str] = mapped_column(String(36), ForeignKey("findings.id", ondelete="CASCADE"), index=True, nullable=False)
    mention_id: Mapped[str] = mapped_column(String(36), ForeignKey("mentions.id", ondelete="CASCADE"), index=True, nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), default="review", nullable=False)
    snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    relevance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    finding: Mapped["Finding"] = relationship("Finding", back_populates="evidence")
