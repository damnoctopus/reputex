"""Mention persistence, atomic deduplication, and query service."""
from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.acquisition.base import RawMentionRecord
from app.acquisition.normalizer import Normalizer
from app.core.exceptions import NotFoundError
from app.models.mention import Mention
from app.schemas.mention import MentionEngagement, MentionResponse, PaginatedMentions


class MentionService:
    @staticmethod
    async def upsert_raw_mentions(
        db: AsyncSession,
        business_id: str,
        records: List[RawMentionRecord],
    ) -> Tuple[int, int]:
        """Deduplicate and insert new mentions. Returns (mentions_found, mentions_added)."""
        if not records:
            return 0, 0

        mentions_found = len(records)
        mentions_added = 0

        # Load existing external_ids and content_hashes for this business
        ext_ids = [str(r.external_id) for r in records]
        content_hashes = [
            Normalizer.compute_content_hash(r.platform, r.author, r.content)
            for r in records
        ]

        stmt = select(Mention.external_id, Mention.content_hash).where(
            Mention.business_id == business_id,
            or_(Mention.external_id.in_(ext_ids), Mention.content_hash.in_(content_hashes)),
        )
        res = await db.execute(stmt)
        existing_rows = res.all()
        existing_ext_ids = {r[0] for r in existing_rows}
        existing_hashes = {r[1] for r in existing_rows}

        for r in records:
            ext_id = str(r.external_id)
            c_hash = Normalizer.compute_content_hash(r.platform, r.author, r.content)
            if ext_id in existing_ext_ids or c_hash in existing_hashes:
                continue

            mention_model = Normalizer.to_mention_model(r, business_id)
            db.add(mention_model)
            existing_ext_ids.add(ext_id)
            existing_hashes.add(c_hash)
            mentions_added += 1

        if mentions_added > 0:
            await db.commit()

        return mentions_found, mentions_added

    @staticmethod
    async def get_paginated(
        db: AsyncSession,
        business_id: str,
        page: int = 1,
        limit: int = 20,
        platform: Optional[str] = None,
        sentiment: Optional[str] = None,
        is_fake: Optional[bool] = None,
        q: Optional[str] = None,
        sort_by: str = "latest",
    ) -> PaginatedMentions:
        query = select(Mention).where(Mention.business_id == business_id)

        if platform and platform.lower() != "all":
            query = query.where(Mention.platform == platform.lower())
        if sentiment and sentiment.lower() != "all":
            query = query.where(Mention.sentiment == sentiment.lower())
        if is_fake is not None:
            query = query.where(Mention.is_fake == is_fake)
        if q and q.strip():
            query = query.where(Mention.content.ilike(f"%{q.strip()}%"))

        # Count total
        count_stmt = select(func.count()).select_from(query.subquery())
        total = (await db.execute(count_stmt)).scalar_one()

        # Ordering
        if sort_by == "rating_high":
            query = query.order_by(Mention.rating.desc().nullslast(), Mention.published_at.desc())
        elif sort_by == "rating_low":
            query = query.order_by(Mention.rating.asc().nullslast(), Mention.published_at.desc())
        else:
            query = query.order_by(Mention.published_at.desc())

        # Pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        result = await db.execute(query)
        items = list(result.scalars().all())

        response_items = []
        for m in items:
            eng = MentionEngagement(**(m.engagement or {}))
            response_items.append(MentionResponse(
                id=m.id,
                platform=m.platform,
                author=m.author,
                content=m.content,
                sentiment=m.sentiment,
                sentiment_score=m.sentiment_score,
                is_fake=m.is_fake,
                fraud_confidence=m.fraud_confidence,
                url=m.url,
                timestamp=m.published_at,
                engagement=eng,
                rating=m.rating,
                response_status=m.response_status,
                response_text=m.response_text,
                author_avatar=m.author_avatar,
            ))

        total_pages = max(1, (total + limit - 1) // limit)
        return PaginatedMentions(
            items=response_items,
            total=total,
            total_count=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_more=page < total_pages,
        )

    @staticmethod
    async def get_by_id(db: AsyncSession, business_id: str, mention_id: str) -> Mention:
        stmt = select(Mention).where(Mention.id == mention_id, Mention.business_id == business_id)
        res = await db.execute(stmt)
        m = res.scalar_one_or_none()
        if not m:
            raise NotFoundError("Mention", mention_id)
        return m
