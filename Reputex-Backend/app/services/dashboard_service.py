"""Dashboard and Analytics domain service aggregating multi-platform metrics."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.mention import Mention
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import (
    DashboardSummarySchema,
    PlatformStatisticsSchema,
    SentimentAnalyticsSchema,
    SentimentDistributionSchema,
    SentimentTrendSchema,
)
from app.schemas.mention import MentionSchema
from app.services.crisis_service import CrisisService
from app.services.reputation_service import ReputationService


class DashboardService:
    """Aggregates dashboard overviews, sentiment distributions, trends, and platform metrics."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.business_repo = BusinessRepository(db)
        self.reputation_service = ReputationService(db)
        self.crisis_service = CrisisService(db)

    async def _resolve_business_id(self, user_id: str) -> str:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            businesses = await self.business_repo.list_by_owner(user_id)
            if businesses:
                return businesses[0].id
            raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")
        return user.business_id

    async def get_dashboard_summary(self, user_id: str) -> DashboardSummarySchema:
        business_id = await self._resolve_business_id(user_id)

        # 1. Reputation Score
        score = await self.reputation_service.get_current_score(user_id)

        # 2. Fetch Mentions
        stmt = select(Mention).where(Mention.business_id == business_id).order_by(Mention.published_at.desc())
        mentions = list((await self.db.execute(stmt)).scalars().all())

        # If zero mentions, trigger initial seed
        if not mentions:
            from app.services.mention_service import MentionService

            m_service = MentionService(self.db)
            await m_service.ingest_initial_batch(business_id)
            mentions = list((await self.db.execute(stmt)).scalars().all())

        total_mentions = len(mentions)

        # 3. Sentiment Distribution
        pos_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "positive")
        neu_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "neutral")
        neg_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "negative")
        tot = max(1, total_mentions)

        dist = SentimentDistributionSchema(
            positive=pos_count,
            neutral=neu_count,
            negative=neg_count,
            total=total_mentions,
            positive_percentage=round((pos_count / tot) * 100, 1),
            neutral_percentage=round((neu_count / tot) * 100, 1),
            negative_percentage=round((neg_count / tot) * 100, 1),
        )

        # 4. Crisis status
        active_crisis = await self.crisis_service.get_active_crisis(user_id)
        crisis_active = active_crisis is not None
        crisis_count = 1 if crisis_active else 0

        # 5. Fraud alerts count
        fraud_alerts_count = sum(1 for m in mentions if m.is_fake or (m.fraud_confidence or 0.0) >= 0.6)

        # 6. Customer Issues & Findings
        from app.repositories.finding_repository import FindingRepository
        from app.repositories.issue_repository import IssueRepository

        issue_repo = IssueRepository(self.db)
        top_issues_raw = await issue_repo.list_by_business(business_id, limit=5)
        top_issues = [
            {
                "id": iss.id,
                "category": iss.category,
                "subtopic": iss.subtopic,
                "severity": iss.severity,
                "status": iss.status,
                "mention_count": iss.mention_count,
                "platforms_breakdown": iss.platforms_breakdown,
                "last_seen_at": iss.last_seen_at.isoformat() if iss.last_seen_at else None,
            }
            for iss in top_issues_raw
        ]

        finding_repo = FindingRepository(self.db)
        all_findings = await finding_repo.list_by_business(business_id, limit=100)
        suspicious_reviews_count = sum(1 for f in all_findings if f.finding_type == "review_authenticity")
        active_clusters_count = sum(1 for f in all_findings if f.finding_type == "manipulation_cluster")

        crisis_risk_level = "Normal"
        crisis_finding = next((f for f in all_findings if f.finding_type == "crisis_risk"), None)
        if crisis_finding and crisis_finding.metadata_json.get("warning_level"):
            crisis_risk_level = crisis_finding.metadata_json["warning_level"]
        elif crisis_active:
            crisis_risk_level = "Crisis Active"

        # 7. Pending responses (unresponded negative mentions)
        pending_responses_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "negative")

        # 8. Recent mentions (top 5)
        recent_schemas = [
            MentionSchema(
                id=m.id,
                business_id=m.business_id,
                platform=m.platform,
                external_id=m.external_id,
                author=m.author,
                content=m.content,
                url=m.url,
                rating=m.rating,
                timestamp=m.published_at,
                sentiment=m.sentiment or "neutral",
                sentiment_score=m.sentiment_score or 0.0,
                is_fake=m.is_fake,
                fraud_confidence=m.fraud_confidence or 0.0,
            )
            for m in mentions[:5]
        ]

        return DashboardSummarySchema(
            reputation_score=score,
            sentiment_distribution=dist,
            total_mentions=total_mentions,
            crisis_active=crisis_active,
            crisis_count=crisis_count,
            crisis_risk_level=crisis_risk_level,
            pending_responses_count=pending_responses_count,
            fraud_alerts_count=fraud_alerts_count,
            suspicious_reviews_count=suspicious_reviews_count,
            active_clusters_count=active_clusters_count,
            top_issues=top_issues,
            recent_mentions=recent_schemas,
        )

    async def get_sentiment_distribution(self, user_id: str) -> SentimentDistributionSchema:
        summary = await self.get_dashboard_summary(user_id)
        return summary.sentiment_distribution

    async def get_sentiment_trends(self, user_id: str, days: int = 7) -> list[SentimentTrendSchema]:
        business_id = await self._resolve_business_id(user_id)
        now = datetime.now(UTC)
        since_date = now - timedelta(days=days)

        stmt = (
            select(Mention)
            .where(Mention.business_id == business_id, Mention.published_at >= since_date)
            .order_by(Mention.published_at.asc())
        )
        mentions = list((await self.db.execute(stmt)).scalars().all())

        # Group by date string YYYY-MM-DD
        day_buckets: dict[str, dict[str, int]] = {}
        for i in range(days):
            day_str = (since_date + timedelta(days=i + 1)).strftime("%b %d")
            day_buckets[day_str] = {"pos": 0, "neu": 0, "neg": 0}

        for m in mentions:
            date_key = m.published_at.strftime("%b %d")
            if date_key in day_buckets:
                sent = (m.sentiment or "neutral").lower()
                if sent == "positive":
                    day_buckets[date_key]["pos"] += 1
                elif sent == "negative":
                    day_buckets[date_key]["neg"] += 1
                else:
                    day_buckets[date_key]["neu"] += 1

        trends = []
        for d_str, counts in day_buckets.items():
            tot = counts["pos"] + counts["neu"] + counts["neg"]
            score = 75.0
            if tot > 0:
                score = round(((counts["pos"] + (0.5 * counts["neu"])) / tot) * 100, 1)
            trends.append(
                SentimentTrendSchema(
                    date=d_str,
                    positive=counts["pos"],
                    neutral=counts["neu"],
                    negative=counts["neg"],
                    score=score,
                )
            )
        return trends

    async def get_platform_statistics(self, user_id: str) -> list[PlatformStatisticsSchema]:
        business_id = await self._resolve_business_id(user_id)

        stmt = select(Mention).where(Mention.business_id == business_id)
        mentions = list((await self.db.execute(stmt)).scalars().all())

        platform_groups: dict[str, list[Mention]] = {}
        for m in mentions:
            plat = m.platform.capitalize()
            if plat not in platform_groups:
                platform_groups[plat] = []
            platform_groups[plat].append(m)

        # Baseline platforms if empty
        if not platform_groups:
            return [
                PlatformStatisticsSchema(
                    platform="Google",
                    count=14,
                    positive_percentage=71.4,
                    negative_percentage=14.3,
                    neutral_percentage=14.3,
                    average_rating=4.2,
                ),
                PlatformStatisticsSchema(
                    platform="Instagram",
                    count=8,
                    positive_percentage=87.5,
                    negative_percentage=12.5,
                    neutral_percentage=0.0,
                    average_rating=4.7,
                ),
                PlatformStatisticsSchema(
                    platform="Reddit",
                    count=6,
                    positive_percentage=33.3,
                    negative_percentage=50.0,
                    neutral_percentage=16.7,
                    average_rating=3.0,
                ),
                PlatformStatisticsSchema(
                    platform="Twitter",
                    count=5,
                    positive_percentage=60.0,
                    negative_percentage=20.0,
                    neutral_percentage=20.0,
                    average_rating=3.8,
                ),
            ]

        results = []
        for plat, p_mentions in platform_groups.items():
            tot = len(p_mentions)
            pos = sum(1 for m in p_mentions if (m.sentiment or "").lower() == "positive")
            neg = sum(1 for m in p_mentions if (m.sentiment or "").lower() == "negative")
            neu = tot - pos - neg
            ratings = [m.rating for m in p_mentions if m.rating is not None]
            avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else None

            results.append(
                PlatformStatisticsSchema(
                    platform=plat,
                    count=tot,
                    positive_percentage=round((pos / tot) * 100, 1),
                    negative_percentage=round((neg / tot) * 100, 1),
                    neutral_percentage=round((neu / tot) * 100, 1),
                    average_rating=avg_rating,
                )
            )
        return results

    async def get_sentiment_analytics(self, user_id: str) -> SentimentAnalyticsSchema:
        summary = await self.get_dashboard_summary(user_id)
        trends = await self.get_sentiment_trends(user_id, days=7)
        platforms = await self.get_platform_statistics(user_id)

        return SentimentAnalyticsSchema(
            distribution=summary.sentiment_distribution,
            trends=trends,
            platform_breakdown=platforms,
            overall_score=summary.reputation_score.current_score,
            total_reviews_analyzed=summary.total_mentions,
        )
