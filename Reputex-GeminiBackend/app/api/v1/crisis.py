"""Crisis monitoring endpoints matching Flutter CrisisRepository."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.crisis import CrisisEventResponse
from app.services.crisis_service import CrisisService

router = APIRouter(prefix="/crisis", tags=["Crisis Monitoring"])


@router.get("", response_model=List[CrisisEventResponse])
async def get_crisis_events(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await CrisisService.get_crisis_events(db, biz.id)


@router.get("/active", response_model=Optional[CrisisEventResponse])
async def get_active_crisis(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await CrisisService.get_active_crisis(db, biz.id)


@router.get("/{id}", response_model=CrisisEventResponse)
async def get_crisis_by_id(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await CrisisService.get_crisis_by_id(db, biz.id, id)
