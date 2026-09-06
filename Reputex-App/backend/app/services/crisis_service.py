"""Crisis Detection and Monitoring domain service."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.crisis import CrisisEvent
from app.models.mention import Mention
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.crisis import CrisisEventSchema, CrisisEventUpdateSchema


class CrisisService:
    """Manages crisis detection, anomaly evaluation, and response workflows."""

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

    async def get_crisis_events(self, user_id: str) -> list[CrisisEventSchema]:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(CrisisEvent).where(CrisisEvent.business_id == business_id).order_by(CrisisEvent.started_at.desc())
        events = list((await self.db.execute(stmt)).scalars().all())

        if not events:
            # Seed an illustrative crisis scenario
            seeded = await self._seed_default_crisis(business_id)
            return [CrisisEventSchema.model_validate(seeded)]

        return [CrisisEventSchema.model_validate(e) for e in events]

    async def get_active_crisis(self, user_id: str) -> CrisisEventSchema | None:
        business_id = await self._resolve_business_id(user_id)
        stmt = (
            select(CrisisEvent)
            .where(CrisisEvent.business_id == business_id, CrisisEvent.status == "active")
            .order_by(CrisisEvent.started_at.desc())
        )
        event = (await self.db.execute(stmt)).scalars().first()
        if not event:
            # Check if any events exist at all; if not, seed default
            all_events = await self.get_crisis_events(user_id)
            for ev in all_events:
                if ev.status == "active":
                    return ev
            return None
        return CrisisEventSchema.model_validate(event)

    async def get_crisis_by_id(self, user_id: str, crisis_id: str) -> CrisisEventSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(CrisisEvent).where(
            CrisisEvent.business_id == business_id,
            CrisisEvent.id == crisis_id,
        )
        event = (await self.db.execute(stmt)).scalars().first()
        if not event:
            raise NotFoundException("Crisis event not found", code="CRISIS_NOT_FOUND")
        return CrisisEventSchema.model_validate(event)

    async def update_crisis(
        self, user_id: str, crisis_id: str, update_data: CrisisEventUpdateSchema
    ) -> CrisisEventSchema:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(CrisisEvent).where(
            CrisisEvent.business_id == business_id,
            CrisisEvent.id == crisis_id,
        )
        event = (await self.db.execute(stmt)).scalars().first()
        if not event:
            raise NotFoundException("Crisis event not found", code="CRISIS_NOT_FOUND")

        if update_data.status is not None:
            event.status = update_data.status
            if update_data.status == "resolved" and not event.resolved_at:
                event.resolved_at = datetime.now(UTC)
        if update_data.resolved_at is not None:
            event.resolved_at = update_data.resolved_at
        if update_data.suggested_actions is not None:
            event.suggested_actions = update_data.suggested_actions

        await self.db.commit()
        await self.db.refresh(event)
        return CrisisEventSchema.model_validate(event)

    async def analyze_and_detect(self, user_id: str) -> CrisisEventSchema | None:
        """Detect anomalies such as sudden spikes in negative reviews."""
        business_id = await self._resolve_business_id(user_id)
        now = datetime.now(UTC)
        past_24h = now - timedelta(hours=24)

        stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.published_at >= past_24h,
        )
        recent_mentions = list((await self.db.execute(stmt)).scalars().all())

        if not recent_mentions:
            return None

        total = len(recent_mentions)
        negative = [m for m in recent_mentions if (m.sentiment or "").lower() == "negative"]
        neg_count = len(negative)
        neg_pct = (neg_count / total) * 100.0 if total else 0.0

        # Anomaly trigger: >= 3 negative mentions and > 40% negative in 24h
        if neg_count >= 3 and neg_pct >= 40.0:
            platforms = list({m.platform for m in negative})
            severity = "critical" if neg_pct >= 60.0 else "high"
            event = CrisisEvent(
                business_id=business_id,
                title="Negative Velocity Surge",
                severity=severity,
                status="active",
                trigger_reason=f"Sudden surge of {neg_count} negative reviews ({neg_pct:.0f}% of total volume) within 24 hours.",
                velocity=round(neg_count / 24.0, 2),
                negative_mentions_count=neg_count,
                affected_platforms=platforms,
                suggested_actions=[
                    "Acknowledge customer concerns publicly within 1 hour",
                    "Offer direct manager contact for resolution",
                    "Conduct internal hygiene audit with kitchen staff",
                    "Temporarily pause promotional ad campaigns",
                ],
                estimated_reach=neg_count * 150,
                peak_volume_per_hour=max(1, neg_count // 3),
                started_at=now,
            )
            self.db.add(event)
            await self.db.commit()
            await self.db.refresh(event)
            return CrisisEventSchema.model_validate(event)

        return None

    async def _seed_default_crisis(self, business_id: str) -> CrisisEvent:
        event = CrisisEvent(
            business_id=business_id,
            title="Service Quality Complaint Wave",
            severity="high",
            status="active",
            trigger_reason="Unusual concentration of 1-star reviews on Google and Reddit citing dinner rush delay.",
            velocity=3.4,
            negative_mentions_count=7,
            affected_platforms=["Google", "Reddit"],
            suggested_actions=[
                "Deploy proactive empathetic apologies on negative Google reviews",
                "Clarify kitchen rush delay and offer complimentary dessert on next visit",
                "Brief floor staff on peak-hour table communication protocols",
            ],
            estimated_reach=1450,
            peak_volume_per_hour=4,
            started_at=datetime.now(UTC) - timedelta(hours=6),
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event
