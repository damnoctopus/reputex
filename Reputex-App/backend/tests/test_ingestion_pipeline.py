"""Integration tests for IngestionService lifecycle, incremental polling state, and failure resilience."""

from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.business import BrandKeyword, Business
from app.repositories.ingestion_job_repository import IngestionJobRepository
from app.repositories.platform_repository import PlatformConnectionRepository
from app.services.ingestion_service import IngestionService


@pytest.mark.asyncio
async def test_ingestion_job_and_polling_state_lifecycle(db_session: AsyncSession):
    """Verify IngestionJob and PlatformConnection are accurately tracked across ingestion runs."""
    biz = Business(name="The Gourmet Kitchen", category="Restaurant", owner_id="user_gourmet")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    kw = BrandKeyword(business_id=biz.id, keyword="pasta", is_active=True)
    db_session.add(kw)
    await db_session.commit()

    service = IngestionService(db_session)
    job_repo = IngestionJobRepository(db_session)
    platform_repo = PlatformConnectionRepository(db_session)

    # 1. Run ingestion for Google
    result = await service.ingest_for_business_and_platform(biz.id, "Google")
    assert result.status == "SUCCESS"
    assert result.records_fetched >= 1
    assert result.records_inserted >= 1

    # 2. Verify IngestionJob audit record
    jobs = await job_repo.list_by_business(biz.id)
    assert len(jobs) == 1
    latest_job = jobs[0]
    assert latest_job.id == result.job_id
    assert latest_job.status == "SUCCESS"
    assert latest_job.records_fetched == result.records_fetched
    assert latest_job.records_inserted == result.records_inserted
    assert latest_job.completed_at is not None

    # 3. Verify PlatformConnection state
    conn = await platform_repo.get_by_business_and_platform(biz.id, "Google")
    assert conn is not None
    assert conn.is_active is True
    assert conn.status == "healthy"
    assert conn.last_polled_at is not None
    assert conn.last_success_at is not None
    assert conn.records_fetched == result.records_fetched
    assert conn.records_inserted == result.records_inserted
    assert conn.error_count == 0


@pytest.mark.asyncio
async def test_ingestion_failure_resilience(db_session: AsyncSession):
    """Verify connector network/HTTP failure is safely handled and logged without crashing."""
    biz = Business(name="Resilient Cafe", category="Cafe", owner_id="user_resilient")
    db_session.add(biz)
    await db_session.commit()
    await db_session.refresh(biz)

    service = IngestionService(db_session)
    platform_repo = PlatformConnectionRepository(db_session)
    job_repo = IngestionJobRepository(db_session)

    # Mock connector throwing an exception (e.g. Rate limit or connection timeout)
    with patch(
        "app.integrations.mock_connector.MockPlatformConnector.fetch_mentions",
        side_effect=RuntimeError("External API connection timed out"),
    ):
        result = await service.ingest_for_business_and_platform(biz.id, "Reddit")

    assert result.status == "FAILED"
    assert result.records_fetched == 0
    assert result.records_inserted == 0
    assert len(result.errors) > 0
    assert "External API connection timed out" in result.errors[0]

    # Check that job was marked FAILED
    jobs = await job_repo.list_by_business(biz.id, platform="Reddit")
    assert len(jobs) == 1
    assert jobs[0].status == "FAILED"
    assert "External API connection timed out" in (jobs[0].error_message or "")

    # Check that PlatformConnection recorded the error
    conn = await platform_repo.get_by_business_and_platform(biz.id, "Reddit")
    assert conn is not None
    assert conn.error_count == 1
    assert "External API connection timed out" in (conn.last_error or "")


@pytest.mark.asyncio
async def test_non_existent_business_handling(db_session: AsyncSession):
    """Verify ingestion gracefully aborts if business ID is invalid."""
    service = IngestionService(db_session)
    result = await service.ingest_for_business_and_platform("biz_non_existent", "X")
    assert result.status == "FAILED"
    assert "does not exist" in result.errors[0]


@pytest.mark.asyncio
async def test_periodic_active_businesses_discovery(db_session: AsyncSession):
    """Verify scheduled periodic ingestion scans businesses and dispatches tasks."""
    biz_1 = Business(name="Chain Store A", category="Retail", owner_id="owner_1")
    biz_2 = Business(name="Chain Store B", category="Retail", owner_id="owner_2")
    db_session.add_all([biz_1, biz_2])
    await db_session.commit()

    service = IngestionService(db_session)

    with patch("app.workers.tasks.ingest_platform_for_business.delay") as mock_delay:
        summary = await service.ingest_periodic_active_businesses()

    assert summary["status"] == "scheduled"
    assert summary["businesses_found"] >= 2
    # 2 businesses * 3 default platforms = at least 6 tasks dispatched
    assert summary["jobs_enqueued"] >= 6
    assert mock_delay.call_count >= 6
