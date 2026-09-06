"""Business and BrandKeyword Pydantic schemas matching Flutter domain models."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BrandKeywordSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    keyword: str
    category: str = "brand"
    is_active: bool = True
    business_id: str | None = None


class BrandKeywordCreate(BaseModel):
    keyword: str = Field(min_length=1)
    category: str = "brand"


class BusinessSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    category: str
    description: str | None = None
    website: str | None = None
    location: str | None = None
    phone: str | None = None
    logo_url: str | None = None
    monitored_platforms: list[str] = Field(default_factory=list)
    keywords: list[BrandKeywordSchema] = Field(default_factory=list)
    owner_id: str | None = None
    created_at: datetime | None = None


class BusinessSetupRequest(BaseModel):
    name: str = Field(min_length=1)
    category: str = Field(default="Restaurant")
    website: str | None = None
    location: str | None = None
    phone: str | None = None
    keywords: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)


class BusinessCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    category: str
    description: str | None = None
    website: str | None = None
    location: str | None = None
    phone: str | None = None


class BusinessUpdateRequest(BaseModel):
    name: str | None = None
    category: str | None = None
    description: str | None = None
    website: str | None = None
    location: str | None = None
    phone: str | None = None
    monitored_platforms: list[str] | None = None
