"""Findings and Review Authenticity API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.repositories.business_repository import BusinessRepository
from app.repositories.finding_repository import FindingRepository
from app.repositories.user_repository import UserRepository
from app.schemas.finding import FindingSchema, FindingsListResponse
from app.services.authenticity_service import ReviewAuthenticityService

router = APIRouter(tags=["Findings & Review Authenticity"])


async def _resolve_business_id_for_user(user_id: str, db: AsyncSession, requested_biz_id: str | None = None) -> str:
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    biz_repo = BusinessRepository(db)
    if requested_biz_id:
        has_access = await biz_repo.user_has_access(requested_biz_id, user_id)
        if not has_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to business")
        return requested_biz_id

    if user.business_id:
        return user.business_id

    owned = await biz_repo.list_by_owner(user_id)
    if owned:
        return owned[0].id

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active business found")


@router.get(
    "/businesses/{business_id}/findings",
    response_model=FindingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all intelligence findings with evidence for a business",
)
async def list_business_findings(
    business_id: str,
    finding_type: str | None = Query(None, description="Filter by finding type"),
    severity: str | None = Query(None, description="Filter by severity"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db, business_id)
    finding_repo = FindingRepository(db)
    findings = await finding_repo.list_by_business(
        business_id=biz_id,
        finding_type=finding_type,
        severity=severity,
        limit=limit,
        offset=offset,
    )
    return FindingsListResponse(
        items=[FindingSchema.model_validate(f) for f in findings],
        total_count=len(findings),
    )


@router.get(
    "/businesses/{business_id}/suspicious-reviews",
    response_model=FindingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List suspicious reviews and manipulation risks for a business",
)
async def list_business_suspicious_reviews(
    business_id: str,
    severity: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db, business_id)
    auth_service = ReviewAuthenticityService(db)
    findings = await auth_service.list_suspicious_reviews(
        business_id=biz_id,
        severity=severity,
        limit=limit,
        offset=offset,
    )
    return FindingsListResponse(
        items=[FindingSchema.model_validate(f) for f in findings],
        total_count=len(findings),
    )


# Active business shortcuts
@router.get(
    "/findings",
    response_model=FindingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List intelligence findings for the active business",
)
async def list_active_findings(
    finding_type: str | None = Query(None),
    severity: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db)
    return await list_business_findings(
        business_id=biz_id,
        finding_type=finding_type,
        severity=severity,
        limit=limit,
        offset=offset,
        current_user_id=current_user_id,
        db=db,
    )


@router.get(
    "/suspicious-reviews",
    response_model=FindingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List suspicious reviews for the active business",
)
async def list_active_suspicious_reviews(
    severity: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db)
    return await list_business_suspicious_reviews(
        business_id=biz_id,
        severity=severity,
        limit=limit,
        offset=offset,
        current_user_id=current_user_id,
        db=db,
    )


@router.get(
    "/manipulation-clusters",
    response_model=FindingsListResponse,
    status_code=status.HTTP_200_OK,
    summary="List coordinated review manipulation clusters for the active business",
)
async def list_active_manipulation_clusters(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db)
    auth_service = ReviewAuthenticityService(db)
    clusters = await auth_service.list_manipulation_clusters(
        business_id=biz_id,
        limit=limit,
        offset=offset,
    )
    return FindingsListResponse(
        items=[FindingSchema.model_validate(c) for c in clusters],
        total_count=len(clusters),
    )
