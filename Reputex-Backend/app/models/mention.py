"""Mention SQLAlchemy ORM model matching Flutter domain schema."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_mention_id() -> str:
    return f"men_{uuid.uuid4().hex[:16]}"


class Mention(Base):
    __tablename__ = "mentions"
    __table_args__ = (UniqueConstraint("business_id", "platform", "external_id", name="uq_business_platform_external"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_mention_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    platform: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(
        String(255), nullable=False, default=lambda: f"manual_{uuid.uuid4().hex[:12]}"
    )
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    author: Mapped[str] = mapped_column(String(255), nullable=False)
    author_avatar: Mapped[str | None] = mapped_column(String(512), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    language: Mapped[str] = mapped_column(String(16), default="en", nullable=False)
    sentiment: Mapped[str] = mapped_column(String(32), default="neutral", nullable=False, index=True)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_fake: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    fraud_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    engagement: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=lambda: {"likes": 0, "shares": 0, "comments": 0}, nullable=False
    )
    response_status: Mapped[str] = mapped_column(String(32), default="none", nullable=False)
    response_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
