"""Issues discovery and customer complaint API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.issue import IssueSchema, IssuesListResponse
from app.services.issue_detection_service import IssueDetectionService

router = APIRouter(tags=["Issues"])


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
    "/businesses/{business_id}/issues",
    response_model=IssuesListResponse,
    status_code=status.HTTP_200_OK,
    summary="List customer issues and complaints for a business",
)
async def list_business_issues(
    business_id: str,
    category: str | None = Query(None, description="Filter by category"),
    severity: str | None = Query(None, description="Filter by severity (critical, high, medium, low)"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status (active, emerging, resolved)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db, business_id)
    service = IssueDetectionService(db)
    issues = await service.list_issues(
        business_id=biz_id,
        category=category,
        severity=severity,
        status=status_filter,
        limit=limit,
        offset=offset,
    )
    return IssuesListResponse(
        items=[IssueSchema.model_validate(iss) for iss in issues],
        total_count=len(issues),
    )


@router.get(
    "/businesses/{business_id}/issues/{issue_id}",
    response_model=IssueSchema,
    status_code=status.HTTP_200_OK,
    summary="Get issue details with supporting evidence mentions",
)
async def get_business_issue(
    business_id: str,
    issue_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db, business_id)
    service = IssueDetectionService(db)
    issue = await service.get_issue_by_id(issue_id, biz_id)
    if not issue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")
    return IssueSchema.model_validate(issue)


# Active business convenience shortcuts (used by mobile app)
@router.get(
    "/issues",
    response_model=IssuesListResponse,
    status_code=status.HTTP_200_OK,
    summary="List customer issues for the active business",
)
async def list_active_issues(
    category: str | None = Query(None),
    severity: str | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db)
    return await list_business_issues(
        business_id=biz_id,
        category=category,
        severity=severity,
        status_filter=status_filter,
        limit=limit,
        offset=offset,
        current_user_id=current_user_id,
        db=db,
    )


@router.get(
    "/issues/{issue_id}",
    response_model=IssueSchema,
    status_code=status.HTTP_200_OK,
    summary="Get issue details for the active business",
)
async def get_active_issue(
    issue_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    biz_id = await _resolve_business_id_for_user(current_user_id, db)
    return await get_business_issue(
        business_id=biz_id,
        issue_id=issue_id,
        current_user_id=current_user_id,
        db=db,
    )
