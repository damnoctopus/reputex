"""Issue repository for managing issues and issue evidence."""

from collections.abc import Sequence

from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.issue import Issue, IssueMention
from app.repositories.base import BaseRepository


class IssueRepository(BaseRepository[Issue]):
    def __init__(self, db: AsyncSession):
        super().__init__(Issue, db)

    async def get_by_id_and_business(self, issue_id: str, business_id: str) -> Issue | None:
        """Fetch an issue with its linked mention evidence for a specific business."""
        result = await self.db.execute(
            select(Issue)
            .options(selectinload(Issue.evidence))
            .where(Issue.id == issue_id, Issue.business_id == business_id)
        )
        return result.scalars().first()

    async def list_by_business(
        self,
        business_id: str,
        category: str | None = None,
        severity: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Issue]:
        """List issues for a business ordered by mention_count desc and severity."""
        stmt = (
            select(Issue)
            .options(selectinload(Issue.evidence))
            .where(Issue.business_id == business_id)
        )
        if category:
            stmt = stmt.where(Issue.category == category)
        if severity:
            stmt = stmt.where(Issue.severity == severity)
        if status:
            stmt = stmt.where(Issue.status == status)

        stmt = stmt.order_by(desc(Issue.mention_count), desc(Issue.last_seen_at)).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def delete_for_business(self, business_id: str) -> int:
        """Delete all existing issues for a business (cascade removes evidence)."""
        result = await self.db.execute(delete(Issue).where(Issue.business_id == business_id))
        await self.db.commit()
        return result.rowcount  # type: ignore[return-value]

    async def save_issue(self, issue: Issue, evidence_records: Sequence[IssueMention]) -> Issue:
        """Save an issue and its linked evidence records in a transaction."""
        self.db.add(issue)
        await self.db.flush()
        for ev in evidence_records:
            ev.issue_id = issue.id
            self.db.add(ev)
        await self.db.commit()
        await self.db.refresh(issue)
        return issue
