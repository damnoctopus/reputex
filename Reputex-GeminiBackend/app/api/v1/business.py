"""Business and Scan endpoints matching Flutter BusinessRepository and ScanService."""
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business, get_current_user_optional
from app.core.database import get_async_db
from app.models.business import Business
from app.models.user import User
from app.schemas.business import BusinessResponse, BusinessSetupRequest
from app.schemas.scan import ScanStatusResponse, ScanTriggerResponse
from app.services.business_service import BusinessService
from app.services.scan_service import ScanService

router = APIRouter(tags=["Business & Scan"])


@router.get("/business", response_model=BusinessResponse)
async def get_business(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    fresh_biz = await BusinessService.get_business_by_id(db, biz.id)
    return BusinessResponse.model_validate(fresh_biz)


@router.post("/business", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def setup_business(
    req: BusinessSetupRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_async_db),
):
    user_id = current_user.id if current_user else None
    biz = await BusinessService.setup_business(db, user_id, req)
    return BusinessResponse.model_validate(biz)


@router.post("/business/scan", response_model=ScanTriggerResponse)
async def trigger_business_scan(
    background_tasks: BackgroundTasks,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ScanService.trigger_scan(db, biz.id, background_tasks=background_tasks)


@router.get("/business/scan/status", response_model=ScanStatusResponse)
async def get_business_scan_status(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ScanService.get_scan_status(db, biz.id)


# REST parity aliases: /businesses and /businesses/{id}/scan
@router.post("/businesses", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def create_business_rest(
    req: BusinessSetupRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_async_db),
):
    user_id = current_user.id if current_user else None
    biz = await BusinessService.setup_business(db, user_id, req)
    return BusinessResponse.model_validate(biz)


@router.get("/businesses/{id}", response_model=BusinessResponse)
async def get_business_by_id(id: str, db: AsyncSession = Depends(get_async_db)):
    biz = await BusinessService.get_business_by_id(db, id)
    return BusinessResponse.model_validate(biz)


@router.post("/businesses/{id}/scan", response_model=ScanTriggerResponse)
async def trigger_scan_by_id(
    id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
):
    return await ScanService.trigger_scan(db, id, background_tasks=background_tasks)


@router.get("/businesses/{id}/scan/status", response_model=ScanStatusResponse)
async def get_scan_status_by_id(id: str, db: AsyncSession = Depends(get_async_db)):
    return await ScanService.get_scan_status(db, id)
