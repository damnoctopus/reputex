"""AI Response Draft SQLAlchemy ORM model matching Flutter domain specifications."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def generate_response_id() -> str:
    return f"resp_{uuid.uuid4().hex[:16]}"


class AIResponse(Base):
    __tablename__ = "ai_responses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_response_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    mention_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("mentions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    original_review: Mapped[str] = mapped_column(Text, nullable=False)
    generated_response: Mapped[str] = mapped_column(Text, nullable=False)
    tone: Mapped[str] = mapped_column(String(32), default="empathetic", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="drafted", nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False, index=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
