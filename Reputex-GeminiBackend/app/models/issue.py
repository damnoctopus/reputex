"""CustomerIssue and IssueEvidence models."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, utc_now


class CustomerIssue(Base, UUIDMixin):
    __tablename__ = "customer_issues"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    subtopic: Mapped[str] = mapped_column(String(200), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="emerging", nullable=False)
    mention_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    platforms_breakdown: Mapped[Dict[str, int]] = mapped_column(JSON, default=dict, nullable=False)
    sentiment_breakdown: Mapped[Dict[str, int]] = mapped_column(JSON, default=dict, nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    evidence: Mapped[List["IssueEvidence"]] = relationship("IssueEvidence", back_populates="issue", cascade="all, delete-orphan")


class IssueEvidence(Base, UUIDMixin):
    __tablename__ = "issue_evidences"

    issue_id: Mapped[str] = mapped_column(String(36), ForeignKey("customer_issues.id", ondelete="CASCADE"), index=True, nullable=False)
    mention_id: Mapped[str] = mapped_column(String(36), ForeignKey("mentions.id", ondelete="CASCADE"), index=True, nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    excerpt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    issue: Mapped["CustomerIssue"] = relationship("CustomerIssue", back_populates="evidence")
