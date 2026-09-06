"""Finding repository for managing findings and finding evidence."""

from collections.abc import Sequence

from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.finding import Finding, FindingEvidence
from app.repositories.base import BaseRepository


class FindingRepository(BaseRepository[Finding]):
    def __init__(self, db: AsyncSession):
        super().__init__(Finding, db)

    async def get_by_id_and_business(self, finding_id: str, business_id: str) -> Finding | None:
        """Fetch a finding with evidence records for a specific business."""
        result = await self.db.execute(
            select(Finding)
            .options(selectinload(Finding.evidence))
            .where(Finding.id == finding_id, Finding.business_id == business_id)
        )
        return result.scalars().first()

    async def list_by_business(
        self,
        business_id: str,
        finding_type: str | None = None,
        severity: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Finding]:
        """List findings for a business ordered by detected_at desc."""
        stmt = (
            select(Finding)
            .options(selectinload(Finding.evidence))
            .where(Finding.business_id == business_id)
        )
        if finding_type:
            stmt = stmt.where(Finding.finding_type == finding_type)
        if severity:
            stmt = stmt.where(Finding.severity == severity)

        stmt = stmt.order_by(desc(Finding.detected_at)).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete_for_business(self, business_id: str, finding_type: str | None = None) -> int:
        """Delete findings for a business, optionally filtered by finding_type."""
        stmt = delete(Finding).where(Finding.business_id == business_id)
        if finding_type:
            stmt = stmt.where(Finding.finding_type == finding_type)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount  # type: ignore[return-value]

    async def save_finding(self, finding: Finding, evidence_records: Sequence[FindingEvidence]) -> Finding:
        """Save a finding and its linked evidence records in a transaction."""
        self.db.add(finding)
        await self.db.flush()
        for ev in evidence_records:
            ev.finding_id = finding.id
            self.db.add(ev)
        await self.db.commit()
        await self.db.refresh(finding)
        return finding
