"""Integration tests for Ingestion Deduplication Engine and Uniqueness Constraints."""

from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import Business
from app.models.mention import Mention
from app.repositories.mention_repository import MentionRepository
from app.schemas.ingestion import NormalizedMention
from app.services.ingestion_service import IngestionService


def _create_mock_normalized(
    business_id: str,
    platform: str,
    external_id: str,
    content: str,
    likes: int = 10,
) -> NormalizedMention:
    from app.services.normalizer import MentionNormalizer

    content_hash = MentionNormalizer.compute_content_hash(content)
    now = datetime.now(UTC)
    return NormalizedMention(
        business_id=business_id,
        platform=platform,
        external_id=external_id,
        content_hash=content_hash,
        author="Reviewer",
        content=content,
        url=f"https://{platform.lower()}.com/{external_id}",
        rating=4.5,
        language="en",
        engagement={"likes": likes, "shares": 2, "comments": 1},
        metadata_json={"test": True},
        published_at=now,
        collected_at=now,
    )


@pytest.mark.asyncio
async def test_in_batch_deduplication(db_session: AsyncSession):
    """Verify duplicates within the same batch are discarded before database insertion."""
    biz = Business(name="Dedupe Cafe", category="Restaurant", owner_id="user_1")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    repo = MentionRepository(db_session)

    # 4 distinct, plus 2 duplicates (total 6 records)
    batch = [
        _create_mock_normalized(biz.id, "Google", "g_1", "Great breakfast spot!"),
        _create_mock_normalized(biz.id, "Google", "g_2", "Pancakes were delicious."),
        _create_mock_normalized(biz.id, "Google", "g_1", "Great breakfast spot!"),  # Duplicate of g_1
        _create_mock_normalized(biz.id, "Reddit", "r_1", "Anyone tried Dedupe Cafe?"),
        _create_mock_normalized(biz.id, "Google", "g_3", "Coffee was fresh and hot."),
        _create_mock_normalized(biz.id, "Reddit", "r_1", "Anyone tried Dedupe Cafe?"),  # Duplicate of r_1
    ]

    persisted, inserted, skipped = await repo.upsert_mentions(biz.id, batch)

    assert inserted == 4
    assert skipped == 2
    assert len(persisted) == 4

    stmt = select(Mention).where(Mention.business_id == biz.id)
    all_in_db = list((await db_session.execute(stmt)).scalars().all())
    assert len(all_in_db) == 4


@pytest.mark.asyncio
async def test_repeated_ingestion_idempotency_the_10_mentions_test(db_session: AsyncSession):
    """CRITICAL SPECIFICATION TEST:

    Run the same mock ingestion job multiple times:
    Run 1: 10 fetched, 10 inserted, 0 skipped.
    Run 2: 10 fetched, 0 inserted, 10 skipped.
    Database still contains exactly 10 mentions.
    """
    biz = Business(name="Spice Symphony", category="Restaurant", owner_id="user_spice")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    service = IngestionService(db_session)

    # Initial Run
    result_1 = await service.ingest_for_business_and_platform(biz.id, "MockPlatform")
    assert result_1.status == "SUCCESS"
    assert result_1.records_fetched == 10
    assert result_1.records_inserted == 10
    assert result_1.records_skipped == 0

    stmt = select(Mention).where(Mention.business_id == biz.id)
    count_after_run_1 = len(list((await db_session.execute(stmt)).scalars().all()))
    assert count_after_run_1 == 10

    # Second Run (Identical batch fetched)
    result_2 = await service.ingest_for_business_and_platform(biz.id, "MockPlatform")
    assert result_2.status == "SUCCESS"
    assert result_2.records_fetched == 10
    assert result_2.records_inserted == 0
    assert result_2.records_skipped == 10

    # Final DB check: exactly 10 records remain, zero duplicates
    count_after_run_2 = len(list((await db_session.execute(stmt)).scalars().all()))
    assert count_after_run_2 == 10


@pytest.mark.asyncio
async def test_cross_tenant_external_id_isolation(db_session: AsyncSession):
    """Verify different businesses can ingest records with the same external_id without collision."""
    biz_a = Business(name="Biz Alpha", category="Retail", owner_id="user_a")
    biz_b = Business(name="Biz Beta", category="Retail", owner_id="user_b")
    db_session.add_all([biz_a, biz_b])
    await db_session.commit()
    await db_session.refresh(biz_a)
    await db_session.refresh(biz_b)

    repo = MentionRepository(db_session)

    # Ingest same external ID for Biz A
    record_a = [_create_mock_normalized(biz_a.id, "Google", "ext_shared_999", "Alpha review content")]
    _, ins_a, _ = await repo.upsert_mentions(biz_a.id, record_a)
    assert ins_a == 1

    # Ingest same external ID for Biz B
    record_b = [_create_mock_normalized(biz_b.id, "Google", "ext_shared_999", "Beta review content")]
    _, ins_b, _ = await repo.upsert_mentions(biz_b.id, record_b)
    assert ins_b == 1

    # Verify both businesses have their own record
    stmt_a = select(Mention).where(Mention.business_id == biz_a.id)
    stmt_b = select(Mention).where(Mention.business_id == biz_b.id)
    assert len(list((await db_session.execute(stmt_a)).scalars().all())) == 1
    assert len(list((await db_session.execute(stmt_b)).scalars().all())) == 1


@pytest.mark.asyncio
async def test_cross_platform_external_id_isolation(db_session: AsyncSession):
    """Verify same business can have identical external IDs if platforms differ."""
    biz = Business(name="Omni Brand", category="Tech", owner_id="user_omni")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    repo = MentionRepository(db_session)

    batch = [
        _create_mock_normalized(biz.id, "Google", "id_100", "Google review with ID 100"),
        _create_mock_normalized(biz.id, "Reddit", "id_100", "Reddit comment with ID 100"),
        _create_mock_normalized(biz.id, "X", "id_100", "X tweet with ID 100"),
    ]

    persisted, inserted, skipped = await repo.upsert_mentions(biz.id, batch)
    assert inserted == 3
    assert skipped == 0
    assert len(persisted) == 3


@pytest.mark.asyncio
async def test_upsert_updates_engagement_metrics(db_session: AsyncSession):
    """Verify repeated ingestion updates engagement metrics on existing record."""
    biz = Business(name="Trending Bistro", category="Food", owner_id="user_trend")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    repo = MentionRepository(db_session)

    # Initial record: 10 likes
    batch_1 = [_create_mock_normalized(biz.id, "X", "tw_trending_1", "Viral tweet about Bistro!", likes=10)]
    await repo.upsert_mentions(biz.id, batch_1)

    # Updated record: 500 likes
    batch_2 = [_create_mock_normalized(biz.id, "X", "tw_trending_1", "Viral tweet about Bistro!", likes=500)]
    await repo.upsert_mentions(biz.id, batch_2)

    stmt = select(Mention).where(Mention.business_id == biz.id, Mention.external_id == "tw_trending_1")
    mention = (await db_session.execute(stmt)).scalars().first()
    assert mention is not None
    assert mention.engagement["likes"] == 500
