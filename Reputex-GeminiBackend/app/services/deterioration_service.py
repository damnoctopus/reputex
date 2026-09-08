"""Deterioration Service.

Orchestrates the Future Reputation Deterioration Assessment feature.
Queries the business's recent mentions, prepares a contextual summary,
and asks Gemini for its expert opinion on future deterioration probability.
"""
import logging
from typing import Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.business import Business
from app.models.mention import Mention, SentimentAnalysis
from app.schemas.deterioration import DeteriorationAssessment
from app.ai.gemini_client import GeminiClient

logger = logging.getLogger(__name__)


class DeteriorationService:
    @staticmethod
    async def get_deterioration_assessment(
        session: AsyncSession,
        business_id: str,
        horizon_days: int = 14,
    ) -> DeteriorationAssessment:
        """Generates an expert Gemini reputation deterioration assessment for a business."""
        # 1. Fetch business
        biz_res = await session.execute(select(Business).where(Business.id == business_id))
        business = biz_res.scalar_one_or_none()
        if not business:
            raise ValueError(f"Business with ID {business_id} not found")

        # 2. Query recent mentions (up to 60)
        mentions_query = (
            select(Mention, SentimentAnalysis)
            .outerjoin(SentimentAnalysis, SentimentAnalysis.mention_id == Mention.id)
            .where(Mention.business_id == business_id)
            .order_by(desc(Mention.published_at))
            .limit(60)
        )
        res = await session.execute(mentions_query)
        rows = res.all()

        recent_reviews = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_rating = 0.0
        rating_count = 0

        for m, s in rows:
            rating = m.rating or (s.compound_score * 2.5 + 2.5 if s else None)
            if rating is not None:
                total_rating += rating
                rating_count += 1

            sentiment_label = (s.sentiment_label if s and s.sentiment_label else (m.sentiment or "neutral")).lower()
            if sentiment_label == "positive":
                positive_count += 1
            elif sentiment_label == "negative":
                negative_count += 1
            else:
                neutral_count += 1

            recent_reviews.append({
                "id": str(m.id),
                "platform": m.platform,
                "author": m.author,
                "content": m.content,
                "rating": rating,
                "sentiment": sentiment_label,
                "published_at": m.published_at.isoformat() if m.published_at else None,
            })

        avg_rating = round(total_rating / max(rating_count, 1), 2) if rating_count > 0 else 4.0
        total_mentions = len(recent_reviews)

        summary_text = (
            f"Analyzed {total_mentions} recent customer mentions for {business.name}. "
            f"Average Rating: {avg_rating} / 5.0 across {rating_count} rated reviews. "
            f"Sentiment breakdown: {positive_count} positive, {neutral_count} neutral, {negative_count} negative. "
            f"Platforms surveyed: Google Reviews, Reddit, X (Twitter)."
        )

        # 3. Call Gemini
        client = GeminiClient()
        gemini_resp = await client.assess_reputation_deterioration(
            business_name=business.name,
            business_category=business.category or "General Business",
            review_summary=summary_text,
            recent_reviews=recent_reviews,
            horizon_days=horizon_days,
        )

        return DeteriorationAssessment(
            business_id=str(business.id),
            business_name=business.name,
            deterioration_probability=gemini_resp.deterioration_probability,
            risk_level=gemini_resp.risk_level,
            is_sustained_decline=gemini_resp.is_sustained_decline,
            confidence=gemini_resp.confidence,
            key_drivers=gemini_resp.key_drivers,
            converging_complaints=gemini_resp.converging_complaints,
            expert_opinion=gemini_resp.expert_opinion,
            recommended_actions=gemini_resp.recommended_actions,
            horizon_days=horizon_days,
        )
