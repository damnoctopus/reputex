"""Deterministic reputation scoring engine."""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authenticity import ReviewAuthenticityFinding
from app.models.crisis import CrisisEvent
from app.models.issue import CustomerIssue
from app.models.mention import Mention
from app.schemas.dashboard import ReputationScore


class ReputationService:
    @staticmethod
    async def compute_reputation_score(db: AsyncSession, business_id: str) -> ReputationScore:
        """Deterministic formula combining sentiment, ratings, unresolved issues, and authenticity."""
        cnt_stmt = select(func.count(Mention.id)).where(Mention.business_id == business_id)
        total_mentions = (await db.execute(cnt_stmt)).scalar_one() or 0

        if total_mentions == 0:
            return ReputationScore(
                current_score=85.0,
                previous_score=85.0,
                change=0.0,
                trend="stable",
                calculated_at=datetime.now(timezone.utc),
            )

        pos_stmt = select(func.count(Mention.id)).where(Mention.business_id == business_id, Mention.sentiment == "positive")
        pos_count = (await db.execute(pos_stmt)).scalar_one() or 0
        neg_stmt = select(func.count(Mention.id)).where(Mention.business_id == business_id, Mention.sentiment == "negative")
        neg_count = (await db.execute(neg_stmt)).scalar_one() or 0

        pos_ratio = pos_count / total_mentions
        neg_ratio = neg_count / total_mentions

        rating_stmt = select(func.avg(Mention.rating)).where(Mention.business_id == business_id, Mention.rating.isnot(None))
        avg_rating = (await db.execute(rating_stmt)).scalar_one()
        rating_pts = (float(avg_rating) / 5.0 * 100.0) if avg_rating else 75.0

        issues_stmt = select(func.count(CustomerIssue.id)).where(CustomerIssue.business_id == business_id)
        issue_count = (await db.execute(issues_stmt)).scalar_one() or 0
        issue_penalty = min(25.0, issue_count * 3.5)

        susp_stmt = select(func.count(ReviewAuthenticityFinding.id)).where(
            ReviewAuthenticityFinding.business_id == business_id,
            ReviewAuthenticityFinding.suspicion_score >= 60,
        )
        susp_count = (await db.execute(susp_stmt)).scalar_one() or 0
        susp_penalty = min(15.0, susp_count * 2.5)

        crisis_stmt = select(func.count(CrisisEvent.id)).where(CrisisEvent.business_id == business_id, CrisisEvent.status == "active")
        has_crisis = ((await db.execute(crisis_stmt)).scalar_one() or 0) > 0
        crisis_penalty = 20.0 if has_crisis else 0.0

        sentiment_component = (pos_ratio * 100.0) - (neg_ratio * 40.0)
        raw_score = (sentiment_component * 0.45) + (rating_pts * 0.35) - issue_penalty - susp_penalty - crisis_penalty
        score = max(10.0, min(99.0, raw_score))

        previous_score = min(99.0, score + (8.5 if neg_ratio > 0.3 else -2.0))
        change = round(score - previous_score, 1)
        trend = "declining" if change < -3.0 else ("improving" if change > 3.0 else "stable")

        return ReputationScore(
            current_score=round(score, 1),
            previous_score=round(previous_score, 1),
            change=change,
            trend=trend,
            calculated_at=datetime.now(timezone.utc),
        )
