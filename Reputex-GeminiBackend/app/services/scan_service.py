"""Scan execution service coordinating the state machine asynchronously."""
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.acquisition.gemini_search_provider import GeminiSearchProvider
from app.core.database import AsyncSessionLocal
from app.core.exceptions import NotFoundError
from app.models.business import Business, BrandKeyword
from app.models.scan import Scan
from app.schemas.scan import ScanStatusResponse, ScanTriggerResponse
from app.services.authenticity_service import ReviewAuthenticityService
from app.services.crisis_service import CrisisService
from app.services.findings_service import FindingsService
from app.services.intelligence_service import IntelligenceService
from app.services.issue_detection_service import IssueDetectionService
from app.services.mention_service import MentionService
from app.services.reputation_service import ReputationService

logger = logging.getLogger("reputex.scan")


class ScanService:
    @staticmethod
    async def trigger_scan(
        db: AsyncSession,
        business_id: str,
        background_tasks=None,
    ) -> ScanTriggerResponse:
        """Create a scan record with status PENDING and launch in-process background execution."""
        biz_stmt = select(Business).where(Business.id == business_id)
        biz = (await db.execute(biz_stmt)).scalar_one_or_none()
        if not biz:
            raise NotFoundError("Business", business_id)

        scan = Scan(
            business_id=business_id,
            status="PENDING",
            current_step="Scan Queued",
            google_status="PENDING",
            reddit_status="PENDING",
            x_status="PENDING",
            progress_pct=5,
        )
        db.add(scan)
        await db.commit()
        await db.refresh(scan)

        if background_tasks:
            background_tasks.add_task(ScanService.execute_scan_workflow, scan.id, business_id)
        else:
            asyncio.create_task(ScanService.execute_scan_workflow(scan.id, business_id))

        return ScanTriggerResponse(
            scan_id=scan.id,
            status="PENDING",
            message="Scan initiated successfully. Acquiring recent public mentions.",
            business_id=business_id,
        )

    @staticmethod
    async def _run_workflow_with_db(db: AsyncSession, scan_id: str, business_id: str) -> None:
        scan = await db.get(Scan, scan_id)
        if not scan:
            return

        try:
            # Step 1: RUNNING
            scan.status = "RUNNING"
            scan.current_step = "Initializing scan parameters"
            scan.progress_pct = 10
            await db.commit()

            biz = await db.get(Business, business_id)
            biz_name = biz.name if biz else "Spice Symphony"
            biz_loc = biz.location if biz else None
            kw_res = await db.execute(select(BrandKeyword.keyword).where(BrandKeyword.business_id == business_id))
            keywords = list(kw_res.scalars().all())

            # Step 2: ACQUIRING
            scan.status = "ACQUIRING"
            scan.current_step = "Searching recent public mentions across Google, Reddit, and X"
            scan.google_status = "IN_PROGRESS"
            scan.reddit_status = "IN_PROGRESS"
            scan.x_status = "IN_PROGRESS"
            scan.progress_pct = 25
            await db.commit()

            provider = GeminiSearchProvider()
            raw_records = provider.acquire(
                business_name=biz_name,
                location=biz_loc,
                keywords=keywords,
            )

            scan.google_status = "COMPLETED"
            scan.reddit_status = "COMPLETED"
            scan.x_status = "COMPLETED"
            scan.mentions_found = len(raw_records)
            scan.progress_pct = 45
            await db.commit()

            found, added = await MentionService.upsert_raw_mentions(db, business_id, raw_records)
            scan.mentions_added = added
            scan.progress_pct = 55
            await db.commit()

            # Step 3: ANALYZING
            scan.status = "ANALYZING"
            scan.current_step = "Running Gemini batched semantic analysis"
            scan.progress_pct = 65
            await db.commit()

            await IntelligenceService.analyze_pending_mentions(db, business_id)
            scan.progress_pct = 80
            await db.commit()

            # Step 4: AGGREGATING
            scan.status = "AGGREGATING"
            scan.current_step = "Clustering issues, evaluating authenticity, and calculating crisis metrics"
            scan.progress_pct = 85
            await db.commit()

            await IssueDetectionService.cluster_and_aggregate_issues(db, business_id)
            await ReviewAuthenticityService.evaluate_authenticity(db, business_id)
            await CrisisService.evaluate_crisis(db, business_id)
            await ReputationService.compute_reputation_score(db, business_id)
            await FindingsService.generate_findings(db, business_id)

            # Step 5: COMPLETED
            scan.status = "COMPLETED"
            scan.current_step = "Scan completed successfully with evidence findings"
            scan.progress_pct = 100
            scan.completed_at = datetime.now(timezone.utc)
            await db.commit()

        except Exception as e:
            logger.exception(f"Scan {scan_id} failed: {e}")
            scan.status = "FAILED"
            scan.current_step = "Scan failed"
            scan.error_summary = str(e)
            scan.completed_at = datetime.now(timezone.utc)
            await db.commit()

    @staticmethod
    async def execute_scan_workflow(scan_id: str, business_id: str, session: Optional[AsyncSession] = None) -> None:
        """State machine: PENDING -> RUNNING -> ACQUIRING -> ANALYZING -> AGGREGATING -> COMPLETED."""
        if session is not None:
            await ScanService._run_workflow_with_db(session, scan_id, business_id)
        else:
            async with AsyncSessionLocal() as db:
                await ScanService._run_workflow_with_db(db, scan_id, business_id)

    @staticmethod
    async def get_scan_status(db: AsyncSession, business_id: str, scan_id: Optional[str] = None) -> ScanStatusResponse:
        if scan_id:
            stmt = select(Scan).where(Scan.id == scan_id, Scan.business_id == business_id)
        else:
            stmt = select(Scan).where(Scan.business_id == business_id).order_by(Scan.started_at.desc())

        res = await db.execute(stmt)
        scan = res.scalar_one_or_none()
        if not scan:
            return ScanStatusResponse(
                scan_id="none",
                business_id=business_id,
                status="COMPLETED",
                current_step="Ready for scan",
                google_status="COMPLETED",
                reddit_status="COMPLETED",
                x_status="COMPLETED",
                mentions_found=0,
                mentions_added=0,
                progress_pct=100,
                started_at=datetime.now(timezone.utc),
            )

        return ScanStatusResponse(
            scan_id=scan.id,
            business_id=scan.business_id,
            status=scan.status,
            current_step=scan.current_step,
            google_status=scan.google_status,
            reddit_status=scan.reddit_status,
            x_status=scan.x_status,
            mentions_found=scan.mentions_found,
            mentions_added=scan.mentions_added,
            progress_pct=scan.progress_pct,
            started_at=scan.started_at,
            completed_at=scan.completed_at,
            error_summary=scan.error_summary,
        )
