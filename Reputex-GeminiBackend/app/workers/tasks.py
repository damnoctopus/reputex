"""Celery background tasks with strict error isolation."""
import asyncio
import logging
from app.services.scan_service import ScanService
from app.workers.celery_app import celery_app

logger = logging.getLogger("reputex.tasks")


@celery_app.task(bind=True, name="tasks.scan_business_full")
def scan_business_full(self, scan_id: str, business_id: str):
    """Execute complete scan pipeline inside Celery worker."""
    logger.info(f"Starting Celery scan task for scan_id={scan_id}, business_id={business_id}")
    try:
        asyncio.run(ScanService.execute_scan_workflow(scan_id, business_id))
        return {"status": "SUCCESS", "scan_id": scan_id}
    except Exception as e:
        logger.exception(f"Celery task failed: {e}")
        return {"status": "FAILED", "error": str(e)}
