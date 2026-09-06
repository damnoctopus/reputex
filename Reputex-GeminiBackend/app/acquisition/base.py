"""Base acquisition interfaces and data records."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RawMentionRecord(BaseModel):
    """Normalized representation of content acquired from any external source."""
    platform: str  # google, reddit, twitter, web
    external_id: str
    content: str
    author: str = "Anonymous"
    author_avatar: Optional[str] = None
    rating: Optional[float] = None
    source_url: Optional[str] = None
    published_at: datetime
    engagement: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    raw_payload: Dict[str, Any] = Field(default_factory=dict)


class AcquisitionProvider(ABC):
    @abstractmethod
    def acquire(
        self,
        business_name: str,
        location: Optional[str] = None,
        keywords: Optional[List[str]] = None,
        last_scan_time: Optional[datetime] = None,
    ) -> List[RawMentionRecord]:
        """Acquire recent public mentions for a business."""
        pass
