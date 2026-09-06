"""Reputation Scoring Service with isolated formula and history tracking."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.mention import Mention
from app.models.reputation import ReputationScoreHistory
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.dashboard import ReputationScoreSchema


class ReputationService:
    """Isolated reputation score computation and tracking engine."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.business_repo = BusinessRepository(db)

    async def _resolve_business_id(self, user_id: str) -> str:
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.business_id:
            businesses = await self.business_repo.list_by_owner(user_id)
            if businesses:
                return businesses[0].id
            raise NotFoundException("Active business not found", code="BUSINESS_NOT_FOUND")
        return user.business_id

    async def compute_score_for_business(self, business_id: str) -> dict[str, Any]:
        """Formula:
        Base components:
        - Rating (0 - 5 stars mapped to 0 - 100): 35%
        - Sentiment (positive % vs negative % mapped to 0 - 100): 30%
        - Volume Factor (scaled by target volume): 15%
        - Response / Health Factor: 20%
        Penalties:
        - Fraud penalty (deduction if fake reviews > 5%)
        """
        # Fetch mentions for the business
        stmt = select(Mention).where(Mention.business_id == business_id)
        mentions = list((await self.db.execute(stmt)).scalars().all())

        if not mentions:
            # Default baseline score for fresh business
            return {
                "score": 85.0,
                "components": {
                    "rating_component": 85.0,
                    "sentiment_component": 85.0,
                    "volume_component": 80.0,
                    "response_component": 90.0,
                    "fraud_penalty": 0.0,
                },
            }

        total_reviews = len(mentions)
        ratings = [m.rating for m in mentions if m.rating is not None]
        avg_rating = sum(ratings) / len(ratings) if ratings else 4.0
        rating_comp = min(100.0, max(0.0, (avg_rating / 5.0) * 100.0))

        pos_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "positive")
        neg_count = sum(1 for m in mentions if (m.sentiment or "").lower() == "negative")
        sentiment_ratio = (pos_count + 0.5) / max(1, pos_count + neg_count + 1)
        sentiment_comp = min(100.0, max(0.0, sentiment_ratio * 100.0))

        # Volume score: target benchmark of 50 reviews
        volume_comp = min(100.0, (total_reviews / 50.0) * 100.0)

        # Response / Health score
        fake_count = sum(1 for m in mentions if m.is_fake or (m.fraud_confidence or 0.0) >= 0.6)
        fraud_ratio = fake_count / max(1, total_reviews)
        fraud_penalty = min(25.0, fraud_ratio * 50.0)

        response_comp = 88.0

        # Weighted calculation
        raw_score = (
            (0.35 * rating_comp)
            + (0.30 * sentiment_comp)
            + (0.15 * volume_comp)
            + (0.20 * response_comp)
            - fraud_penalty
        )
        final_score = round(min(100.0, max(10.0, raw_score)), 1)

        return {
            "score": final_score,
            "components": {
                "rating_component": round(rating_comp, 1),
                "sentiment_component": round(sentiment_comp, 1),
                "volume_component": round(volume_comp, 1),
                "response_component": round(response_comp, 1),
                "fraud_penalty": round(fraud_penalty, 1),
                "total_reviews": total_reviews,
                "fake_count": fake_count,
            },
        }

    async def get_current_score(self, user_id: str) -> ReputationScoreSchema:
        business_id = await self._resolve_business_id(user_id)

        # Get latest score history
        stmt = (
            select(ReputationScoreHistory)
            .where(ReputationScoreHistory.business_id == business_id)
            .order_by(ReputationScoreHistory.calculated_at.desc())
        )
        latest = (await self.db.execute(stmt)).scalars().first()

        if not latest:
            return await self.recalculate(user_id)

        return ReputationScoreSchema(
            current_score=latest.current_score,
            previous_score=latest.previous_score,
            change=latest.change,
            trend=latest.trend,
            calculated_at=latest.calculated_at,
        )

    async def get_history(self, user_id: str, limit: int = 30) -> list[ReputationScoreSchema]:
        business_id = await self._resolve_business_id(user_id)
        stmt = (
            select(ReputationScoreHistory)
            .where(ReputationScoreHistory.business_id == business_id)
            .order_by(ReputationScoreHistory.calculated_at.desc())
            .limit(limit)
        )
        records = list((await self.db.execute(stmt)).scalars().all())

        # If no records exist, run first calculation
        if not records:
            first = await self.recalculate(user_id)
            return [first]

        return [
            ReputationScoreSchema(
                current_score=r.current_score,
                previous_score=r.previous_score,
                change=r.change,
                trend=r.trend,
                calculated_at=r.calculated_at,
            )
            for r in records
        ]

    async def recalculate(self, user_id: str) -> ReputationScoreSchema:
        business_id = await self._resolve_business_id(user_id)

        # Get latest existing score
        stmt = (
            select(ReputationScoreHistory)
            .where(ReputationScoreHistory.business_id == business_id)
            .order_by(ReputationScoreHistory.calculated_at.desc())
        )
        previous = (await self.db.execute(stmt)).scalars().first()
        prev_score = previous.current_score if previous else None

        res = await self.compute_score_for_business(business_id)
        new_score = res["score"]

        if prev_score is not None:
            change = round(new_score - prev_score, 1)
            if change > 0.5:
                trend = "improving"
            elif change < -0.5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            change = 0.0
            trend = "stable"

        history_entry = ReputationScoreHistory(
            business_id=business_id,
            current_score=new_score,
            previous_score=prev_score,
            change=change,
            trend=trend,
            components=res["components"],
            calculated_at=datetime.now(UTC),
        )
        self.db.add(history_entry)
        await self.db.commit()
        await self.db.refresh(history_entry)

        return ReputationScoreSchema(
            current_score=history_entry.current_score,
            previous_score=history_entry.previous_score,
            change=history_entry.change,
            trend=history_entry.trend,
            calculated_at=history_entry.calculated_at,
        )
