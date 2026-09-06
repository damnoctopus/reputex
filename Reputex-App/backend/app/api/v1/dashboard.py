"""Dashboard and Analytics API endpoints matching Flutter RealApiService and OpenAPI specs."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.schemas.dashboard import (
    DashboardSummarySchema,
    PlatformStatisticsSchema,
    ReputationScoreSchema,
    SentimentAnalyticsSchema,
    SentimentDistributionSchema,
    SentimentTrendSchema,
)
from app.services.dashboard_service import DashboardService
from app.services.reputation_service import ReputationService

router = APIRouter(tags=["Dashboard & Analytics"])


# ── Flutter /dashboard/ endpoints ──


@router.get("/dashboard", response_model=DashboardSummarySchema)
async def get_dashboard_summary(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve full dashboard overview summary."""
    service = DashboardService(db)
    return await service.get_dashboard_summary(current_user_id)


@router.get("/dashboard/score", response_model=ReputationScoreSchema)
async def get_dashboard_reputation_score(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve reputation score for the dashboard."""
    rep_service = ReputationService(db)
    return await rep_service.get_current_score(current_user_id)


@router.get("/dashboard/sentiment", response_model=SentimentDistributionSchema)
async def get_dashboard_sentiment_distribution(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve sentiment distribution metrics."""
    service = DashboardService(db)
    return await service.get_sentiment_distribution(current_user_id)


@router.get("/dashboard/trends", response_model=list[SentimentTrendSchema])
async def get_dashboard_sentiment_trends(
    days: int = Query(default=7, ge=1, le=90),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve day-by-day sentiment trend history."""
    service = DashboardService(db)
    return await service.get_sentiment_trends(current_user_id, days=days)


@router.get("/dashboard/platforms", response_model=list[PlatformStatisticsSchema])
async def get_dashboard_platform_statistics(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve aggregated breakdown by platform."""
    service = DashboardService(db)
    return await service.get_platform_statistics(current_user_id)


# ── General /analytics/ aliases ──


@router.get("/analytics/overview", response_model=DashboardSummarySchema)
async def get_analytics_overview(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Alias for dashboard overview."""
    service = DashboardService(db)
    return await service.get_dashboard_summary(current_user_id)


@router.get("/analytics/sentiment", response_model=SentimentAnalyticsSchema)
async def get_sentiment_analytics(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Comprehensive sentiment analytics combining distribution, trends, and platform metrics."""
    service = DashboardService(db)
    return await service.get_sentiment_analytics(current_user_id)


@router.get("/analytics/trends", response_model=list[SentimentTrendSchema])
async def get_analytics_trends(
    days: int = Query(default=7, ge=1, le=90),
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Alias for sentiment trends."""
    service = DashboardService(db)
    return await service.get_sentiment_trends(current_user_id, days=days)


@router.get("/analytics/platforms", response_model=list[PlatformStatisticsSchema])
async def get_analytics_platforms(
    current_user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Alias for platform breakdown."""
    service = DashboardService(db)
    return await service.get_platform_statistics(current_user_id)
