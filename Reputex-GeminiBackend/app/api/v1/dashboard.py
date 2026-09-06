"""Dashboard and analytics endpoints matching Flutter DashboardRepository."""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_business
from app.core.database import get_async_db
from app.models.authenticity import ManipulationCluster, ReviewAuthenticityFinding
from app.models.business import Business
from app.models.crisis import CrisisEvent
from app.models.issue import CustomerIssue
from app.models.mention import Mention
from app.models.response import ResponseDraft
from app.schemas.dashboard import (
    DashboardSummary,
    PlatformStatistics,
    ReputationScore,
    SentimentDistribution,
    SentimentTrend,
)
from app.schemas.mention import MentionEngagement, MentionResponse
from app.services.reputation_service import ReputationService
from app.services.time_series_service import TimeSeriesService

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    # 1. Reputation Score
    score = await ReputationService.compute_reputation_score(db, biz.id)

    # 2. Sentiment Distribution
    dist = await TimeSeriesService.compute_sentiment_distribution(db, biz.id)

    # 3. Total Mentions
    tot_stmt = select(func.count(Mention.id)).where(Mention.business_id == biz.id)
    total_mentions = (await db.execute(tot_stmt)).scalar_one() or 0

    # 4. Active crisis
    crisis_stmt = select(CrisisEvent).where(CrisisEvent.business_id == biz.id, CrisisEvent.status == "active")
    active_crisis = (await db.execute(crisis_stmt)).scalar_one_or_none()
    crisis_active = active_crisis is not None
    crisis_risk_level = active_crisis.severity.capitalize() if active_crisis else "Normal"

    crisis_cnt_stmt = select(func.count(CrisisEvent.id)).where(CrisisEvent.business_id == biz.id)
    crisis_count = (await db.execute(crisis_cnt_stmt)).scalar_one() or 0

    # 5. Pending responses
    resp_stmt = select(func.count(ResponseDraft.id)).where(ResponseDraft.business_id == biz.id, ResponseDraft.status == "draft")
    pending_responses_count = (await db.execute(resp_stmt)).scalar_one() or 0

    # 6. Fraud / Suspicious counts
    fraud_stmt = select(func.count(ReviewAuthenticityFinding.id)).where(ReviewAuthenticityFinding.business_id == biz.id)
    fraud_alerts_count = (await db.execute(fraud_stmt)).scalar_one() or 0

    susp_stmt = select(func.count(ReviewAuthenticityFinding.id)).where(
        ReviewAuthenticityFinding.business_id == biz.id,
        ReviewAuthenticityFinding.suspicion_score >= 60,
    )
    suspicious_reviews_count = (await db.execute(susp_stmt)).scalar_one() or 0

    cluster_stmt = select(func.count(ManipulationCluster.id)).where(ManipulationCluster.business_id == biz.id)
    active_clusters_count = (await db.execute(cluster_stmt)).scalar_one() or 0

    # 7. Top Issues
    issues_stmt = select(CustomerIssue).where(CustomerIssue.business_id == biz.id).order_by(CustomerIssue.mention_count.desc()).limit(5)
    issues = list((await db.execute(issues_stmt)).scalars().all())
    top_issues = [
        {
            "id": iss.id,
            "category": iss.category,
            "subtopic": iss.subtopic,
            "severity": iss.severity,
            "mention_count": iss.mention_count,
            "platforms": iss.platforms_breakdown or {},
        }
        for iss in issues
    ]

    # 8. Recent Mentions
    recent_stmt = select(Mention).where(Mention.business_id == biz.id).order_by(Mention.published_at.desc()).limit(10)
    recents = list((await db.execute(recent_stmt)).scalars().all())
    recent_mentions = [
        MentionResponse(
            id=m.id,
            platform=m.platform,
            author=m.author,
            content=m.content,
            sentiment=m.sentiment,
            sentiment_score=m.sentiment_score,
            is_fake=m.is_fake,
            fraud_confidence=m.fraud_confidence,
            url=m.url,
            timestamp=m.published_at,
            engagement=MentionEngagement(**(m.engagement or {})),
            rating=m.rating,
            response_status=m.response_status,
            response_text=m.response_text,
            author_avatar=m.author_avatar,
        )
        for m in recents
    ]

    return DashboardSummary(
        reputation_score=score,
        sentiment_distribution=dist,
        total_mentions=total_mentions,
        crisis_active=crisis_active,
        crisis_count=crisis_count,
        pending_responses_count=pending_responses_count,
        fraud_alerts_count=fraud_alerts_count,
        crisis_risk_level=crisis_risk_level,
        suspicious_reviews_count=suspicious_reviews_count,
        active_clusters_count=active_clusters_count,
        top_issues=top_issues,
        recent_mentions=recent_mentions,
    )


@router.get("/dashboard/score", response_model=ReputationScore)
async def get_dashboard_score(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await ReputationService.compute_reputation_score(db, biz.id)


@router.get("/dashboard/sentiment", response_model=SentimentDistribution)
async def get_dashboard_sentiment(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await TimeSeriesService.compute_sentiment_distribution(db, biz.id)


@router.get("/dashboard/trends", response_model=List[SentimentTrend])
async def get_dashboard_trends(
    days: int = Query(7, ge=1, le=90),
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await TimeSeriesService.compute_sentiment_trends(db, biz.id, days=days)


@router.get("/dashboard/platforms", response_model=List[PlatformStatistics])
async def get_dashboard_platforms(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    return await TimeSeriesService.compute_platform_statistics(db, biz.id)


@router.get("/analytics/sentiment")
async def get_sentiment_analytics(
    biz: Business = Depends(get_current_business),
    db: AsyncSession = Depends(get_async_db),
):
    dist = await TimeSeriesService.compute_sentiment_distribution(db, biz.id)
    trends = await TimeSeriesService.compute_sentiment_trends(db, biz.id, days=7)
    platforms = await TimeSeriesService.compute_platform_statistics(db, biz.id)
    return {
        "distribution": dist.model_dump(),
        "trends": [t.model_dump() for t in trends],
        "platforms": [p.model_dump() for p in platforms],
    }
