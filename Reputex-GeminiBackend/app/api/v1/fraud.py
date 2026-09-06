"""Fraud and review authenticity endpoints matching Flutter FraudRepository."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.business import Business
from app.schemas.fraud import FraudResult
from app.services.authenticity_service import ReviewAuthenticityService

router = APIRouter(prefix="/fraud", tags=["Fraud & Authenticity"])


@router.get("", response_model=List[FraudResult])
async def get_fraud_reviews(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ReviewAuthenticityService.get_fraud_reviews(db, biz.id)


@router.get("/{mention_id}", response_model=FraudResult)
async def get_fraud_analysis(
    mention_id: str,
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ReviewAuthenticityService.get_fraud_analysis_for_mention(db, biz.id, mention_id)
