"""Explainable Fraud Detection domain service using multi-signal heuristics."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.fraud import FraudAnalysis
from app.models.mention import Mention
from app.repositories.business_repository import BusinessRepository
from app.repositories.mention_repository import MentionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.fraud import FraudResultSchema, SuspiciousPatternSchema


class FraudDetector:
    """Explainable rule-based fraud detection engine."""

    SPAM_PHRASES = [
        "complete scam",
        "worst experience ever",
        "scam!",
        "do not visit",
        "cheat",
        "fake reviews",
        "beware guys",
        "money waste",
        "fraudsters",
    ]

    def analyze(self, mention: Mention, recent_mentions: list[Mention]) -> dict[str, Any]:
        reasons: list[str] = []
        patterns: list[dict[str, Any]] = []
        score = 0.0

        content_lower = mention.content.lower()

        # 1. Spam Phrasing Anomaly
        spam_hits = [p for p in self.SPAM_PHRASES if p in content_lower]
        if spam_hits:
            score += 0.35
            reasons.append(f"Contains high-frequency negative spam triggers: {', '.join(spam_hits)}")
            patterns.append(
                {
                    "pattern_name": "Syntactic Spam Signature",
                    "description": "Text contains overt malicious triggering phrases",
                    "severity": "high",
                }
            )

        # 2. Rating & Sentiment Inversion
        if mention.rating is not None and mention.rating <= 1.0 and mention.sentiment_score < -0.8:
            score += 0.25
            reasons.append("Extreme polarization: rating 1.0 coupled with extreme negative sentiment score")
            patterns.append(
                {
                    "pattern_name": "Extreme Polarization",
                    "description": "Maximum negative sentiment deviation with minimal rating",
                    "severity": "medium",
                }
            )

        # 3. Duplicate Text Detection across other reviews
        duplicate_count = sum(
            1
            for other in recent_mentions
            if other.id != mention.id
            and (
                mention.content.strip() == other.content.strip()
                or (len(mention.content) > 30 and mention.content[:30] in other.content)
            )
        )
        if duplicate_count > 0:
            score += 0.40
            reasons.append(f"Identical or near-identical phrasing detected across {duplicate_count} other reviews")
            patterns.append(
                {
                    "pattern_name": "Duplicate Text Wave",
                    "description": "Identical review text posted across different accounts",
                    "severity": "critical",
                }
            )

        # 4. Review Burst Detection (same platform within short window)
        time_diffs = [
            abs((m.published_at - mention.published_at).total_seconds())
            for m in recent_mentions
            if m.id != mention.id and m.platform == mention.platform
        ]
        burst_count = sum(1 for diff in time_diffs if diff <= 900)  # within 15 minutes
        if burst_count >= 2:
            score += 0.30
            reasons.append(
                f"Coordinated burst: {burst_count + 1} reviews posted within 15 minutes on {mention.platform}"
            )
            patterns.append(
                {
                    "pattern_name": "Review Burst",
                    "description": "Coordinated cluster of reviews submitted within a 15-minute window",
                    "severity": "critical",
                }
            )

        confidence = min(0.99, max(0.05, round(score, 2)))

        if confidence >= 0.70:
            risk_level = "critical" if confidence >= 0.85 else "high"
            is_fraudulent = True
        elif confidence >= 0.40:
            risk_level = "medium"
            is_fraudulent = False
        else:
            risk_level = "low"
            is_fraudulent = False
            if not reasons:
                reasons.append("No suspicious indicators detected")

        return {
            "is_fraudulent": is_fraudulent,
            "confidence": confidence,
            "risk_level": risk_level,
            "reasons": reasons,
            "patterns": patterns,
        }


class FraudService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.detector = FraudDetector()
        self.mention_repo = MentionRepository(db)
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

    async def get_fraud_reviews(self, user_id: str) -> list[FraudResultSchema]:
        business_id = await self._resolve_business_id(user_id)

        stmt = (
            select(Mention)
            .where(Mention.business_id == business_id, (Mention.is_fake == True) | (Mention.fraud_confidence >= 0.6))
            .order_by(Mention.published_at.desc())
        )
        flagged = list((await self.db.execute(stmt)).scalars().all())

        results = []
        for m in flagged:
            analysis = await self.get_or_run_analysis(m)
            results.append(analysis)
        return results

    async def get_fraud_analysis(self, user_id: str, mention_id: str) -> FraudResultSchema:
        business_id = await self._resolve_business_id(user_id)
        mention = await self.mention_repo.get_by_business_and_id(business_id, mention_id)
        if not mention:
            raise NotFoundException("Mention not found", code="MENTION_NOT_FOUND")
        return await self.get_or_run_analysis(mention)

    async def get_or_run_analysis(self, mention: Mention) -> FraudResultSchema:
        # Check existing
        stmt = select(FraudAnalysis).where(FraudAnalysis.mention_id == mention.id)
        existing = (await self.db.execute(stmt)).scalars().first()
        if existing:
            patterns = [SuspiciousPatternSchema(**p) for p in existing.patterns]
            return FraudResultSchema(
                mention_id=mention.id,
                is_fraudulent=existing.is_fraudulent,
                confidence=existing.confidence,
                risk_level=existing.risk_level,
                reasons=existing.reasons,
                patterns=patterns,
                review_content=mention.content,
                author=mention.author,
                platform=mention.platform,
                timestamp=mention.published_at,
            )

        # Run fresh analysis
        from app.schemas.mention import MentionsFilterParams

        recent, _, _, _ = await self.mention_repo.list_paginated(
            business_id=mention.business_id,
            filter_params=MentionsFilterParams(page=1, limit=50),
        )
        res = self.detector.analyze(mention, recent)

        # Persist analysis
        analysis = FraudAnalysis(
            mention_id=mention.id,
            business_id=mention.business_id,
            is_fraudulent=res["is_fraudulent"],
            confidence=res["confidence"],
            risk_level=res["risk_level"],
            reasons=res["reasons"],
            patterns=res["patterns"],
        )
        self.db.add(analysis)

        # Update mention record
        mention.is_fake = res["is_fraudulent"]
        mention.fraud_confidence = res["confidence"]
        await self.db.commit()

        patterns = [SuspiciousPatternSchema(**p) for p in res["patterns"]]
        return FraudResultSchema(
            mention_id=mention.id,
            is_fraudulent=res["is_fraudulent"],
            confidence=res["confidence"],
            risk_level=res["risk_level"],
            reasons=res["reasons"],
            patterns=patterns,
            review_content=mention.content,
            author=mention.author,
            platform=mention.platform,
            timestamp=mention.published_at,
        )
