"""Customer issues and complaints endpoints matching Flutter CustomerIssues screens."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.issue import CustomerIssueResponse, CustomerIssuesListResponse
from app.services.issue_detection_service import IssueDetectionService

router = APIRouter(prefix="/issues", tags=["Customer Issues"])


@router.get("", response_model=CustomerIssuesListResponse)
async def get_issues(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    issues = await IssueDetectionService.get_issues(
        db,
        business_id=biz.id,
        category=category,
        severity=severity,
        status=status,
    )
    return CustomerIssuesListResponse(items=issues, total=len(issues))


@router.get("/{id}", response_model=CustomerIssueResponse)
async def get_issue_by_id(
    id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await IssueDetectionService.get_issue_by_id(db, biz.id, id)
