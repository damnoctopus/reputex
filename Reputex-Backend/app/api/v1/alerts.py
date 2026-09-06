"""Alerts API endpoints matching Flutter RealApiService and OpenAPI specs."""

from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.alert import AlertItemSchema
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertItemSchema])
async def get_alerts(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all alerts for the active business."""
    service = AlertService(db)
    return await service.get_alerts(current_user_id)


@router.put("/{id}/read", status_code=status.HTTP_200_OK)
async def mark_alert_read_put(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Mark a specific alert as read (PUT method used by Flutter client)."""
    service = AlertService(db)
    await service.mark_as_read(current_user_id, id)
    return {"success": True, "message": "Alert marked as read"}


@router.patch("/{id}/read", status_code=status.HTTP_200_OK)
async def mark_alert_read_patch(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Mark a specific alert as read (PATCH alias)."""
    service = AlertService(db)
    await service.mark_as_read(current_user_id, id)
    return {"success": True, "message": "Alert marked as read"}


@router.patch("/read-all", status_code=status.HTTP_200_OK)
async def mark_all_alerts_read(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Mark all unread alerts as read for the business."""
    service = AlertService(db)
    await service.mark_all_as_read(current_user_id)
    return {"success": True, "message": "All alerts marked as read"}
