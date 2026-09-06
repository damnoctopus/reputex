"""Sentiment & Aspect Analysis API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.sentiment import AspectSentimentSchema, SentimentAnalysisSchema
from app.services.sentiment_service import SentimentService

router = APIRouter(tags=["Sentiment"])


@router.get("/sentiment/{mention_id}", response_model=SentimentAnalysisSchema)
async def get_mention_sentiment(
    mention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve or run sentiment analysis on a specific mention."""
    service = SentimentService(db)
    return await service.analyze_mention(current_user.id, mention_id)


@router.post("/sentiment/analyze/{mention_id}", response_model=SentimentAnalysisSchema)
async def analyze_mention_sentiment(
    mention_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Explicitly trigger sentiment analysis for a mention."""
    service = SentimentService(db)
    return await service.analyze_mention(current_user.id, mention_id)


@router.get("/analytics/aspects", response_model=list[AspectSentimentSchema])
async def get_aspect_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated aspect-based sentiment analysis for the active business."""
    service = SentimentService(db)
    return await service.get_aspect_analytics(current_user.id)
