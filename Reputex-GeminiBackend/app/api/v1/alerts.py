"""Alerts notification endpoints matching Flutter Alerts repository."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.response import AlertItemResponse
from app.services.response_service import ResponseService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=List[AlertItemResponse])
async def get_alerts(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ResponseService.get_alerts(db, biz.id)


@router.put("/{id}/read")
async def mark_alert_as_read(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    await ResponseService.mark_alert_as_read(db, biz.id, id)
    return {"success": True}
