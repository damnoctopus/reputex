"""Data Acquisition & Ingestion Orchestration Service for RepuTex."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.integrations.base import PlatformConnector
from app.integrations.google import GoogleConnector
from app.integrations.justdial import JustDialConnector
from app.integrations.mock_connector import MockPlatformConnector
from app.integrations.query_builder import PlatformQueryBuilder
from app.integrations.reddit import RedditConnector
from app.integrations.twitter import TwitterConnector
from app.models.business import Business
from app.repositories.business_repository import BusinessRepository
from app.repositories.ingestion_job_repository import IngestionJobRepository
from app.repositories.mention_repository import MentionRepository
from app.repositories.platform_repository import PlatformConnectionRepository
from app.schemas.ingestion import IngestionBatchResult, RawMentionRecord
from app.services.normalizer import MentionNormalizer


class IngestionService:
    """Orchestrates the data acquisition lifecycle:

    Keyword -> Query Builder -> Connector -> Raw Records -> Normalizer -> Deduplication Engine -> PostgreSQL Upsert
    -> Incremental Polling State -> Downstream Intelligence Dispatch.
    """

    CONNECTOR_MAP: dict[str, type[PlatformConnector]] = {
        "google": GoogleConnector,
        "google places": GoogleConnector,
        "reddit": RedditConnector,
        "x": TwitterConnector,
        "twitter": TwitterConnector,
        "justdial": JustDialConnector,
        "mockplatform": MockPlatformConnector,
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self.business_repo = BusinessRepository(db)
        self.mention_repo = MentionRepository(db)
        self.platform_repo = PlatformConnectionRepository(db)
        self.job_repo = IngestionJobRepository(db)

    def _resolve_connector(self, platform: str) -> PlatformConnector:
        """Instantiate appropriate connector based on platform and environment settings."""
        if settings.PLATFORM_MODE.lower() == "mock":
            return MockPlatformConnector(platform=platform)

        connector_cls = self.CONNECTOR_MAP.get(platform.strip().lower())
        if not connector_cls:
            logger.info(f"No dedicated connector for '{platform}'. Falling back to MockPlatformConnector.")
            return MockPlatformConnector(platform=platform)

        return connector_cls()

    async def ingest_for_business_and_platform(
        self,
        business_id: str,
        platform: str,
        force: bool = False,
    ) -> IngestionBatchResult:
        """Run an ingestion cycle for a specific business and external platform."""
        standard_platform = MentionNormalizer.normalize_platform_name(platform)

        # 1. Fetch business and active brand keywords
        business = await self.business_repo.get_by_id(business_id)
        if not business:
            logger.error(f"Ingestion aborted: Business '{business_id}' not found.")
            return IngestionBatchResult(
                job_id="none",
                business_id=business_id,
                platform=standard_platform,
                status="FAILED",
                records_fetched=0,
                records_normalized=0,
                records_inserted=0,
                records_skipped=0,
                errors=[f"Business '{business_id}' does not exist."],
            )

        keywords = await self.business_repo.list_keywords(business_id)
        keyword_tokens = [k.keyword for k in keywords] if keywords else []

        # 2. Retrieve or initialize platform connection state
        conn = await self.platform_repo.get_or_create(business_id, standard_platform)

        # Check rate-limit backoff
        now = datetime.now(UTC)
        if not force and conn.rate_limit_reset_at and conn.rate_limit_reset_at > now:
            logger.warning(
                f"Rate limit active for business {business_id} on {standard_platform} until {conn.rate_limit_reset_at}. Skipping."
            )
            return IngestionBatchResult(
                job_id="rate_limited",
                business_id=business_id,
                platform=standard_platform,
                status="SKIPPED",
                records_fetched=0,
                records_normalized=0,
                records_inserted=0,
                records_skipped=0,
                errors=[f"Rate limit active until {conn.rate_limit_reset_at}"],
            )

        # 3. Create job audit record (RUNNING)
        job = await self.job_repo.start_job(business_id, standard_platform)

        raw_records: list[RawMentionRecord] = []
        errors: list[str] = []

        # 4. Fetch raw records via connector
        try:
            connector = self._resolve_connector(standard_platform)

            # Build platform query for audit trail
            query = PlatformQueryBuilder.build_query(
                platform=standard_platform,
                business_name=business.name,
                keywords=keyword_tokens,
                location=business.location,
            )
            logger.info(
                f"Ingestion [{job.id}] fetching for {business.name} on {standard_platform} using query: {query.query_string}"
            )

            # Pass metadata (e.g. cached place_id) alongside credentials to connector.
            # credentials = API secrets; platform_meta = platform-specific cached state.
            connector_credentials = dict(conn.credentials)
            connector_credentials["_metadata"] = dict(conn.platform_meta) if conn.platform_meta else {}

            raw_records = await connector.fetch_mentions(
                business_name=business.name,
                keywords=keyword_tokens,
                since=conn.last_polled_at,
                cursor=conn.cursor,
                location=business.location,
                credentials=connector_credentials,
            )

            # If connector discovered new metadata (e.g. Google place_id), persist it
            if hasattr(connector, "get_discovered_metadata"):
                discovered = connector.get_discovered_metadata()
                if discovered:
                    conn.platform_meta = {**(conn.platform_meta or {}), **discovered}
                    await self.db.commit()
        except Exception as e:
            err_msg = f"Connector failure on {standard_platform} for business {business_id}: {e}"
            logger.exception(err_msg)
            errors.append(err_msg)

            await self.platform_repo.record_poll_result(
                business_id=business_id,
                platform=standard_platform,
                success=False,
                error=err_msg,
            )
            await self.job_repo.finish_job(
                job_id=job.id,
                status="FAILED",
                error_message=err_msg,
            )
            return IngestionBatchResult(
                job_id=job.id,
                business_id=business_id,
                platform=standard_platform,
                status="FAILED",
                records_fetched=0,
                records_normalized=0,
                records_inserted=0,
                records_skipped=0,
                errors=errors,
            )

        fetched_count = len(raw_records)

        # 5. Normalize raw records
        normalized_records, norm_errors = MentionNormalizer.normalize_batch(
            records=raw_records,
            business_id=business_id,
        )
        errors.extend(norm_errors)
        normalized_count = len(normalized_records)

        # 6. Atomic deduplication and persistence
        inserted_count = 0
        skipped_count = 0
        persisted_mentions = []

        if normalized_records:
            try:
                persisted_mentions, inserted_count, skipped_count = await self.mention_repo.upsert_mentions(
                    business_id=business_id,
                    normalized_mentions=normalized_records,
                )
            except Exception as e:
                err_msg = f"Database upsert error on {standard_platform} for {business_id}: {e}"
                logger.exception(err_msg)
                errors.append(err_msg)

                await self.platform_repo.record_poll_result(
                    business_id=business_id,
                    platform=standard_platform,
                    success=False,
                    fetched=fetched_count,
                    error=err_msg,
                )
                await self.job_repo.finish_job(
                    job_id=job.id,
                    status="FAILED",
                    records_fetched=fetched_count,
                    records_normalized=normalized_count,
                    error_message=err_msg,
                )
                return IngestionBatchResult(
                    job_id=job.id,
                    business_id=business_id,
                    platform=standard_platform,
                    status="FAILED",
                    records_fetched=fetched_count,
                    records_normalized=normalized_count,
                    records_inserted=0,
                    records_skipped=0,
                    errors=errors,
                )

        # Account for records skipped during normalization
        skipped_count += fetched_count - normalized_count

        # 7. Update platform connection polling metrics
        await self.platform_repo.record_poll_result(
            business_id=business_id,
            platform=standard_platform,
            success=True,
            fetched=fetched_count,
            inserted=inserted_count,
            skipped=skipped_count,
            cursor=conn.cursor,
        )

        # 8. Determine final job status
        final_status = "SUCCESS"
        if norm_errors:
            final_status = "PARTIAL"

        await self.job_repo.finish_job(
            job_id=job.id,
            status=final_status,
            records_fetched=fetched_count,
            records_normalized=normalized_count,
            records_inserted=inserted_count,
            records_skipped=skipped_count,
            error_message="; ".join(errors) if errors else None,
        )

        logger.info(
            f"Ingestion [{job.id}] completed: {fetched_count} fetched, {normalized_count} normalized, "
            f"{inserted_count} inserted, {skipped_count} skipped (status: {final_status})."
        )

        # 9. Trigger downstream intelligence processing integration hook
        if inserted_count > 0 and persisted_mentions:
            try:
                from app.workers.tasks import pipeline_process_mentions

                new_mention_ids = [m.id for m in persisted_mentions[:inserted_count]]
                pipeline_process_mentions.delay(business_id, new_mention_ids)
                logger.info(f"Dispatched intelligence pipeline hook for {len(new_mention_ids)} new mentions.")
            except Exception as e:
                logger.warning(f"Could not dispatch async intelligence hook: {e}")

        return IngestionBatchResult(
            job_id=job.id,
            business_id=business_id,
            platform=standard_platform,
            status=final_status,
            records_fetched=fetched_count,
            records_normalized=normalized_count,
            records_inserted=inserted_count,
            records_skipped=skipped_count,
            errors=errors,
        )

    async def ingest_for_business_all_active(self, business_id: str) -> list[IngestionBatchResult]:
        """Ingest across all configured platforms for a given business."""
        active_connections = await self.platform_repo.list_active_for_business(business_id)

        # Default platforms if none configured yet
        platforms_to_poll = (
            [c.platform for c in active_connections] if active_connections else ["Google", "Reddit", "X"]
        )

        results = []
        for p in platforms_to_poll:
            res = await self.ingest_for_business_and_platform(business_id, p)
            results.append(res)
        return results

    async def ingest_periodic_active_businesses(self) -> dict[str, Any]:
        """Discover active businesses and enqueue platform ingestion jobs."""
        from sqlalchemy import select

        stmt = select(Business.id)
        biz_ids = list((await self.db.execute(stmt)).scalars().all())

        enqueued_count = 0
        from app.workers.tasks import ingest_platform_for_business

        default_platforms = ["Google", "Reddit", "X"]

        for b_id in biz_ids:
            conns = await self.platform_repo.list_active_for_business(b_id)
            platforms = [c.platform for c in conns] if conns else default_platforms
            for plat in platforms:
                ingest_platform_for_business.delay(b_id, plat)
                enqueued_count += 1

        return {
            "status": "scheduled",
            "businesses_found": len(biz_ids),
            "jobs_enqueued": enqueued_count,
        }
