"""Business and BrandKeyword schemas matching Flutter contract."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class BrandKeywordCreate(BaseModel):
    keyword: str
    category: str = "brand"


class BrandKeywordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    keyword: str
    category: str = "brand"
    is_active: bool = True
    business_id: Optional[str] = None


class BusinessSetupRequest(BaseModel):
    name: str
    category: str
    website: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    platforms: List[str] = Field(default_factory=list)


class BusinessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    category: str
    website: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    monitored_platforms: List[str] = Field(default_factory=list)
    keywords: List[BrandKeywordResponse] = Field(default_factory=list)
    owner_id: Optional[str] = None
    created_at: Optional[datetime] = None
