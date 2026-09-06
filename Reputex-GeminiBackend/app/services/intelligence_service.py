"""Batched Gemini mention intelligence analysis service."""
import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.gemini_client import GeminiClient
from app.models.business import Business
from app.models.mention import Mention, MentionAspect, SentimentAnalysis
from app.schemas.gemini import GeminiMentionAnalysis

logger = logging.getLogger("reputex.intelligence")


class IntelligenceService:
    @staticmethod
    async def analyze_pending_mentions(
        db: AsyncSession,
        business_id: str,
        batch_size: int = 10,
    ) -> int:
        """Process all unanalyzed mentions in batches using Gemini structured intelligence."""
        # Fetch business info for context
        biz_stmt = select(Business).where(Business.id == business_id)
        biz = (await db.execute(biz_stmt)).scalar_one_or_none()
        biz_name = biz.name if biz else "Business"
        biz_category = biz.category if biz else "General"

        # Fetch pending mentions
        stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.ai_status == "PENDING",
        ).order_by(Mention.published_at.desc()).limit(100)

        result = await db.execute(stmt)
        pending_mentions = list(result.scalars().all())
        if not pending_mentions:
            return 0

        client = GeminiClient()
        total_processed = 0

        # Chunk into batches of 10
        for i in range(0, len(pending_mentions), batch_size):
            chunk = pending_mentions[i : i + batch_size]
            payloads = [
                {
                    "content": m.content,
                    "platform": m.platform,
                    "rating": m.rating,
                    "author": m.author,
                }
                for m in chunk
            ]

            analyses: List[GeminiMentionAnalysis] = client.analyze_mentions_batch(
                mentions=payloads,
                business_name=biz_name,
                business_category=biz_category,
            )

            for idx, m in enumerate(chunk):
                analysis = analyses[idx] if idx < len(analyses) else None
                if not analysis:
                    continue

                m.sentiment = analysis.sentiment_label
                m.sentiment_score = analysis.sentiment_score
                m.ai_status = "COMPLETE"

                # Save metadata
                meta = dict(m.metadata_json or {})
                meta["intent"] = analysis.intent
                meta["summary"] = analysis.summary
                meta["linguistic_signals"] = analysis.linguistic_signals.model_dump()
                meta["extracted_issues"] = [iss.model_dump() for iss in analysis.issues]
                m.metadata_json = meta

                # Create SentimentAnalysis record
                sa = SentimentAnalysis(
                    mention_id=m.id,
                    sentiment_label=analysis.sentiment_label,
                    confidence=analysis.confidence,
                    compound_score=analysis.sentiment_score,
                    emotions={"confidence": analysis.confidence, "intent": analysis.intent},
                    aspects=[asp.model_dump() for asp in analysis.aspects],
                )
                db.add(sa)

                # Create MentionAspect records
                for asp in analysis.aspects:
                    db.add(MentionAspect(
                        mention_id=m.id,
                        aspect=asp.aspect,
                        sentiment=asp.sentiment,
                        confidence=asp.confidence,
                    ))

                total_processed += 1

            await db.commit()

        return total_processed
