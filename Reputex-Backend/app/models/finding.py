"""Unified Finding and FindingEvidence SQLAlchemy ORM models."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def generate_finding_id() -> str:
    return f"fnd_{uuid.uuid4().hex[:16]}"


def generate_finding_evidence_id() -> str:
    return f"fne_{uuid.uuid4().hex[:16]}"


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_finding_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    finding_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    evidence: Mapped[list["FindingEvidence"]] = relationship(
        "FindingEvidence", back_populates="finding", cascade="all, delete-orphan", lazy="selectin"
    )


class FindingEvidence(Base):
    __tablename__ = "finding_evidence"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_finding_evidence_id)
    finding_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("findings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    evidence_type: Mapped[str] = mapped_column(String(32), default="review", nullable=False)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    relevance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    finding: Mapped["Finding"] = relationship("Finding", back_populates="evidence")
