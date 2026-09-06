"""Mention repository supporting pagination, multi-facet filtering, and sorting."""

import math

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mention import Mention
from app.repositories.base import BaseRepository
from app.schemas.ingestion import NormalizedMention
from app.schemas.mention import MentionsFilterParams


class MentionRepository(BaseRepository[Mention]):
    def __init__(self, db: AsyncSession):
        super().__init__(Mention, db)

    async def get_by_business_and_id(self, business_id: str, mention_id: str) -> Mention | None:
        result = await self.db.execute(
            select(Mention).where(
                Mention.business_id == business_id,
                Mention.id == mention_id,
            )
        )
        return result.scalars().first()

    async def list_paginated(
        self,
        business_id: str,
        filter_params: MentionsFilterParams,
        reviews_only: bool = False,
    ) -> tuple[list[Mention], int, int, bool]:
        """Returns (items, total_count, total_pages, has_more) based on filter query."""
        stmt = select(Mention).where(Mention.business_id == business_id)

        if reviews_only:
            stmt = stmt.where(Mention.rating.isnot(None))

        # Platform filter
        if filter_params.platform and filter_params.platform.lower() != "all":
            stmt = stmt.where(func.lower(Mention.platform) == filter_params.platform.lower())

        # Sentiment filter
        if filter_params.sentiment and filter_params.sentiment.lower() != "all":
            stmt = stmt.where(func.lower(Mention.sentiment) == filter_params.sentiment.lower())

        # Fake review filter
        if filter_params.is_fake is not None:
            stmt = stmt.where(Mention.is_fake == filter_params.is_fake)

        # Keyword search
        if filter_params.q and filter_params.q.strip():
            query_term = f"%{filter_params.q.strip().lower()}%"
            stmt = stmt.where(
                func.lower(Mention.content).like(query_term) | func.lower(Mention.author).like(query_term)
            )

        # Total count query
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = (await self.db.execute(count_stmt)).scalar() or 0

        # Sorting
        sort_by = filter_params.sort_by.lower()
        if sort_by == "oldest":
            stmt = stmt.order_by(Mention.published_at.asc())
        elif sort_by == "highest_rating":
            stmt = stmt.order_by(Mention.rating.desc().nullslast(), Mention.published_at.desc())
        elif sort_by == "lowest_rating":
            stmt = stmt.order_by(Mention.rating.asc().nullslast(), Mention.published_at.desc())
        else:  # newest (default)
            stmt = stmt.order_by(Mention.published_at.desc())

        # Pagination offsets
        page = max(1, filter_params.page)
        limit = max(1, filter_params.limit)
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())

        total_pages = max(1, math.ceil(total_count / limit)) if total_count > 0 else 1
        has_more = page < total_pages

        return items, total_count, total_pages, has_more

    async def bulk_create(self, mentions: list[Mention]) -> list[Mention]:
        self.db.add_all(mentions)
        await self.db.commit()
        for m in mentions:
            await self.db.refresh(m)
        return mentions

    async def upsert_mentions(
        self,
        business_id: str,
        normalized_mentions: list["NormalizedMention"],
    ) -> tuple[list[Mention], int, int]:
        """Idempotently insert or update mentions with in-batch and database-level deduplication.

        Returns: (persisted_mentions, inserted_count, skipped_or_updated_count)
        """
        if not normalized_mentions:
            return [], 0, 0

        # 1. Application-level in-batch deduplication
        deduped_batch: list[NormalizedMention] = []
        seen_keys: set[tuple[str, str]] = set()
        seen_hashes: set[str] = set()

        for m in normalized_mentions:
            key = (m.platform.lower(), m.external_id.lower())
            h = m.content_hash
            if key not in seen_keys and h not in seen_hashes:
                seen_keys.add(key)
                seen_hashes.add(h)
                deduped_batch.append(m)

        if not deduped_batch:
            return [], 0, len(normalized_mentions)

        # 2. Identify pre-existing records to calculate exact inserted vs skipped counts
        ext_ids = [m.external_id for m in deduped_batch]
        platforms = list({m.platform for m in deduped_batch})

        existing_stmt = select(Mention.platform, Mention.external_id).where(
            Mention.business_id == business_id,
            Mention.platform.in_(platforms),
            Mention.external_id.in_(ext_ids),
        )
        existing_rows = set((await self.db.execute(existing_stmt)).all())
        existing_pairs = {(p.lower(), e.lower()) for p, e in existing_rows}

        inserted_count = 0
        updated_count = 0

        # 3. Native atomic upsert via dialect-specific ON CONFLICT DO UPDATE
        bind = self.db.get_bind()
        dialect_name = bind.dialect.name if bind else "sqlite"

        if dialect_name == "postgresql":
            from sqlalchemy.dialects.postgresql import insert as dialect_insert
        else:
            from sqlalchemy.dialects.sqlite import insert as dialect_insert

        persisted: list[Mention] = []
        for m in deduped_batch:
            is_new = (m.platform.lower(), m.external_id.lower()) not in existing_pairs
            if is_new:
                inserted_count += 1
            else:
                updated_count += 1

            insert_values = {
                "business_id": business_id,
                "platform": m.platform,
                "external_id": m.external_id,
                "content_hash": m.content_hash,
                "author": m.author,
                "author_avatar": m.author_avatar,
                "content": m.content,
                "url": m.url,
                "rating": m.rating,
                "language": m.language,
                "engagement": m.engagement,
                "metadata_json": m.metadata_json,
                "published_at": m.published_at,
                "collected_at": m.collected_at,
            }

            stmt = dialect_insert(Mention).values(**insert_values)
            upsert_action = stmt.on_conflict_do_update(
                index_elements=["business_id", "platform", "external_id"],
                set_={
                    "engagement": stmt.excluded.engagement,
                    "collected_at": stmt.excluded.collected_at,
                    "url": func.coalesce(stmt.excluded.url, Mention.url),
                    "author_avatar": func.coalesce(stmt.excluded.author_avatar, Mention.author_avatar),
                },
            )
            await self.db.execute(upsert_action)

        await self.db.commit()

        # In-batch duplicate discards count as skipped
        total_skipped = updated_count + (len(normalized_mentions) - len(deduped_batch))

        # Query all processed mentions
        final_stmt = select(Mention).where(
            Mention.business_id == business_id,
            Mention.external_id.in_(ext_ids),
        )
        persisted = list((await self.db.execute(final_stmt)).scalars().all())

        return persisted, inserted_count, total_skipped
