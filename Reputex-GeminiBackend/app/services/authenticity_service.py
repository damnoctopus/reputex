"""Evidence-based review authenticity and manipulation cluster detection service."""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.authenticity import ManipulationCluster, ReviewAuthenticityFinding
from app.models.mention import Mention
from app.schemas.fraud import FraudResult, SuspiciousPattern


def _to_utc(dt: Optional[datetime]) -> datetime:
    if dt is None:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class ReviewAuthenticityService:
    @staticmethod
    async def evaluate_authenticity(db: AsyncSession, business_id: str) -> None:
        """Evaluate mentions using multi-signal suspicion scoring and detect manipulation clusters."""
        stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.ai_status == "COMPLETE",
        ).order_by(Mention.published_at.asc())

        mentions = list((await db.execute(stmt)).scalars().all())
        if not mentions:
            return

        # Clear existing authenticity findings for clean run
        del_findings = select(ReviewAuthenticityFinding).where(ReviewAuthenticityFinding.business_id == business_id)
        for row in (await db.execute(del_findings)).scalars().all():
            await db.delete(row)
        del_clusters = select(ManipulationCluster).where(ManipulationCluster.business_id == business_id)
        for row in (await db.execute(del_clusters)).scalars().all():
            await db.delete(row)
        await db.flush()

        cluster_mentions: List[Mention] = []

        for i, m in enumerate(mentions):
            meta = m.metadata_json or {}
            ling = meta.get("linguistic_signals", {})
            templated = float(ling.get("templated_language", 0.0))
            superlatives = float(ling.get("excessive_superlatives", 0.0))
            unusual = float(ling.get("unusual_patterns", 0.0))

            # Signal 1: Linguistic score (0-40 pts)
            ling_score = (templated * 25.0) + (superlatives * 15.0)

            # Signal 2: Temporal burst (0-30 pts)
            m_time = _to_utc(m.published_at)
            window_start = m_time - timedelta(minutes=40)
            window_end = m_time + timedelta(minutes=40)
            nearby = [
                other for other in mentions
                if other.id != m.id
                and window_start <= _to_utc(other.published_at) <= window_end
                and other.rating == m.rating
            ]
            burst_score = min(30.0, len(nearby) * 7.5)

            # Signal 3: Text similarity / repetition (0-20 pts)
            text_sim_score = 0.0
            for other in nearby:
                c1 = m.content.strip().lower()
                c2 = other.content.strip().lower()
                if c1 == c2 or (len(c1) > 20 and c1[:20] in c2):
                    text_sim_score = 20.0
                    break

            # Signal 4: Extreme polarized rating inversion / unusual pattern (0-15 pts)
            rating_score = 15.0 if (m.rating == 5.0 and (templated > 0.6 or unusual > 0.5)) else 0.0

            suspicion_score = min(100.0, ling_score + burst_score + text_sim_score + rating_score)

            if suspicion_score >= 75:
                risk_level = "High Suspicion"
                is_fraud = True
            elif suspicion_score >= 55:
                risk_level = "Likely Suspicious"
                is_fraud = True
            elif suspicion_score >= 35:
                risk_level = "Potentially Suspicious"
                is_fraud = False
            else:
                risk_level = "Normal"
                is_fraud = False

            m.is_fake = is_fraud
            m.fraud_confidence = round(suspicion_score / 100.0, 2)

            if suspicion_score >= 35:
                reasons = []
                patterns = []
                if templated > 0.5:
                    reasons.append(f"High templated linguistic patterns detected ({int(templated*100)}% confidence)")
                    patterns.append(SuspiciousPattern(pattern_name="Templated Phrasing", description="Phrasing mirrors common automated marketing copy", severity="high").model_dump())
                if burst_score >= 10:
                    reasons.append(f"Unusual posting burst: {len(nearby)} identical-rating reviews in close proximity")
                    patterns.append(SuspiciousPattern(pattern_name="Temporal Burst", description="Unusual velocity of polarized reviews within 40 minutes", severity="high").model_dump())
                if text_sim_score > 0:
                    reasons.append("Verbatim or near-verbatim text duplication across multiple reviewer accounts")
                    patterns.append(SuspiciousPattern(pattern_name="Text Duplication", description="Repeated text identified across independent accounts", severity="critical").model_dump())

                finding = ReviewAuthenticityFinding(
                    business_id=business_id,
                    mention_id=m.id,
                    suspicion_score=round(suspicion_score, 1),
                    confidence=round(max(0.7, suspicion_score / 100.0), 2),
                    risk_level=risk_level,
                    is_fraudulent=is_fraud,
                    reasons=reasons or ["Elevated promotional linguistic markers"],
                    patterns=patterns,
                    review_content=m.content,
                    author=m.author,
                    platform=m.platform,
                    timestamp=m.published_at,
                )
                db.add(finding)

                if suspicion_score >= 60:
                    cluster_mentions.append(m)

        if len(cluster_mentions) >= 3:
            cluster = ManipulationCluster(
                business_id=business_id,
                cluster_name="Coordinated 5-Star Promotional Burst",
                risk_level="Review Manipulation Risk",
                confidence=0.92,
                review_count=len(cluster_mentions),
                platforms=list({m.platform for m in cluster_mentions}),
                time_window_minutes=45,
                metadata_json={
                    "mention_ids": [m.id for m in cluster_mentions],
                    "average_rating": 5.0,
                    "signals": ["Templated Language", "Temporal Velocity Spike", "Linguistic Repetition"],
                },
            )
            db.add(cluster)

        await db.commit()

    @staticmethod
    async def get_fraud_reviews(db: AsyncSession, business_id: str) -> List[FraudResult]:
        stmt = select(ReviewAuthenticityFinding).where(ReviewAuthenticityFinding.business_id == business_id).order_by(ReviewAuthenticityFinding.suspicion_score.desc())
        res = await db.execute(stmt)
        findings = list(res.scalars().all())

        results = []
        for f in findings:
            patterns = [
                SuspiciousPattern(pattern_name=p.get("pattern_name", ""), description=p.get("description", ""), severity=p.get("severity", "medium"))
                for p in (f.patterns or [])
            ]
            results.append(FraudResult(
                mention_id=f.mention_id,
                is_fraudulent=f.is_fraudulent,
                confidence=f.confidence,
                risk_level=f.risk_level,
                reasons=f.reasons or [],
                patterns=patterns,
                review_content=f.review_content,
                author=f.author,
                platform=f.platform,
                timestamp=f.timestamp,
            ))
        return results

    @staticmethod
    async def get_fraud_analysis_for_mention(db: AsyncSession, business_id: str, mention_id: str) -> FraudResult:
        stmt = select(ReviewAuthenticityFinding).where(
            ReviewAuthenticityFinding.business_id == business_id,
            ReviewAuthenticityFinding.mention_id == mention_id,
        )
        res = await db.execute(stmt)
        f = res.scalar_one_or_none()
        if f:
            patterns = [
                SuspiciousPattern(pattern_name=p.get("pattern_name", ""), description=p.get("description", ""), severity=p.get("severity", "medium"))
                for p in (f.patterns or [])
            ]
            return FraudResult(
                mention_id=f.mention_id,
                is_fraudulent=f.is_fraudulent,
                confidence=f.confidence,
                risk_level=f.risk_level,
                reasons=f.reasons or [],
                patterns=patterns,
                review_content=f.review_content,
                author=f.author,
                platform=f.platform,
                timestamp=f.timestamp,
            )

        return FraudResult(
            mention_id=mention_id,
            is_fraudulent=False,
            confidence=0.9,
            risk_level="Normal",
            reasons=["No suspicious patterns or linguistic anomalies detected"],
            patterns=[],
        )
