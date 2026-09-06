"""Mentions and Reviews API endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.mention import (
    MentionCreateRequest,
    MentionSchema,
    MentionsFilterParams,
    PaginatedMentionsSchema,
)
from app.services.mention_service import MentionService

router = APIRouter(tags=["Mentions & Reviews"])


@router.get(
    "/mentions",
    response_model=PaginatedMentionsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get paginated mentions feed with multi-facet filters",
)
async def get_mentions(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    platform: str | None = Query(default=None),
    sentiment: str | None = Query(default=None),
    is_fake: bool | None = Query(default=None),
    q: str | None = Query(default=None),
    sort_by: str = Query(default="newest"),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    filter_params = MentionsFilterParams(
        page=page,
        limit=limit,
        platform=platform,
        sentiment=sentiment,
        is_fake=is_fake,
        q=q,
        sort_by=sort_by,
    )
    service = MentionService(db)
    return await service.get_paginated_mentions(current_user_id, filter_params)


@router.get(
    "/mentions/{id}",
    response_model=MentionSchema,
    status_code=status.HTTP_200_OK,
    summary="Get mention details by ID",
)
async def get_mention_by_id(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = MentionService(db)
    return await service.get_mention_by_id(current_user_id, id)


@router.post(
    "/mentions",
    response_model=MentionSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new mention or review record",
)
async def create_mention(
    req: MentionCreateRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = MentionService(db)
    return await service.create_mention(current_user_id, req)


# ── Reviews Endpoints (Mentions with rating >= 1.0) ──
@router.get(
    "/reviews",
    response_model=PaginatedMentionsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get paginated customer reviews feed (mentions with ratings)",
)
async def get_reviews(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    platform: str | None = Query(default=None),
    sentiment: str | None = Query(default=None),
    is_fake: bool | None = Query(default=None),
    q: str | None = Query(default=None),
    sort_by: str = Query(default="newest"),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    filter_params = MentionsFilterParams(
        page=page,
        limit=limit,
        platform=platform,
        sentiment=sentiment,
        is_fake=is_fake,
        q=q,
        sort_by=sort_by,
    )
    service = MentionService(db)
    return await service.get_paginated_mentions(current_user_id, filter_params, reviews_only=True)


@router.get(
    "/reviews/{id}",
    response_model=MentionSchema,
    status_code=status.HTTP_200_OK,
    summary="Get review details by ID",
)
async def get_review_by_id(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = MentionService(db)
    return await service.get_mention_by_id(current_user_id, id)
