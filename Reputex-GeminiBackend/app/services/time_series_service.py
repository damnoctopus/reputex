"""Deterministic time-series analytics (Negative ratio, Delta S, Engagement Growth, Velocity)."""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mention import Mention
from app.schemas.dashboard import PlatformStatistics, SentimentDistribution, SentimentTrend


class TimeSeriesService:
    @staticmethod
    async def compute_sentiment_distribution(db: AsyncSession, business_id: str) -> SentimentDistribution:
        stmt = select(Mention.sentiment, func.count(Mention.id)).where(
            Mention.business_id == business_id
        ).group_by(Mention.sentiment)

        res = await db.execute(stmt)
        counts = {row[0].lower(): row[1] for row in res.all()}

        pos = counts.get("positive", 0)
        neu = counts.get("neutral", 0)
        neg = counts.get("negative", 0)
        total = pos + neu + neg

        pos_pct = round((pos / total) * 100.0, 1) if total > 0 else 0.0
        neu_pct = round((neu / total) * 100.0, 1) if total > 0 else 0.0
        neg_pct = round((neg / total) * 100.0, 1) if total > 0 else 0.0

        return SentimentDistribution(
            positive=pos,
            neutral=neu,
            negative=neg,
            total=total,
            positive_percentage=pos_pct,
            neutral_percentage=neu_pct,
            negative_percentage=neg_pct,
        )

    @staticmethod
    async def compute_platform_statistics(db: AsyncSession, business_id: str) -> List[PlatformStatistics]:
        stmt = select(
            Mention.platform,
            func.count(Mention.id),
            func.avg(Mention.rating),
        ).where(Mention.business_id == business_id).group_by(Mention.platform)

        res = await db.execute(stmt)
        rows = res.all()

        results = []
        for row in rows:
            plat = row[0]
            cnt = row[1]
            avg_rating = round(float(row[2] or 0.0), 1)

            plat_sent_stmt = select(Mention.sentiment, func.count(Mention.id)).where(
                Mention.business_id == business_id,
                Mention.platform == plat,
            ).group_by(Mention.sentiment)
            plat_counts = {r[0].lower(): r[1] for r in (await db.execute(plat_sent_stmt)).all()}
            p_pos = plat_counts.get("positive", 0)
            p_neg = plat_counts.get("negative", 0)

            pos_pct = round((p_pos / cnt) * 100.0, 1) if cnt > 0 else 0.0
            neg_pct = round((p_neg / cnt) * 100.0, 1) if cnt > 0 else 0.0

            results.append(PlatformStatistics(
                platform=plat.capitalize(),
                count=cnt,
                average_rating=avg_rating,
                positive_percentage=pos_pct,
                negative_percentage=neg_pct,
            ))
        return results

    @staticmethod
    async def compute_sentiment_trends(db: AsyncSession, business_id: str, days: int = 7) -> List[SentimentTrend]:
        now = datetime.now(timezone.utc)
        trends = []

        for d in range(days - 1, -1, -1):
            day_date = (now - timedelta(days=d)).date()
            start_dt = datetime.combine(day_date, datetime.min.time()).replace(tzinfo=timezone.utc)
            end_dt = datetime.combine(day_date, datetime.max.time()).replace(tzinfo=timezone.utc)

            stmt = select(
                Mention.sentiment,
                func.count(Mention.id),
                func.avg(Mention.sentiment_score),
            ).where(
                Mention.business_id == business_id,
                Mention.published_at >= start_dt,
                Mention.published_at <= end_dt,
            ).group_by(Mention.sentiment)

            rows = (await db.execute(stmt)).all()
            day_counts = {r[0].lower(): r[1] for r in rows}
            avg_scores = [r[2] for r in rows if r[2] is not None]
            avg_score = round(float(sum(avg_scores) / len(avg_scores)), 2) if avg_scores else 0.0

            trends.append(SentimentTrend(
                date=day_date.strftime("%Y-%m-%d"),
                positive=day_counts.get("positive", 0),
                neutral=day_counts.get("neutral", 0),
                negative=day_counts.get("negative", 0),
                average_score=avg_score,
            ))
        return trends

    @staticmethod
    async def compute_metrics_for_crisis(
        db: AsyncSession,
        business_id: str,
        recent_hours: int = 48,
    ) -> Dict[str, Any]:
        """Deterministic math: Negative ratio (N_t), Deterioration (Delta S), Velocity, Engagement Growth (G_t)."""
        now = datetime.now(timezone.utc)
        cutoff_recent = now - timedelta(hours=recent_hours)
        cutoff_prior = now - timedelta(hours=recent_hours * 2)

        recent_stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.published_at >= cutoff_recent,
        )
        recent_mentions = list((await db.execute(recent_stmt)).scalars().all())

        prior_stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.published_at >= cutoff_prior,
            Mention.published_at < cutoff_recent,
        )
        prior_mentions = list((await db.execute(prior_stmt)).scalars().all())

        total_recent = len(recent_mentions)
        neg_recent = sum(1 for m in recent_mentions if m.sentiment == "negative")
        total_prior = len(prior_mentions)
        neg_prior = sum(1 for m in prior_mentions if m.sentiment == "negative")

        # 1. Negative Ratio: N_t = neg / total
        negative_ratio = (neg_recent / total_recent) if total_recent > 0 else 0.0

        # 2. Sentiment Deterioration: Delta S_t = S_t - S_{t-k}
        s_recent = sum(m.sentiment_score for m in recent_mentions) / max(total_recent, 1)
        s_prior = sum(m.sentiment_score for m in prior_mentions) / max(total_prior, 1)
        delta_s = s_recent - s_prior

        # 3. Complaint Velocity (complaints per day)
        velocity = (neg_recent / (recent_hours / 24.0))

        # 4. Engagement Growth: G_t = (E_t - E_{t-k}) / max(E_{t-k}, 1)
        eng_recent = sum(
            (m.engagement.get("likes", 0) + m.engagement.get("retweets", 0) + m.engagement.get("upvotes", 0))
            for m in recent_mentions
        )
        eng_prior = sum(
            (m.engagement.get("likes", 0) + m.engagement.get("retweets", 0) + m.engagement.get("upvotes", 0))
            for m in prior_mentions
        )
        eng_growth = ((eng_recent - eng_prior) / max(eng_prior, 1.0)) if eng_prior > 0 else (1.0 if eng_recent > 0 else 0.0)

        platforms_recent = list({m.platform for m in recent_mentions if m.sentiment == "negative"})

        return {
            "negative_ratio": round(negative_ratio, 3),
            "sentiment_deterioration": round(delta_s, 3),
            "complaint_velocity": round(velocity, 2),
            "engagement_growth": round(eng_growth, 2),
            "recent_negative_count": neg_recent,
            "total_recent_count": total_recent,
            "affected_platforms": platforms_recent,
            "recent_mentions": recent_mentions,
        }
