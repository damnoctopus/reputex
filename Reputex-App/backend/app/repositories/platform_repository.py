"""Repository for platform connection and incremental polling state persistence."""

from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.platform import PlatformConnection
from app.repositories.base import BaseRepository


class PlatformConnectionRepository(BaseRepository[PlatformConnection]):
    def __init__(self, db: AsyncSession):
        super().__init__(PlatformConnection, db)

    async def get_by_business_and_platform(self, business_id: str, platform: str) -> PlatformConnection | None:
        stmt = select(PlatformConnection).where(
            PlatformConnection.business_id == business_id,
            PlatformConnection.platform.ilike(platform.strip()),
        )
        return (await self.db.execute(stmt)).scalars().first()

    async def list_active_for_business(self, business_id: str) -> list[PlatformConnection]:
        stmt = select(PlatformConnection).where(
            PlatformConnection.business_id == business_id,
            PlatformConnection.is_active == True,  # noqa: E712
        )
        return list((await self.db.execute(stmt)).scalars().all())

    async def list_all_active(self) -> list[PlatformConnection]:
        stmt = select(PlatformConnection).where(PlatformConnection.is_active == True)  # noqa: E712
        return list((await self.db.execute(stmt)).scalars().all())

    async def get_or_create(
        self, business_id: str, platform: str, credentials: dict | None = None
    ) -> PlatformConnection:
        existing = await self.get_by_business_and_platform(business_id, platform)
        if existing:
            return existing

        conn = PlatformConnection(
            business_id=business_id,
            platform=platform,
            is_active=True,
            credentials=credentials or {},
            status="healthy",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )
        self.db.add(conn)
        await self.db.commit()
        await self.db.refresh(conn)
        return conn

    async def record_poll_result(
        self,
        business_id: str,
        platform: str,
        success: bool,
        fetched: int = 0,
        inserted: int = 0,
        skipped: int = 0,
        error: str | None = None,
        cursor: str | None = None,
    ) -> PlatformConnection:
        conn = await self.get_or_create(business_id, platform)
        now = datetime.now(UTC)

        conn.last_attempt_at = now
        conn.last_polled_at = now

        if success:
            conn.last_success_at = now
            conn.records_fetched += fetched
            conn.records_inserted += inserted
            conn.records_skipped += skipped
            conn.status = "healthy"
            conn.last_error = None
            if cursor:
                conn.cursor = cursor
        else:
            conn.error_count += 1
            conn.last_error = error
            conn.status = "error" if conn.error_count >= 3 else "warning"

        conn.updated_at = now
        await self.db.commit()
        await self.db.refresh(conn)
        return conn
