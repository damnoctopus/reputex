"""Business management API endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.business import (
    BusinessSchema,
    BusinessSetupRequest,
    BusinessUpdateRequest,
)
from app.services.business_service import BusinessService

router = APIRouter(tags=["Business"])


# ── Active Business Endpoints (Matched with Flutter RealApiService) ──
@router.get(
    "/business",
    response_model=Optional[BusinessSchema],
    status_code=status.HTTP_200_OK,
    summary="Get the currently active business for the authenticated user",
)
async def get_active_business(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.get_active_business(current_user_id)


@router.post(
    "/business",
    response_model=BusinessSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Setup or configure business during onboarding wizard",
)
async def setup_business(
    req: BusinessSetupRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.setup_business(current_user_id, req)


# ── Standard CRUD Endpoints ──
@router.get(
    "/businesses",
    response_model=list[BusinessSchema],
    status_code=status.HTTP_200_OK,
    summary="List all businesses owned or accessible by user",
)
async def list_businesses(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.list_businesses(current_user_id)


@router.get(
    "/businesses/{id}",
    response_model=BusinessSchema,
    status_code=status.HTTP_200_OK,
    summary="Get business details by ID",
)
async def get_business_by_id(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.get_business_by_id(current_user_id, id)


@router.put(
    "/businesses/{id}",
    response_model=BusinessSchema,
    status_code=status.HTTP_200_OK,
    summary="Update business profile metadata",
)
async def update_business(
    id: str,
    req: BusinessUpdateRequest,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    return await service.update_business(current_user_id, id, req)


@router.delete(
    "/businesses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete business profile (Owner only)",
)
async def delete_business(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    await service.delete_business(current_user_id, id)
