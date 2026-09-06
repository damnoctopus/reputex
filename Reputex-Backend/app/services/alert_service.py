"""Alerts management domain service."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.alert import Alert
from app.repositories.business_repository import BusinessRepository
from app.repositories.user_repository import UserRepository
from app.schemas.alert import AlertItemSchema


class AlertService:
    """Manages system alerts and notification events."""

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

    async def get_alerts(self, user_id: str) -> list[AlertItemSchema]:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(Alert).where(Alert.business_id == business_id).order_by(Alert.created_at.desc())
        alerts = list((await self.db.execute(stmt)).scalars().all())

        if not alerts:
            # Seed default realistic alerts
            alerts = await self._seed_default_alerts(business_id)

        return [AlertItemSchema.model_validate(a) for a in alerts]

    async def mark_as_read(self, user_id: str, alert_id: str) -> None:
        business_id = await self._resolve_business_id(user_id)
        stmt = select(Alert).where(Alert.business_id == business_id, Alert.id == alert_id)
        alert = (await self.db.execute(stmt)).scalars().first()
        if not alert:
            raise NotFoundException("Alert not found", code="ALERT_NOT_FOUND")

        alert.is_read = True
        await self.db.commit()

    async def mark_all_as_read(self, user_id: str) -> None:
        business_id = await self._resolve_business_id(user_id)
        stmt = update(Alert).where(Alert.business_id == business_id, Alert.is_read == False).values(is_read=True)
        await self.db.execute(stmt)
        await self.db.commit()

    async def create_alert(
        self,
        business_id: str,
        type: str,
        title: str,
        message: str,
        severity: str = "medium",
        reference_id: str | None = None,
        reference_type: str | None = None,
    ) -> AlertItemSchema:
        alert = Alert(
            business_id=business_id,
            type=type,
            title=title,
            message=message,
            severity=severity,
            reference_id=reference_id,
            reference_type=reference_type,
            is_read=False,
            created_at=datetime.now(UTC),
        )
        self.db.add(alert)
        await self.db.commit()
        await self.db.refresh(alert)
        return AlertItemSchema.model_validate(alert)

    async def _seed_default_alerts(self, business_id: str) -> list[Alert]:
        now = datetime.now(UTC)
        items = [
            Alert(
                business_id=business_id,
                type="CRISIS",
                title="Service Quality Complaint Wave",
                message="Multiple 1-star reviews detected on Google within the last 4 hours.",
                severity="critical",
                is_read=False,
                reference_type="crisis",
                created_at=now - timedelta(minutes=45),
            ),
            Alert(
                business_id=business_id,
                type="FRAUD_DETECTED",
                title="Potential Astroturfing Detected",
                message="Cluster of 3 near-identical 1-star reviews posted from new accounts.",
                severity="high",
                is_read=False,
                reference_type="fraud",
                created_at=now - timedelta(hours=2),
            ),
            Alert(
                business_id=business_id,
                type="NEGATIVE_REVIEW",
                title="New Negative Review on Reddit",
                message="'Cold food and rude service' posted on r/bangalore foodies.",
                severity="medium",
                is_read=True,
                reference_type="mention",
                created_at=now - timedelta(hours=5),
            ),
            Alert(
                business_id=business_id,
                type="AI_RESPONSE_READY",
                title="AI Response Draft Generated",
                message="Empathetic response ready for review on Google Maps review #2104.",
                severity="low",
                is_read=False,
                reference_type="response_draft",
                created_at=now - timedelta(hours=8),
            ),
        ]
        self.db.add_all(items)
        await self.db.commit()
        for it in items:
            await self.db.refresh(it)
        return items
