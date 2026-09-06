"""Evidence-backed Findings service answering 'Why did RepuTex say this?'."""
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.authenticity import ManipulationCluster, ReviewAuthenticityFinding
from app.models.crisis import CrisisEvent
from app.models.finding import Finding, FindingEvidence
from app.models.issue import CustomerIssue
from app.schemas.finding import FindingEvidenceItemResponse, FindingItemResponse


class FindingsService:
    @staticmethod
    async def generate_findings(db: AsyncSession, business_id: str) -> None:
        """Generate traceable, evidence-backed findings from issues, authenticity, and crises."""
        del_stmt = select(Finding).where(Finding.business_id == business_id)
        for f in (await db.execute(del_stmt)).scalars().all():
            await db.delete(f)
        await db.flush()

        now = datetime.now(timezone.utc)

        # 1. ISSUE Findings
        issues_stmt = select(CustomerIssue).where(
            CustomerIssue.business_id == business_id
        ).options(selectinload(CustomerIssue.evidence))
        issues = list((await db.execute(issues_stmt)).scalars().all())

        for iss in issues:
            f = Finding(
                business_id=business_id,
                finding_type="ISSUE",
                severity=iss.severity,
                confidence=0.92,
                score=float(iss.mention_count),
                title=f"Recurring Issue: {iss.category} - {iss.subtopic}",
                description=f"{iss.mention_count} customer mentions across {len(iss.platforms_breakdown)} platforms report {iss.subtopic.lower()}.\nPlatforms: {', '.join([f'{k.capitalize()} ({v})' for k, v in iss.platforms_breakdown.items()])}",
                detected_at=now,
                first_seen_at=iss.first_seen_at,
                last_seen_at=iss.last_seen_at,
                metadata_json={
                    "issue_id": iss.id,
                    "category": iss.category,
                    "subtopic": iss.subtopic,
                    "platforms_breakdown": iss.platforms_breakdown,
                },
            )
            db.add(f)
            await db.flush()

            for ev in iss.evidence:
                db.add(FindingEvidence(
                    finding_id=f.id,
                    mention_id=ev.mention_id,
                    evidence_type="review",
                    snippet=ev.excerpt,
                    relevance_score=ev.relevance_score,
                ))

        # 2. SUSPICIOUS_REVIEW Findings
        susp_stmt = select(ReviewAuthenticityFinding).where(
            ReviewAuthenticityFinding.business_id == business_id,
            ReviewAuthenticityFinding.suspicion_score >= 50,
        )
        susp_findings = list((await db.execute(susp_stmt)).scalars().all())

        for sf in susp_findings[:15]:
            f = Finding(
                business_id=business_id,
                finding_type="SUSPICIOUS_REVIEW",
                severity="high" if sf.suspicion_score >= 80 else "medium",
                confidence=sf.confidence,
                score=sf.suspicion_score,
                title=f"{sf.risk_level}: Review by {sf.author or 'Anonymous'}",
                description=f"Review on {sf.platform or 'web'} exhibited suspicious signals: {', '.join(sf.reasons)}",
                detected_at=now,
                first_seen_at=sf.timestamp or now,
                last_seen_at=sf.timestamp or now,
                metadata_json={
                    "mention_id": sf.mention_id,
                    "patterns": sf.patterns,
                    "risk_level": sf.risk_level,
                },
            )
            db.add(f)
            await db.flush()

            db.add(FindingEvidence(
                finding_id=f.id,
                mention_id=sf.mention_id,
                evidence_type="review",
                snippet=sf.review_content[:200] if sf.review_content else "",
                relevance_score=sf.confidence,
            ))

        # 3. MANIPULATION_CLUSTER Findings
        clusters_stmt = select(ManipulationCluster).where(ManipulationCluster.business_id == business_id)
        clusters = list((await db.execute(clusters_stmt)).scalars().all())

        for cl in clusters:
            f = Finding(
                business_id=business_id,
                finding_type="MANIPULATION_CLUSTER",
                severity="critical",
                confidence=cl.confidence,
                score=85.0,
                title=cl.cluster_name,
                description=f"Detected coordinated manipulation burst of {cl.review_count} reviews within {cl.time_window_minutes} minutes with matching 5-star ratings and promotional phrasing.",
                detected_at=now,
                first_seen_at=cl.created_at,
                last_seen_at=cl.created_at,
                metadata_json=cl.metadata_json or {},
            )
            db.add(f)
            await db.flush()

            for m_id in (cl.metadata_json.get("mention_ids", []) if cl.metadata_json else []):
                db.add(FindingEvidence(
                    finding_id=f.id,
                    mention_id=m_id,
                    evidence_type="cluster_member",
                    snippet="Coordinated burst review with templated language",
                    relevance_score=cl.confidence,
                ))

        # 4. CRISIS Findings
        crisis_stmt = select(CrisisEvent).where(CrisisEvent.business_id == business_id, CrisisEvent.status == "active")
        crisis_events = list((await db.execute(crisis_stmt)).scalars().all())

        for ce in crisis_events:
            f = Finding(
                business_id=business_id,
                finding_type="CRISIS",
                severity=ce.severity,
                confidence=0.95,
                score=ce.velocity,
                title=ce.title,
                description=f"Active Reputation Crisis: {ce.trigger_reason}. Spread across {', '.join(ce.affected_platforms)}.",
                detected_at=now,
                first_seen_at=ce.started_at,
                last_seen_at=now,
                metadata_json=ce.drivers or {},
            )
            db.add(f)

        await db.commit()

    @staticmethod
    async def get_findings(
        db: AsyncSession,
        business_id: str,
        finding_type: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[FindingItemResponse]:
        stmt = select(Finding).where(Finding.business_id == business_id).options(selectinload(Finding.evidence))

        if finding_type and finding_type.lower() != "all":
            stmt = stmt.where(Finding.finding_type == finding_type.upper())
        if severity and severity.lower() != "all":
            stmt = stmt.where(Finding.severity == severity.lower())

        stmt = stmt.order_by(Finding.detected_at.desc(), Finding.score.desc())
        res = await db.execute(stmt)
        findings = list(res.scalars().all())

        results = []
        for f in findings:
            ev_items = [
                FindingEvidenceItemResponse(
                    id=e.id,
                    finding_id=e.finding_id,
                    mention_id=e.mention_id,
                    evidence_type=e.evidence_type,
                    snippet=e.snippet,
                    relevance_score=e.relevance_score,
                    created_at=e.created_at,
                )
                for e in f.evidence
            ]
            results.append(FindingItemResponse(
                id=f.id,
                business_id=f.business_id,
                finding_type=f.finding_type,
                severity=f.severity,
                confidence=f.confidence,
                score=f.score,
                title=f.title,
                description=f.description,
                detected_at=f.detected_at,
                first_seen_at=f.first_seen_at,
                last_seen_at=f.last_seen_at,
                metadata_json=f.metadata_json or {},
                evidence=ev_items,
            ))
        return results
