"""Deterministic crisis detection and early warning alert service."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.crisis import CrisisEvent
from app.models.issue import CustomerIssue
from app.schemas.crisis import CrisisEventResponse
from app.services.time_series_service import TimeSeriesService


class CrisisService:
    @staticmethod
    async def evaluate_crisis(db: AsyncSession, business_id: str) -> Optional[CrisisEvent]:
        """Evaluate time-series metrics and issue severity to generate explainable crisis events."""
        metrics = await TimeSeriesService.compute_metrics_for_crisis(db, business_id)

        neg_ratio = metrics["negative_ratio"]
        delta_s = metrics["sentiment_deterioration"]
        velocity = metrics["complaint_velocity"]
        eng_growth = metrics["engagement_growth"]
        neg_count = metrics["recent_negative_count"]
        affected_plats = metrics["affected_platforms"]

        issues_stmt = select(CustomerIssue).where(
            CustomerIssue.business_id == business_id,
            CustomerIssue.severity.in_(["critical", "high"]),
        )
        critical_issues = list((await db.execute(issues_stmt)).scalars().all())
        has_food_safety = any("poisoning" in iss.subtopic.lower() or "safety" in iss.category.lower() for iss in critical_issues)

        risk_score = 0.0
        drivers = {}

        if neg_ratio > 0.35:
            contrib = min(30.0, neg_ratio * 40.0)
            risk_score += contrib
            drivers["negative_ratio"] = f"Elevated negative ratio ({int(neg_ratio*100)}% of recent mentions are negative)"

        if delta_s < -0.2:
            contrib = min(25.0, abs(delta_s) * 35.0)
            risk_score += contrib
            drivers["sentiment_deterioration"] = f"Sharp sentiment deterioration (ΔS = {delta_s})"

        if velocity >= 4.0:
            contrib = min(20.0, velocity * 3.0)
            risk_score += contrib
            drivers["complaint_velocity"] = f"Surge in complaint velocity ({velocity} negative mentions/day)"

        if len(affected_plats) >= 2:
            risk_score += 15.0
            drivers["cross_platform_spread"] = f"Discussion spreading across multiple platforms ({', '.join(affected_plats)})"

        if has_food_safety:
            risk_score += 25.0
            drivers["severe_incident"] = "High-severity issue detected: Alleged food contamination / safety incident reported"

        risk_score = min(100.0, risk_score)

        if risk_score >= 75 or (has_food_safety and neg_count >= 5):
            risk_level = "Crisis"
            severity = "critical"
        elif risk_score >= 55:
            risk_level = "High Risk"
            severity = "high"
        elif risk_score >= 35:
            risk_level = "Early Warning"
            severity = "medium"
        elif risk_score >= 20:
            risk_level = "Elevated Risk"
            severity = "low"
        else:
            risk_level = "Normal"
            severity = "low"

        del_stmt = select(CrisisEvent).where(CrisisEvent.business_id == business_id)
        for ce in (await db.execute(del_stmt)).scalars().all():
            await db.delete(ce)
        await db.flush()

        if risk_score >= 35:
            actions = [
                "Acknowledge affected customers immediately with transparent communication.",
                "Conduct an internal operational and quality audit.",
                "Issue a statement clarifying management is actively investigating customer concerns.",
                "Monitor public social channels for escalating viral threads.",
            ]

            event = CrisisEvent(
                business_id=business_id,
                title="Viral Reputation Escalation: Food Safety & Service Complaints",
                severity=severity,
                status="active",
                trigger_reason=f"Multi-platform complaint surge with sentiment deterioration (Risk Score: {int(risk_score)}/100)",
                velocity=velocity,
                negative_mentions_count=neg_count,
                affected_platforms=[p.capitalize() for p in affected_plats] or ["Twitter", "Reddit"],
                started_at=datetime.now(timezone.utc),
                suggested_actions=actions,
                estimated_reach=int(neg_count * 1250),
                peak_volume_per_hour=int(max(1, velocity / 6.0)),
                drivers=drivers,
            )
            db.add(event)
            await db.commit()
            return event

        await db.commit()
        return None

    @staticmethod
    async def get_active_crisis(db: AsyncSession, business_id: str) -> Optional[CrisisEventResponse]:
        stmt = select(CrisisEvent).where(
            CrisisEvent.business_id == business_id,
            CrisisEvent.status == "active",
        ).order_by(CrisisEvent.started_at.desc())
        res = await db.execute(stmt)
        ev = res.scalar_one_or_none()
        if not ev:
            return None
        return CrisisEventResponse.model_validate(ev)

    @staticmethod
    async def get_crisis_events(db: AsyncSession, business_id: str) -> List[CrisisEventResponse]:
        stmt = select(CrisisEvent).where(CrisisEvent.business_id == business_id).order_by(CrisisEvent.started_at.desc())
        res = await db.execute(stmt)
        events = list(res.scalars().all())
        return [CrisisEventResponse.model_validate(ev) for ev in events]

    @staticmethod
    async def get_crisis_by_id(db: AsyncSession, business_id: str, crisis_id: str) -> CrisisEventResponse:
        stmt = select(CrisisEvent).where(CrisisEvent.id == crisis_id, CrisisEvent.business_id == business_id)
        res = await db.execute(stmt)
        ev = res.scalar_one_or_none()
        if not ev:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("CrisisEvent", crisis_id)
        return CrisisEventResponse.model_validate(ev)
