"""Issue and IssueMention SQLAlchemy ORM models for customer problem discovery."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def generate_issue_id() -> str:
    return f"iss_{uuid.uuid4().hex[:16]}"


def generate_issue_mention_id() -> str:
    return f"ism_{uuid.uuid4().hex[:16]}"


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_issue_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    subtopic: Mapped[str] = mapped_column(String(128), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), default="emerging", nullable=False, index=True)
    mention_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    platforms_breakdown: Mapped[dict[str, int]] = mapped_column(JSON, default=dict, nullable=False)
    sentiment_breakdown: Mapped[dict[str, int]] = mapped_column(JSON, default=dict, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relationships
    evidence: Mapped[list["IssueMention"]] = relationship(
        "IssueMention", back_populates="issue", cascade="all, delete-orphan", lazy="selectin"
    )


class IssueMention(Base):
    __tablename__ = "issue_mentions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_issue_mention_id)
    issue_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("issues.id", ondelete="CASCADE"), nullable=False, index=True
    )
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    relevance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    issue: Mapped["Issue"] = relationship("Issue", back_populates="evidence")
