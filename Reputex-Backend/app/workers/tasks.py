"""Background tasks for RepuTex asynchronous pipeline (Migrated from Celery)."""

import asyncio
from typing import Any
import traceback

from app.core.database import AsyncSessionLocal
from app.core.logging import logger

# NOTE: Removed celery_app imports and @celery_app.task decorators.
# All functions are now plain async functions that manage their own db sessions
# from the global AsyncSessionLocal factory.


async def schedule_periodic_ingestion() -> dict[str, Any]:
    """Periodic trigger to discover active businesses and dispatch platform workers."""
    async with AsyncSessionLocal() as session:
        from app.services.ingestion_service import IngestionService
        service = IngestionService(session)
        return await service.ingest_periodic_active_businesses()


async def ingest_platform_for_business(business_id: str, platform: str) -> dict[str, Any]:
    """Execute ingestion cycle for a specific business and platform."""
    try:
        async with AsyncSessionLocal() as session:
            from app.services.ingestion_service import IngestionService
            service = IngestionService(session)
            result = await service.ingest_for_business_and_platform(business_id, platform)
            return result.model_dump()
    except Exception as exc:
        logger.error(f"Task ingest_platform_for_business failed for {business_id} on {platform}: {exc}")
        return {"status": "error", "error_message": str(exc)}


async def pipeline_process_mentions(business_id: str, mention_ids: list[str]) -> dict[str, Any]:
    """Integration hook: handoff newly ingested mentions to intelligence analysis."""
    async with AsyncSessionLocal() as session:
        from app.models.business import Business
        from app.services.crisis_service import CrisisService
        from app.services.fraud_service import FraudService
        from app.services.reputation_service import ReputationService
        from app.services.sentiment_service import SentimentService

        biz = await session.get(Business, business_id)
        user_id = biz.owner_id if biz else business_id

        sentiment_service = SentimentService(session)
        fraud_service = FraudService(session)
        reputation_service = ReputationService(session)
        crisis_service = CrisisService(session)

        processed_count = 0
        for m_id in mention_ids:
            try:
                await sentiment_service.analyze_mention(user_id, m_id)
                await fraud_service.get_fraud_analysis(user_id, m_id)
                processed_count += 1
            except Exception as e:
                logger.warning(f"Error processing mention {m_id} in intelligence pipeline: {e}")

        try:
            await reputation_service.recalculate(user_id)
            await crisis_service.analyze_and_detect(user_id)
        except Exception as e:
            logger.warning(f"Error updating reputation/crisis for business {business_id}: {e}")

        return {
            "business_id": business_id,
            "mentions_processed": processed_count,
            "total_mentions": len(mention_ids),
            "status": "intelligence_complete",
        }


async def fetch_mentions(business_id: str) -> dict[str, Any]:
    """Fetch external mentions from platform connectors in background via IngestionService."""
    async with AsyncSessionLocal() as session:
        from app.services.ingestion_service import IngestionService
        service = IngestionService(session)
        results = await service.ingest_for_business_all_active(business_id)
        return {
            "business_id": business_id,
            "status": "mentions_fetched",
            "results": [r.model_dump() for r in results],
        }


async def process_sentiment(mention_id: str, user_id: str) -> dict[str, Any]:
    """Process sentiment and aspect breakdown in background."""
    async with AsyncSessionLocal() as session:
        from app.services.sentiment_service import SentimentService
        service = SentimentService(session)
        result = await service.analyze_mention(user_id, mention_id)
        return {"mention_id": mention_id, "sentiment": result.sentiment, "confidence": result.confidence}


async def analyze_fraud(mention_id: str, user_id: str) -> dict[str, Any]:
    """Analyze review for fraudulent indicators in background."""
    async with AsyncSessionLocal() as session:
        from app.services.fraud_service import FraudService
        service = FraudService(session)
        result = await service.get_fraud_analysis(user_id, mention_id)
        return {"mention_id": mention_id, "is_fraudulent": result.is_fraudulent, "risk_level": result.risk_level}


async def calculate_reputation(user_id: str) -> dict[str, Any]:
    """Recalculate reputation score in background."""
    async with AsyncSessionLocal() as session:
        from app.services.reputation_service import ReputationService
        service = ReputationService(session)
        score = await service.recalculate(user_id)
        return {"user_id": user_id, "current_score": score.current_score}


async def detect_crisis(user_id: str) -> dict[str, Any]:
    """Evaluate crisis anomalies in background."""
    async with AsyncSessionLocal() as session:
        from app.services.crisis_service import CrisisService
        service = CrisisService(session)
        event = await service.analyze_and_detect(user_id)
        return {"user_id": user_id, "crisis_detected": event is not None}


async def generate_alerts(
    business_id: str,
    alert_type: str,
    title: str,
    message: str,
    severity: str = "medium",
    reference_id: str | None = None,
    reference_type: str | None = None,
) -> dict[str, Any]:
    """Generate and dispatch notification alert in background."""
    async with AsyncSessionLocal() as session:
        from app.services.alert_service import AlertService
        service = AlertService(session)
        alert = await service.create_alert(
            business_id=business_id,
            type=alert_type,
            title=title,
            message=message,
            severity=severity,
            reference_id=reference_id,
            reference_type=reference_type,
        )
        return {"alert_id": alert.id, "status": "dispatched"}


async def scan_business_full(business_id: str) -> dict[str, Any]:
    """Execute complete end-to-end asynchronous scan using FastAPI BackgroundTasks."""
    try:
        async with AsyncSessionLocal() as session:
            from app.models.business import Business
            from app.models.platform import PlatformConnection
            from app.repositories.platform_repository import PlatformConnectionRepository
            from app.services.authenticity_service import ReviewAuthenticityService
            from app.services.crisis_service import CrisisService
            from app.services.ingestion_service import IngestionService
            from app.services.issue_detection_service import IssueDetectionService
            from app.services.reputation_service import ReputationService
            from app.services.sentiment_service import SentimentService

            biz = await session.get(Business, business_id)
            if not biz:
                logger.error(f"Scan aborted: Business '{business_id}' not found.")
                return {"status": "error", "error_message": "Business not found"}
                
            user_id = biz.owner_id if biz.owner_id else business_id

            # 1. Multi-platform Ingestion with Failure Isolation
            ingestion_service = IngestionService(session)
            platform_repo = PlatformConnectionRepository(session)

            standard_platforms = ["google", "reddit", "twitter"]
            for plat in standard_platforms:
                await platform_repo.get_or_create(business_id, plat)

            ingestion_results = []
            active_conns = await platform_repo.list_active_for_business(business_id)
            for conn in active_conns:
                try:
                    res = await ingestion_service.ingest_for_business_and_platform(business_id, conn.platform)
                    ingestion_results.append(res.model_dump())
                except Exception as exc:
                    logger.error(f"Scan ingestion failed for {business_id} on {conn.platform}: {exc}")
                    ingestion_results.append({
                        "platform": conn.platform,
                        "status": "error",
                        "error_message": str(exc),
                        "records_inserted": 0,
                    })

            # 2. Intelligence Pipeline: Sentiment
            sentiment_service = SentimentService(session)
            from app.models.mention import Mention
            from sqlalchemy import select

            stmt_mentions = select(Mention).where(Mention.business_id == business_id)
            all_mentions = list((await session.execute(stmt_mentions)).scalars().all())
            for m in all_mentions:
                if not m.sentiment:
                    try:
                        await sentiment_service.analyze_mention(user_id, m.id)
                    except Exception as e:
                        logger.warning(f"Sentiment failed for {m.id}: {e}")

            # 3. Issue Discovery & Clustering
            issue_service = IssueDetectionService(session)
            issues = await issue_service.detect_and_persist_issues(business_id)

            # 4. Review Authenticity & Clusters
            auth_service = ReviewAuthenticityService(session)
            findings = await auth_service.analyze_business_authenticity(business_id)

            # 5. Crisis Early Warning & Driver Attribution
            crisis_service = CrisisService(session)
            crisis_res = await crisis_service.evaluate_crisis_for_business(business_id)

            # 6. Reputation Score Recomputation
            rep_service = ReputationService(session)
            rep_score = await rep_service.recalculate(user_id)

            logger.info(f"Scan completed for business {business_id}")
            return {
                "business_id": business_id,
                "status": "completed",
                "ingestion_results": ingestion_results,
                "issues_count": len(issues),
                "findings_count": len(findings),
                "crisis_warning_level": crisis_res["warning_level"],
                "reputation_score": rep_score.current_score,
            }
    except Exception as e:
        logger.error(f"Error in scan_business_full for {business_id}: {e}\n{traceback.format_exc()}")
        return {"status": "error", "error_message": str(e)}
