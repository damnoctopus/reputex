"""Issue Detection and Clustering domain service for customer problem discovery."""

import re
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.issue import Issue, IssueMention
from app.models.mention import Mention
from app.repositories.issue_repository import IssueRepository


class IssueDetectionService:
    """Discovers recurring issues from customer mentions across Google, Reddit, and X."""

    # Pre-defined domain categories and regex topic patterns
    CATEGORY_PATTERNS: dict[str, dict[str, list[str]]] = {
        "Customer Service": {
            "Long Wait Times & Queue Delay": [
                r"\bwait(?:ed|ing)?\b",
                r"\bdelay(?:ed)?\b",
                r"\bslow service\b",
                r"\bline\b",
                r"\bqueue\b",
                r"\bwaited forever\b",
                r"\btook (\d+|so) (?:min|minute|hour)s?\b",
            ],
            "Rude or Unhelpful Staff": [
                r"\brude\b",
                r"\barrogant\b",
                r"\bunhelpful\b",
                r"\battitude\b",
                r"\bmanager refused\b",
                r"\bdisrespectful\b",
                r"\bignored us\b",
                r"\bpoor customer service\b",
            ],
        },
        "Product & Service Quality": {
            "Food / Product Defect": [
                r"\bcold food\b",
                r"\bundercooked\b",
                r"\bovercooked\b",
                r"\btasteless\b",
                r"\bsalty\b",
                r"\bbad taste\b",
                r"\bdefective\b",
                r"\bbroken\b",
                r"\bpoor quality\b",
                r"\bstale\b",
                r"\bwrong order\b",
            ],
            "Inconsistent Experience": [
                r"\bused to be better\b",
                r"\bquality (?:dropped|declined|gone down)\b",
                r"\binconsistent\b",
                r"\bhit or miss\b",
            ],
        },
        "Billing & Pricing": {
            "Unexpected Fees & Surcharges": [
                r"\bhidden fee\b",
                r"\bsurcharge\b",
                r"\bovercharg(?:e|ed|ing)\b",
                r"\bextra charge\b",
                r"\bprice gouging\b",
                r"\bripoff\b",
                r"\brip off\b",
                r"\btoo expensive\b",
                r"\bnot worth\b",
            ],
            "Refund & Cancellation Issues": [
                r"\brefund\b",
                r"\bcancellation\b",
                r"\brefused to refund\b",
                r"\bchargeback\b",
                r"\bbilling issue\b",
            ],
        },
        "Hygiene & Cleanliness": {
            "Facility Cleanliness Concerns": [
                r"\bdirty\b",
                r"\bunclean\b",
                r"\bfilthy\b",
                r"\bsmell\b",
                r"\brestroom\b",
                r"\btoilet\b",
                r"\bhair in (?:food|plate)\b",
                r"\bhygiene\b",
                r"\bsanitation\b",
                r"\broach|cockroach|bug|insect\b",
            ],
        },
        "Operations & Fulfillment": {
            "Delivery & Order Fulfillment Delays": [
                r"\bdelivery delay(?:ed)?\b",
                r"\blate delivery\b",
                r"\bnever arrived\b",
                r"\bpackage lost\b",
                r"\bmissing items?\b",
                r"\bcancelled my order\b",
            ],
            "Booking & Reservation Glitches": [
                r"\breservation lost\b",
                r"\bbooking error\b",
                r"\btable not ready\b",
                r"\boverbooked\b",
            ],
        },
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.issue_repo = IssueRepository(db)

    async def detect_and_persist_issues(self, business_id: str) -> list[Issue]:
        """Scans all mentions for business_id, discovers issues, and persists them."""
        stmt = (
            select(Mention)
            .where(Mention.business_id == business_id)
            .order_by(Mention.published_at.desc())
        )
        mentions = list((await self.db.execute(stmt)).scalars().all())
        if not mentions:
            return []

        # Cluster mentions by (category, subtopic)
        issue_clusters: dict[tuple[str, str], list[tuple[Mention, str, float]]] = defaultdict(list)

        for mention in mentions:
            content_lower = mention.content.lower()
            # Mention must have negative or mixed sentiment or lower rating (<=3 stars)
            is_negative_sentiment = (mention.sentiment or "").lower() in {"negative", "mixed"}
            has_low_rating = mention.rating is not None and mention.rating <= 3.0
            sentiment_score_neg = mention.sentiment_score is not None and mention.sentiment_score < 0.0

            if not (is_negative_sentiment or has_low_rating or sentiment_score_neg):
                continue

            for category, subtopics in self.CATEGORY_PATTERNS.items():
                for subtopic, patterns in subtopics.items():
                    matched_patterns = []
                    for pat in patterns:
                        match = re.search(pat, content_lower)
                        if match:
                            matched_patterns.append(match.group(0))

                    if matched_patterns:
                        # Extract short excerpt around the match
                        snippet_match = re.search(
                            rf"(?:[\w\s]{{0,35}})(?:{'|'.join(patterns)})(?:[\w\s]{{0,45}})",
                            mention.content,
                            re.IGNORECASE,
                        )
                        excerpt = snippet_match.group(0).strip() if snippet_match else mention.content[:100]
                        relevance = min(1.0, 0.5 + (0.2 * len(matched_patterns)))
                        issue_clusters[(category, subtopic)].append((mention, excerpt, relevance))

        # Clear previous issues for fresh analysis
        await self.issue_repo.delete_for_business(business_id)

        persisted_issues: list[Issue] = []

        for (category, subtopic), clustered_items in issue_clusters.items():
            if not clustered_items:
                continue

            total_mentions = len(clustered_items)
            platforms_breakdown: dict[str, int] = defaultdict(int)
            sentiment_breakdown: dict[str, int] = defaultdict(int)

            timestamps = []
            for mention, _, _ in clustered_items:
                plat_key = mention.platform.capitalize()
                platforms_breakdown[plat_key] += 1
                sent_key = (mention.sentiment or "negative").lower()
                sentiment_breakdown[sent_key] += 1
                timestamps.append(mention.published_at)

            first_seen = min(timestamps) if timestamps else datetime.now(UTC)
            last_seen = max(timestamps) if timestamps else datetime.now(UTC)

            # Determine severity
            if total_mentions >= 8 or category in {"Hygiene & Cleanliness"}:
                severity = "critical"
            elif total_mentions >= 4:
                severity = "high"
            elif total_mentions >= 2:
                severity = "medium"
            else:
                severity = "low"

            # Determine status
            now = datetime.now(UTC)
            hours_since_last = (now - last_seen).total_seconds() / 3600.0 if last_seen else 999.0
            if hours_since_last <= 48 and total_mentions >= 2:
                status = "active"
            elif hours_since_last <= 168:
                status = "emerging"
            else:
                status = "resolved"

            issue = Issue(
                business_id=business_id,
                category=category,
                subtopic=subtopic,
                severity=severity,
                status=status,
                mention_count=total_mentions,
                platforms_breakdown=dict(platforms_breakdown),
                sentiment_breakdown=dict(sentiment_breakdown),
                first_seen_at=first_seen,
                last_seen_at=last_seen,
            )

            evidence_records = [
                IssueMention(
                    mention_id=mention.id,
                    relevance_score=relevance,
                    excerpt=excerpt,
                    created_at=datetime.now(UTC),
                )
                for mention, excerpt, relevance in clustered_items
            ]

            saved = await self.issue_repo.save_issue(issue, evidence_records)
            persisted_issues.append(saved)

        return persisted_issues

    async def list_issues(
        self,
        business_id: str,
        category: str | None = None,
        severity: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Issue]:
        return await self.issue_repo.list_by_business(
            business_id=business_id,
            category=category,
            severity=severity,
            status=status,
            limit=limit,
            offset=offset,
        )

    async def get_issue_by_id(self, issue_id: str, business_id: str) -> Issue | None:
        return await self.issue_repo.get_by_id_and_business(issue_id, business_id)
