"""Business, BusinessMember, and BrandKeyword SQLAlchemy ORM models."""

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


def generate_business_id() -> str:
    return f"biz_{uuid.uuid4().hex[:16]}"


def generate_member_id() -> str:
    return f"mem_{uuid.uuid4().hex[:16]}"


def generate_keyword_id() -> str:
    return f"kw_{uuid.uuid4().hex[:16]}"


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_business_id)
    owner_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    monitored_platforms: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False
    )

    # Relationships
    members: Mapped[list["BusinessMember"]] = relationship(
        "BusinessMember", back_populates="business", cascade="all, delete-orphan"
    )
    keywords: Mapped[list["BrandKeyword"]] = relationship(
        "BrandKeyword", back_populates="business", cascade="all, delete-orphan"
    )


class BusinessMember(Base):
    __tablename__ = "business_members"
    __table_args__ = (UniqueConstraint("business_id", "user_id", name="uq_business_member"),)

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_member_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(32), default="owner", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    # Relationships
    business: Mapped["Business"] = relationship("Business", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="memberships")


class BrandKeyword(Base):
    __tablename__ = "brand_keywords"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=generate_keyword_id)
    business_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(64), default="brand", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )

    # Relationships
    business: Mapped["Business"] = relationship("Business", back_populates="keywords")
