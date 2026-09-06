"""Crisis Monitoring API endpoints matching Flutter RealApiService and OpenAPI specs."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.crisis import CrisisEventSchema, CrisisEventUpdateSchema
from app.services.crisis_service import CrisisService

router = APIRouter(prefix="/crisis", tags=["Crisis Monitoring"])


@router.get("", response_model=list[CrisisEventSchema])
async def get_crisis_events(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all crisis events for the active business."""
    service = CrisisService(db)
    return await service.get_crisis_events(current_user_id)


@router.get("/active", response_model=Optional[CrisisEventSchema])
async def get_active_crisis(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve the currently active crisis event, if any."""
    service = CrisisService(db)
    return await service.get_active_crisis(current_user_id)


@router.get("/{id}", response_model=CrisisEventSchema)
async def get_crisis_by_id(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve details for a specific crisis event."""
    service = CrisisService(db)
    return await service.get_crisis_by_id(current_user_id, id)


@router.post("/analyze", response_model=Optional[CrisisEventSchema])
async def analyze_crisis(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Evaluate recent reviews for anomalous velocity surges and crisis triggers."""
    service = CrisisService(db)
    return await service.analyze_and_detect(current_user_id)


@router.patch("/{id}", response_model=CrisisEventSchema)
async def update_crisis(
    id: str,
    update_data: CrisisEventUpdateSchema,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update crisis event status, resolution, or actions taken."""
    service = CrisisService(db)
    return await service.update_crisis(current_user_id, id, update_data)
