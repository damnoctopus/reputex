"""Mention, SentimentAnalysis, and MentionAspect models."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, utc_now


class Mention(Base, UUIDMixin):
    __tablename__ = "mentions"

    business_id: Mapped[str] = mapped_column(String(36), ForeignKey("businesses.id", ondelete="CASCADE"), index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # google, reddit, twitter, web
    external_id: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), default="Anonymous", nullable=False)
    author_avatar: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(32), default="neutral", index=True, nullable=False)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_fake: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    fraud_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    engagement: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    ai_status: Mapped[str] = mapped_column(String(32), default="PENDING", index=True, nullable=False)
    response_status: Mapped[str] = mapped_column(String(32), default="none", nullable=False)
    response_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("business_id", "platform", "external_id", name="uq_mention_biz_plat_ext"),
    )

    sentiments: Mapped[List["SentimentAnalysis"]] = relationship("SentimentAnalysis", back_populates="mention", cascade="all, delete-orphan")
    aspects: Mapped[List["MentionAspect"]] = relationship("MentionAspect", back_populates="mention", cascade="all, delete-orphan")


class SentimentAnalysis(Base, UUIDMixin):
    __tablename__ = "sentiment_analyses"

    mention_id: Mapped[str] = mapped_column(String(36), ForeignKey("mentions.id", ondelete="CASCADE"), index=True, nullable=False)
    sentiment_label: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    compound_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    emotions: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    aspects: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    mention: Mapped["Mention"] = relationship("Mention", back_populates="sentiments")


class MentionAspect(Base, UUIDMixin):
    __tablename__ = "mention_aspects"

    mention_id: Mapped[str] = mapped_column(String(36), ForeignKey("mentions.id", ondelete="CASCADE"), index=True, nullable=False)
    aspect: Mapped[str] = mapped_column(String(100), nullable=False)
    sentiment: Mapped[str] = mapped_column(String(32), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    mention: Mapped["Mention"] = relationship("Mention", back_populates="aspects")
