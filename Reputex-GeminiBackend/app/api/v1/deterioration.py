"""Reputation deterioration prediction router."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.deterioration import DeteriorationAssessment
from app.services.deterioration_service import DeteriorationService

router = APIRouter(prefix="/reputation", tags=["Reputation Deterioration"])


@router.get("/deterioration-prediction", response_model=DeteriorationAssessment)
async def get_deterioration_prediction(
    horizon_days: int = Query(14, ge=7, le=60, description="Forecast horizon in days"),
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    """Returns Gemini's expert assessment on the probability of future reputation deterioration."""
    return await DeteriorationService.get_deterioration_assessment(
        session=db,
        business_id=str(biz.id),
        horizon_days=horizon_days,
    )
