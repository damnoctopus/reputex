"""Repository for ingestion job telemetry and audit tracking."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ingestion_job import IngestionJob
from app.repositories.base import BaseRepository


class IngestionJobRepository(BaseRepository[IngestionJob]):
    def __init__(self, db: AsyncSession):
        super().__init__(IngestionJob, db)

    async def start_job(self, business_id: str, platform: str) -> IngestionJob:
        job = IngestionJob(
            business_id=business_id,
            platform=platform,
            status="RUNNING",
            started_at=datetime.now(UTC),
            created_at=datetime.now(UTC),
        )
        self.db.add(job)
        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def finish_job(
        self,
        job_id: str,
        status: str,
        records_fetched: int = 0,
        records_normalized: int = 0,
        records_inserted: int = 0,
        records_skipped: int = 0,
        error_message: str | None = None,
    ) -> IngestionJob | None:
        job = await self.get_by_id(job_id)
        if not job:
            return None

        job.status = status
        job.completed_at = datetime.now(UTC)
        job.records_fetched = records_fetched
        job.records_normalized = records_normalized
        job.records_inserted = records_inserted
        job.records_skipped = records_skipped
        job.error_message = error_message

        await self.db.commit()
        await self.db.refresh(job)
        return job

    async def list_by_business(
        self, business_id: str, platform: str | None = None, limit: int = 50
    ) -> list[IngestionJob]:
        stmt = select(IngestionJob).where(IngestionJob.business_id == business_id)
        if platform:
            stmt = stmt.where(IngestionJob.platform.ilike(platform.strip()))
        stmt = stmt.order_by(IngestionJob.started_at.desc()).limit(limit)
        return list((await self.db.execute(stmt)).scalars().all())
