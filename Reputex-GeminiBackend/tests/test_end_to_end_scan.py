"""End-to-end full scan workflow test verifying complete pipeline."""
import pytest
from app.services.scan_service import ScanService


@pytest.mark.asyncio
async def test_full_scan_pipeline_mock(db_session, test_business):
    trigger = await ScanService.trigger_scan(db_session, test_business.id)
    assert trigger.status == "PENDING"
    assert trigger.scan_id != "none"

    # Execute workflow directly with test db session
    await ScanService.execute_scan_workflow(trigger.scan_id, test_business.id, session=db_session)

    # Check status
    status = await ScanService.get_scan_status(db_session, test_business.id, trigger.scan_id)
    assert status.status == "COMPLETED"
    assert status.mentions_found == 75
    assert status.mentions_added >= 70
    assert status.progress_pct == 100
