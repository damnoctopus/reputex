"""Review Authenticity and Manipulation Detection service with explainable signal attribution."""

import difflib
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.finding import Finding, FindingEvidence
from app.models.mention import Mention
from app.repositories.finding_repository import FindingRepository


class ReviewAuthenticityService:
    """Detects review manipulation risks, calculates transparent suspicion scores,

    and discovers coordinated manipulation clusters with evidence links.
    Safe Terminology:
      - 'Potentially Suspicious' (0.40 - 0.59)
      - 'Likely Suspicious' (0.60 - 0.79)
      - 'High Suspicion' (>= 0.80)
      - 'Review Manipulation Risk'
    """

    GENERIC_SUPERLATIVES = [
        "best place in the world",
        "must visit for everyone",
        "absolute perfection",
        "life changing experience",
        "ten stars if i could",
        "highly recommended by me",
        "top notch quality guaranteed",
        "greatest of all time",
        "unmatched excellence",
    ]

    SPAM_ATTACK_PHRASES = [
        "complete scam",
        "scam!",
        "worst experience ever",
        "do not visit",
        "cheat",
        "fraudsters",
        "money waste",
        "beware guys",
        "fake reviews",
    ]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.finding_repo = FindingRepository(db)

    def evaluate_mention_suspicion(
        self, mention: Mention, all_mentions: list[Mention]
    ) -> dict[str, Any]:
        """Calculates transparent multi-signal suspicion breakdown for a single review."""
        signals: list[dict[str, Any]] = []
        raw_score = 0.0
        content_lower = mention.content.lower().strip()

        # 1. Lexical / Syntactic Over-Optimization
        superlative_hits = [p for p in self.GENERIC_SUPERLATIVES if p in content_lower]
        spam_hits = [p for p in self.SPAM_ATTACK_PHRASES if p in content_lower]

        if superlative_hits:
            pts = min(0.30, len(superlative_hits) * 0.15)
            raw_score += pts
            signals.append({
                "signal_name": "Syntactic Superlative Density",
                "score_contribution": round(pts, 2),
                "description": f"Overly promotional phrasing detected: {', '.join(superlative_hits)}",
            })
        elif spam_hits:
            pts = min(0.35, len(spam_hits) * 0.20)
            raw_score += pts
            signals.append({
                "signal_name": "Coordinated Attack Signatures",
                "score_contribution": round(pts, 2),
                "description": f"High-frequency generic attack keywords detected: {', '.join(spam_hits)}",
            })

        # 2. Text Duplication / Template Phrasing Across Reviews
        duplicates = [
            other for other in all_mentions
            if other.id != mention.id and (
                content_lower == other.content.lower().strip()
                or (len(content_lower) > 35 and content_lower[:35] == other.content.lower().strip()[:35])
                or difflib.SequenceMatcher(None, content_lower, other.content.lower().strip()).ratio() > 0.85
            )
        ]
        if duplicates:
            pts = min(0.40, 0.25 + 0.05 * len(duplicates))
            raw_score += pts
            signals.append({
                "signal_name": "Duplicate Text Template",
                "score_contribution": round(pts, 2),
                "description": f"Identical or near-identical text template matches {len(duplicates)} other reviewer post(s)",
            })

        # 3. Temporal Burst / Clumping (same platform within 30 minutes)
        burst_matches = [
            other for other in all_mentions
            if other.id != mention.id
            and other.platform == mention.platform
            and abs((other.published_at - mention.published_at).total_seconds()) <= 1800
        ]
        if len(burst_matches) >= 2:
            pts = min(0.30, 0.15 + (0.05 * len(burst_matches)))
            raw_score += pts
            signals.append({
                "signal_name": "Temporal Burst Velocity",
                "score_contribution": round(pts, 2),
                "description": f"Abnormal velocity cluster: {len(burst_matches) + 1} reviews published within 30 minutes on {mention.platform}",
            })

        # 4. Extreme Polarization Inversion
        if mention.rating is not None:
            if mention.rating >= 5.0 and len(mention.content) < 25 and (superlative_hits or duplicates):
                pts = 0.20
                raw_score += pts
                signals.append({
                    "signal_name": "Polarized Rating Inversion",
                    "score_contribution": pts,
                    "description": "Maximum 5-star rating with minimal content and promotional patterns",
                })
            elif mention.rating <= 1.0 and (mention.sentiment_score or 0) < -0.8 and spam_hits:
                pts = 0.25
                raw_score += pts
                signals.append({
                    "signal_name": "Polarized Rating Inversion",
                    "score_contribution": pts,
                    "description": "Minimum 1-star rating with extreme negative deviation and attack phrases",
                })

        suspicion_score = round(min(0.99, max(0.05, raw_score)), 2)

        # Map to safe terminology
        if suspicion_score >= 0.80:
            label = "High Suspicion"
            severity = "critical"
        elif suspicion_score >= 0.60:
            label = "Likely Suspicious"
            severity = "high"
        elif suspicion_score >= 0.40:
            label = "Potentially Suspicious"
            severity = "medium"
        else:
            label = "Authentic Review"
            severity = "low"

        return {
            "score": suspicion_score,
            "label": label,
            "severity": severity,
            "signals": signals,
            "duplicate_mention_ids": [d.id for d in duplicates],
            "burst_mention_ids": [b.id for b in burst_matches],
        }

    async def analyze_business_authenticity(self, business_id: str) -> list[Finding]:
        """Runs full authenticity and manipulation cluster discovery on all mentions for business."""
        stmt = (
            select(Mention)
            .where(Mention.business_id == business_id)
            .order_by(Mention.published_at.desc())
        )
        mentions = list((await self.db.execute(stmt)).scalars().all())
        if not mentions:
            return []

        # Remove existing review_authenticity and manipulation_cluster findings for fresh analysis
        await self.finding_repo.delete_for_business(business_id, finding_type="review_authenticity")
        await self.finding_repo.delete_for_business(business_id, finding_type="manipulation_cluster")

        persisted_findings: list[Finding] = []
        suspicious_evaluations: list[tuple[Mention, dict[str, Any]]] = []

        # Track template clusters
        template_groups: dict[str, list[Mention]] = defaultdict(list)

        for mention in mentions:
            eval_result = self.evaluate_mention_suspicion(mention, mentions)
            # Update mention columns for backward compatibility
            mention.fraud_confidence = eval_result["score"]
            mention.is_fake = eval_result["score"] >= 0.60

            if eval_result["score"] >= 0.40:
                suspicious_evaluations.append((mention, eval_result))

            # Key for template clustering (normalized first 35 chars)
            cleaned_prefix = mention.content.lower().strip()[:35]
            if len(cleaned_prefix) >= 20:
                template_groups[cleaned_prefix].append(mention)

        await self.db.commit()

        # 1. Persist individual suspicious review findings (for score >= 0.40)
        for mention, eval_data in suspicious_evaluations:
            finding = Finding(
                business_id=business_id,
                finding_type="review_authenticity",
                severity=eval_data["severity"],
                confidence=eval_data["score"],
                score=eval_data["score"],
                title=f"{eval_data['label']}: Review on {mention.platform}",
                description=(
                    f"Review exhibits {len(eval_data['signals'])} manipulation indicator(s). "
                    + "; ".join([s["description"] for s in eval_data["signals"]])
                ),
                detected_at=datetime.now(UTC),
                first_seen_at=mention.published_at,
                last_seen_at=mention.published_at,
                metadata_json={
                    "mention_id": mention.id,
                    "author": mention.author,
                    "platform": mention.platform,
                    "rating": mention.rating,
                    "label": eval_data["label"],
                    "signals": eval_data["signals"],
                },
            )
            evidence = [
                FindingEvidence(
                    mention_id=mention.id,
                    evidence_type="review",
                    snippet=mention.content[:150],
                    relevance_score=eval_data["score"],
                    created_at=datetime.now(UTC),
                )
            ]
            saved = await self.finding_repo.save_finding(finding, evidence)
            persisted_findings.append(saved)

        # 2. Persist Coordinated Review Manipulation Clusters (3+ reviews sharing template)
        for template, group_mentions in template_groups.items():
            if len(group_mentions) >= 3:
                platforms = list({m.platform for m in group_mentions})
                timestamps = [m.published_at for m in group_mentions]
                first_time = min(timestamps)
                last_time = max(timestamps)

                cluster_finding = Finding(
                    business_id=business_id,
                    finding_type="manipulation_cluster",
                    severity="critical" if len(group_mentions) >= 5 else "high",
                    confidence=0.92,
                    score=0.90,
                    title=f"Coordinated Review Manipulation Cluster ({len(group_mentions)} reviews)",
                    description=(
                        f"Detected coordinated pattern of {len(group_mentions)} reviews sharing nearly identical "
                        f"phrasing across {', '.join(platforms)}. Indicative of coordinated artificial review campaign."
                    ),
                    detected_at=datetime.now(UTC),
                    first_seen_at=first_time,
                    last_seen_at=last_time,
                    metadata_json={
                        "cluster_size": len(group_mentions),
                        "platforms": platforms,
                        "shared_template_snippet": template,
                        "mention_ids": [m.id for m in group_mentions],
                    },
                )
                evidence = [
                    FindingEvidence(
                        mention_id=m.id,
                        evidence_type="review",
                        snippet=m.content[:150],
                        relevance_score=0.95,
                        created_at=datetime.now(UTC),
                    )
                    for m in group_mentions
                ]
                saved_cluster = await self.finding_repo.save_finding(cluster_finding, evidence)
                persisted_findings.append(saved_cluster)

        return persisted_findings

    async def list_suspicious_reviews(
        self, business_id: str, severity: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[Finding]:
        return await self.finding_repo.list_by_business(
            business_id=business_id,
            finding_type="review_authenticity",
            severity=severity,
            limit=limit,
            offset=offset,
        )

    async def list_manipulation_clusters(
        self, business_id: str, limit: int = 50, offset: int = 0
    ) -> list[Finding]:
        return await self.finding_repo.list_by_business(
            business_id=business_id,
            finding_type="manipulation_cluster",
            limit=limit,
            offset=offset,
        )
