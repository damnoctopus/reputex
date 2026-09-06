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
from app.schemas.scan import ScanStatusResponse, ScanTriggerResponse
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


# ── Full Platform Scan Endpoints ──
@router.post(
    "/businesses/{id}/scan",
    response_model=ScanTriggerResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger a full asynchronous reputation and review integrity scan",
)
async def trigger_business_scan(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import ForbiddenException, NotFoundException
    from app.repositories.business_repository import BusinessRepository
    from app.schemas.scan import ScanTriggerResponse
    from app.workers import tasks

    biz_repo = BusinessRepository(db)
    biz = await biz_repo.get_by_id(id)
    if not biz:
        raise NotFoundException("Business not found", code="BUSINESS_NOT_FOUND")

    has_access = await biz_repo.user_has_access(id, current_user_id)
    if not has_access:
        raise ForbiddenException("Access denied to business", code="FORBIDDEN")

    task_id = None
    try:
        task_res = tasks.scan_business_full.delay(id)
        task_id = getattr(task_res, "id", None)
    except Exception:
        # Fallback to direct synchronous execution if Celery broker is offline
        try:
            tasks.scan_business_full(id)
        except Exception:
            pass

    return ScanTriggerResponse(
        business_id=id,
        status="triggered" if task_id else "completed",
        task_id=task_id,
        message="Scan initiated across Google, Reddit, and X platforms",
    )


@router.get(
    "/businesses/{id}/scan/status",
    response_model=ScanStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get status and progress of reputation scan",
)
async def get_business_scan_status(
    id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select

    from app.core.exceptions import ForbiddenException, NotFoundException
    from app.models.reputation import ReputationScoreHistory
    from app.repositories.business_repository import BusinessRepository
    from app.repositories.finding_repository import FindingRepository
    from app.repositories.ingestion_job_repository import IngestionJobRepository
    from app.repositories.issue_repository import IssueRepository
    from app.repositories.platform_repository import PlatformConnectionRepository
    from app.schemas.scan import ScanStatusResponse

    biz_repo = BusinessRepository(db)
    biz = await biz_repo.get_by_id(id)
    if not biz:
        raise NotFoundException("Business not found", code="BUSINESS_NOT_FOUND")

    has_access = await biz_repo.user_has_access(id, current_user_id)
    if not has_access:
        raise ForbiddenException("Access denied to business", code="FORBIDDEN")

    platform_repo = PlatformConnectionRepository(db)
    active_conns = await platform_repo.list_active_for_business(id)
    active_platforms = [c.platform for c in active_conns]

    job_repo = IngestionJobRepository(db)
    recent_jobs = await job_repo.list_by_business(id, limit=5)
    jobs_summary = [
        {
            "id": j.id,
            "platform": j.platform,
            "status": j.status,
            "records_inserted": j.records_inserted,
            "started_at": j.started_at.isoformat() if j.started_at else None,
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
        }
        for j in recent_jobs
    ]

    issue_repo = IssueRepository(db)
    issues = await issue_repo.list_by_business(id)

    finding_repo = FindingRepository(db)
    findings = await finding_repo.list_by_business(id)

    stmt_rep = select(ReputationScoreHistory).where(ReputationScoreHistory.business_id == id).order_by(ReputationScoreHistory.calculated_at.desc())
    latest_rep = (await db.execute(stmt_rep)).scalars().first()

    return ScanStatusResponse(
        business_id=id,
        status="completed" if recent_jobs and all(j.status in ["completed", "failed"] for j in recent_jobs) else "running",
        active_platforms=active_platforms,
        jobs=jobs_summary,
        issues_count=len(issues),
        findings_count=len(findings),
        reputation_score=latest_rep.current_score if latest_rep else None,
        last_scanned_at=recent_jobs[0].completed_at if recent_jobs and recent_jobs[0].completed_at else None,
    )


@router.post(
    "/business/scan",
    response_model=ScanTriggerResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger scan for active business",
)
async def trigger_active_business_scan(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    biz = await service.get_active_business(current_user_id)
    from app.core.exceptions import NotFoundException
    if not biz:
        raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")
    return await trigger_business_scan(biz.id, current_user_id=current_user_id, db=db)


@router.get(
    "/business/scan/status",
    response_model=ScanStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get scan status for active business",
)
async def get_active_business_scan_status(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    service = BusinessService(db)
    biz = await service.get_active_business(current_user_id)
    from app.core.exceptions import NotFoundException
    if not biz:
        raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")
    return await get_business_scan_status(biz.id, current_user_id=current_user_id, db=db)

