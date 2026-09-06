"""Tests for Phase 7: Celery and Redis background processing pipeline."""

from app.workers.celery_app import celery_app


def test_celery_task_registration():
    """Verify that all domain background tasks are properly registered with Celery."""
    registered_tasks = celery_app.tasks.keys()
    assert "tasks.fetch_mentions" in registered_tasks
    assert "tasks.schedule_periodic_ingestion" in registered_tasks
    assert "tasks.ingest_platform_for_business" in registered_tasks
    assert "tasks.pipeline_process_mentions" in registered_tasks
    assert "tasks.process_sentiment" in registered_tasks
    assert "tasks.analyze_fraud" in registered_tasks
    assert "tasks.calculate_reputation" in registered_tasks
    assert "tasks.detect_crisis" in registered_tasks
    assert "tasks.generate_alerts" in registered_tasks


def test_celery_app_configuration():
    """Verify Celery app serialization, timezone, concurrency, and beat scheduler."""
    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.result_serializer == "json"
    assert celery_app.conf.timezone == "UTC"
    assert celery_app.conf.task_time_limit == 300
    assert "periodic-data-ingestion" in celery_app.conf.beat_schedule
    assert celery_app.conf.beat_schedule["periodic-data-ingestion"]["task"] == "tasks.schedule_periodic_ingestion"
