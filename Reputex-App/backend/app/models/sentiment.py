"""Sentiment and Aspect Analysis SQLAlchemy ORM models."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_sentiment_id() -> str:
    return f"snt_{uuid.uuid4().hex[:16]}"


def generate_aspect_id() -> str:
    return f"asp_{uuid.uuid4().hex[:16]}"


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_sentiment_id)
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    sentiment: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    positive_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    neutral_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    negative_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    emotions: Mapped[dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )


class MentionAspect(Base):
    __tablename__ = "mention_aspects"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_aspect_id)
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    aspect: Mapped[str] = mapped_column(String(64), nullable=False)
    sentiment: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
