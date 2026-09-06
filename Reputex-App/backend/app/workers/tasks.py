"""Background Celery worker tasks for RepuTex asynchronous pipeline."""

import asyncio
from typing import Any

from app.core.database import AsyncSessionLocal
from app.core.logging import logger
from app.workers.celery_app import celery_app


def run_async(coro):
    """Bridge async coroutine execution inside Celery task thread."""
    return asyncio.run(coro)


@celery_app.task(name="tasks.schedule_periodic_ingestion")
def schedule_periodic_ingestion() -> dict[str, Any]:
    """Periodic Celery Beat trigger to discover active businesses and dispatch platform workers."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.ingestion_service import IngestionService

            service = IngestionService(session)
            return await service.ingest_periodic_active_businesses()

    return run_async(_impl())


@celery_app.task(name="tasks.ingest_platform_for_business", bind=True, max_retries=3, default_retry_delay=60)
def ingest_platform_for_business(self, business_id: str, platform: str) -> dict[str, Any]:
    """Execute ingestion cycle for a specific business and platform with exponential backoff retry."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.ingestion_service import IngestionService

            service = IngestionService(session)
            result = await service.ingest_for_business_and_platform(business_id, platform)
            return result.model_dump()

    try:
        return run_async(_impl())
    except Exception as exc:
        logger.error(f"Task ingest_platform_for_business failed for {business_id} on {platform}: {exc}")
        # Only retry transient failures, do not retry permanent errors
        raise self.retry(exc=exc)


@celery_app.task(name="tasks.pipeline_process_mentions")
def pipeline_process_mentions(business_id: str, mention_ids: list[str]) -> dict[str, Any]:
    """Integration hook: handoff newly ingested mentions to intelligence analysis."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.models.business import Business
            from app.services.crisis_service import CrisisService
            from app.services.fraud_service import FraudService
            from app.services.reputation_service import ReputationService
            from app.services.sentiment_service import SentimentService

            # Resolve business owner for user-scoped services
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

            # Recalculate score and check for crisis
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

    return run_async(_impl())


@celery_app.task(name="tasks.fetch_mentions")
def fetch_mentions(business_id: str) -> dict[str, Any]:
    """Fetch external mentions from platform connectors in background via IngestionService."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.ingestion_service import IngestionService

            service = IngestionService(session)
            results = await service.ingest_for_business_all_active(business_id)
            return {
                "business_id": business_id,
                "status": "mentions_fetched",
                "results": [r.model_dump() for r in results],
            }

    return run_async(_impl())


@celery_app.task(name="tasks.process_sentiment")
def process_sentiment(mention_id: str, user_id: str) -> dict[str, Any]:
    """Process sentiment and aspect breakdown in background."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.sentiment_service import SentimentService

            service = SentimentService(session)
            result = await service.analyze_mention(user_id, mention_id)
            return {"mention_id": mention_id, "sentiment": result.sentiment, "confidence": result.confidence}

    return run_async(_impl())


@celery_app.task(name="tasks.analyze_fraud")
def analyze_fraud(mention_id: str, user_id: str) -> dict[str, Any]:
    """Analyze review for fraudulent indicators in background."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.fraud_service import FraudService

            service = FraudService(session)
            result = await service.get_fraud_analysis(user_id, mention_id)
            return {"mention_id": mention_id, "is_fraudulent": result.is_fraudulent, "risk_level": result.risk_level}

    return run_async(_impl())


@celery_app.task(name="tasks.calculate_reputation")
def calculate_reputation(user_id: str) -> dict[str, Any]:
    """Recalculate reputation score in background."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.reputation_service import ReputationService

            service = ReputationService(session)
            score = await service.recalculate(user_id)
            return {"user_id": user_id, "current_score": score.current_score}

    return run_async(_impl())


@celery_app.task(name="tasks.detect_crisis")
def detect_crisis(user_id: str) -> dict[str, Any]:
    """Evaluate crisis anomalies in background."""

    async def _impl():
        async with AsyncSessionLocal() as session:
            from app.services.crisis_service import CrisisService

            service = CrisisService(session)
            event = await service.analyze_and_detect(user_id)
            return {"user_id": user_id, "crisis_detected": event is not None}

    return run_async(_impl())


@celery_app.task(name="tasks.generate_alerts")
def generate_alerts(
    business_id: str,
    alert_type: str,
    title: str,
    message: str,
    severity: str = "medium",
    reference_id: str | None = None,
    reference_type: str | None = None,
) -> dict[str, Any]:
    """Generate and dispatch notification alert in background."""

    async def _impl():
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

    return run_async(_impl())
