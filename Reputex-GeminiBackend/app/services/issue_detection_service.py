"""Semantic issue clustering and cross-platform aggregation service."""
from datetime import datetime, timezone
from typing import Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError
from app.models.issue import CustomerIssue, IssueEvidence
from app.models.mention import Mention
from app.schemas.issue import CustomerIssueResponse, IssueEvidenceResponse


class IssueDetectionService:
    @staticmethod
    async def cluster_and_aggregate_issues(db: AsyncSession, business_id: str) -> List[CustomerIssue]:
        """Extract and group issues from analyzed mentions, compute cross-platform stats, and store evidence."""
        stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.ai_status == "COMPLETE",
        ).order_by(Mention.published_at.asc())

        mentions = list((await db.execute(stmt)).scalars().all())

        # Group by (category, subtopic)
        groups: Dict[tuple, Dict] = {}

        for m in mentions:
            meta = m.metadata_json or {}
            issues = meta.get("extracted_issues", [])
            for iss in issues:
                cat = iss.get("category", "General")
                sub = iss.get("subtopic", "Unspecified Problem")
                sev = iss.get("severity", "medium")
                excerpt = iss.get("excerpt") or m.content[:140]

                key = (cat.strip(), sub.strip())
                if key not in groups:
                    groups[key] = {
                        "category": cat.strip(),
                        "subtopic": sub.strip(),
                        "severity": sev,
                        "platforms": {},
                        "sentiments": {},
                        "mentions": [],
                        "first_seen": m.published_at,
                        "last_seen": m.published_at,
                    }

                g = groups[key]
                # Update platforms
                g["platforms"][m.platform] = g["platforms"].get(m.platform, 0) + 1
                # Update sentiments
                g["sentiments"][m.sentiment] = g["sentiments"].get(m.sentiment, 0) + 1
                # Update timestamps
                if m.published_at < g["first_seen"]:
                    g["first_seen"] = m.published_at
                if m.published_at > g["last_seen"]:
                    g["last_seen"] = m.published_at

                # Evidence link
                g["mentions"].append((m.id, excerpt))

        # Clear existing issues for clean atomic aggregation
        existing_issues_stmt = select(CustomerIssue).where(CustomerIssue.business_id == business_id)
        existing_issues = list((await db.execute(existing_issues_stmt)).scalars().all())
        for ei in existing_issues:
            await db.delete(ei)
        await db.flush()

        created_issues: List[CustomerIssue] = []
        for (cat, sub), data in groups.items():
            cnt = sum(data["platforms"].values())
            # Determine status
            status = "active" if cnt >= 5 else "emerging"

            issue = CustomerIssue(
                business_id=business_id,
                category=data["category"],
                subtopic=data["subtopic"],
                severity=data["severity"],
                status=status,
                mention_count=cnt,
                platforms_breakdown=data["platforms"],
                sentiment_breakdown=data["sentiments"],
                first_seen_at=data["first_seen"],
                last_seen_at=data["last_seen"],
            )
            db.add(issue)
            await db.flush()

            # Add up to 5 top evidence mentions
            seen_mention_ids = set()
            for m_id, excerpt in data["mentions"]:
                if m_id in seen_mention_ids:
                    continue
                seen_mention_ids.add(m_id)
                db.add(IssueEvidence(
                    issue_id=issue.id,
                    mention_id=m_id,
                    relevance_score=1.0,
                    excerpt=excerpt,
                ))
                if len(seen_mention_ids) >= 5:
                    break

            created_issues.append(issue)

        await db.commit()
        return created_issues

    @staticmethod
    async def get_issues(
        db: AsyncSession,
        business_id: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[CustomerIssueResponse]:
        stmt = select(CustomerIssue).where(CustomerIssue.business_id == business_id).options(selectinload(CustomerIssue.evidence))

        if category and category.lower() != "all":
            stmt = stmt.where(CustomerIssue.category == category)
        if severity and severity.lower() != "all":
            stmt = stmt.where(CustomerIssue.severity == severity.lower())
        if status and status.lower() != "all":
            stmt = stmt.where(CustomerIssue.status == status.lower())

        stmt = stmt.order_by(CustomerIssue.mention_count.desc())
        res = await db.execute(stmt)
        issues = list(res.scalars().all())

        results = []
        for iss in issues:
            ev_items = [
                IssueEvidenceResponse(
                    id=e.id,
                    mention_id=e.mention_id,
                    relevance_score=e.relevance_score,
                    excerpt=e.excerpt,
                    created_at=e.created_at,
                )
                for e in iss.evidence
            ]
            results.append(CustomerIssueResponse(
                id=iss.id,
                business_id=iss.business_id,
                category=iss.category,
                subtopic=iss.subtopic,
                severity=iss.severity,
                status=iss.status,
                mention_count=iss.mention_count,
                platforms_breakdown=iss.platforms_breakdown or {},
                sentiment_breakdown=iss.sentiment_breakdown or {},
                first_seen_at=iss.first_seen_at,
                last_seen_at=iss.last_seen_at,
                evidence=ev_items,
            ))
        return results

    @staticmethod
    async def get_issue_by_id(db: AsyncSession, business_id: str, issue_id: str) -> CustomerIssueResponse:
        stmt = select(CustomerIssue).where(
            CustomerIssue.id == issue_id,
            CustomerIssue.business_id == business_id,
        ).options(selectinload(CustomerIssue.evidence))
        res = await db.execute(stmt)
        iss = res.scalar_one_or_none()
        if not iss:
            raise NotFoundError("CustomerIssue", issue_id)

        ev_items = [
            IssueEvidenceResponse(
                id=e.id,
                mention_id=e.mention_id,
                relevance_score=e.relevance_score,
                excerpt=e.excerpt,
                created_at=e.created_at,
            )
            for e in iss.evidence
        ]
        return CustomerIssueResponse(
            id=iss.id,
            business_id=iss.business_id,
            category=iss.category,
            subtopic=iss.subtopic,
            severity=iss.severity,
            status=iss.status,
            mention_count=iss.mention_count,
            platforms_breakdown=iss.platforms_breakdown or {},
            sentiment_breakdown=iss.sentiment_breakdown or {},
            first_seen_at=iss.first_seen_at,
            last_seen_at=iss.last_seen_at,
            evidence=ev_items,
        )
