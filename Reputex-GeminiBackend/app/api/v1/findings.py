"""Evidence-backed Findings endpoints matching Flutter Findings repository."""
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.finding import FindingsListResponse
from app.services.findings_service import FindingsService

router = APIRouter(tags=["Findings"])


@router.get("/findings", response_model=FindingsListResponse)
async def get_findings(
    finding_type: Optional[str] = None,
    severity: Optional[str] = None,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    items = await FindingsService.get_findings(db, biz.id, finding_type=finding_type, severity=severity)
    return FindingsListResponse(items=items, total=len(items))


@router.get("/suspicious-reviews", response_model=FindingsListResponse)
async def get_suspicious_review_findings(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    items = await FindingsService.get_findings(db, biz.id, finding_type="SUSPICIOUS_REVIEW")
    return FindingsListResponse(items=items, total=len(items))


@router.get("/manipulation-clusters", response_model=FindingsListResponse)
async def get_manipulation_cluster_findings(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    items = await FindingsService.get_findings(db, biz.id, finding_type="MANIPULATION_CLUSTER")
    return FindingsListResponse(items=items, total=len(items))
