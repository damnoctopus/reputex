"""Mentions endpoints matching Flutter MentionsRepository."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.mention import MentionEngagement, MentionResponse, PaginatedMentions
from app.services.mention_service import MentionService

router = APIRouter(prefix="/mentions", tags=["Mentions"])


@router.get("", response_model=PaginatedMentions)
async def get_mentions(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    platform: Optional[str] = None,
    sentiment: Optional[str] = None,
    is_fake: Optional[bool] = None,
    q: Optional[str] = None,
    sort_by: str = "latest",
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await MentionService.get_paginated(
        db,
        business_id=biz.id,
        page=page,
        limit=limit,
        platform=platform,
        sentiment=sentiment,
        is_fake=is_fake,
        q=q,
        sort_by=sort_by,
    )


@router.get("/{id}", response_model=MentionResponse)
async def get_mention_by_id(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    m = await MentionService.get_by_id(db, biz.id, id)
    return MentionResponse(
        id=m.id,
        platform=m.platform,
        author=m.author,
        content=m.content,
        sentiment=m.sentiment,
        sentiment_score=m.sentiment_score,
        is_fake=m.is_fake,
        fraud_confidence=m.fraud_confidence,
        url=m.url,
        timestamp=m.published_at,
        engagement=MentionEngagement(**(m.engagement or {})),
        rating=m.rating,
        response_status=m.response_status,
        response_text=m.response_text,
        author_avatar=m.author_avatar,
    )
