"""Fraud Detection API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.fraud import FraudResultSchema
from app.services.fraud_service import FraudService

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])


@router.get("", response_model=list[FraudResultSchema])
async def get_fraud_reviews(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all fraudulent or suspicious reviews detected for the active business."""
    service = FraudService(db)
    return await service.get_fraud_reviews(current_user.id)


@router.get("/{mention_id}", response_model=FraudResultSchema)
async def get_fraud_analysis(
    mention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve explainable fraud analysis for a specific review/mention."""
    service = FraudService(db)
    return await service.get_fraud_analysis(current_user.id, mention_id)


@router.post("/analyze/{mention_id}", response_model=FraudResultSchema)
async def analyze_fraud(
    mention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Explicitly trigger fraud detection analysis for a specific review/mention."""
    service = FraudService(db)
    return await service.get_fraud_analysis(current_user.id, mention_id)
