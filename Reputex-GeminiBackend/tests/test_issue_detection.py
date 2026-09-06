"""Tests for semantic issue clustering and cross-platform aggregation."""
from datetime import datetime, timezone
import pytest
from app.acquisition.base import RawMentionRecord
from app.services.intelligence_service import IntelligenceService
from app.services.issue_detection_service import IssueDetectionService
from app.services.mention_service import MentionService


@pytest.mark.asyncio
async def test_issue_clustering_cross_platform(db_session, test_business):
    records = [
        RawMentionRecord(
            platform="google",
            external_id="iss_g1",
            content="Rude staff ignored us at the table.",
            published_at=datetime.now(timezone.utc),
        ),
        RawMentionRecord(
            platform="reddit",
            external_id="iss_r1",
            content="Can confirm rude staff and terrible attitudes.",
            published_at=datetime.now(timezone.utc),
        ),
    ]
    await MentionService.upsert_raw_mentions(db_session, test_business.id, records)
    await IntelligenceService.analyze_pending_mentions(db_session, test_business.id)

    issues = await IssueDetectionService.cluster_and_aggregate_issues(db_session, test_business.id)
    assert len(issues) >= 1

    staff_issue = next((iss for iss in issues if "Staff" in iss.subtopic or "Customer Service" in iss.category), None)
    assert staff_issue is not None
    assert staff_issue.mention_count >= 1
    assert "google" in staff_issue.platforms_breakdown or "reddit" in staff_issue.platforms_breakdown
