"""Reputation Scoring API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import ReputationScoreSchema
from app.services.reputation_service import ReputationService

router = APIRouter(prefix="/reputation", tags=["Reputation"])


@router.get("", response_model=ReputationScoreSchema)
async def get_reputation_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve current reputation score for the active business."""
    service = ReputationService(db)
    return await service.get_current_score(current_user.id)


@router.get("/history", response_model=list[ReputationScoreSchema])
async def get_reputation_history(
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve historical reputation score records for trend analysis."""
    service = ReputationService(db)
    return await service.get_history(current_user.id, limit=limit)


@router.post("/recalculate", response_model=ReputationScoreSchema)
async def recalculate_reputation_score(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Trigger recalculation of the reputation score based on latest metrics."""
    service = ReputationService(db)
    return await service.recalculate(current_user.id)
