"""Celery configuration and worker initialization."""

import os
from datetime import timedelta

from celery import Celery

from app.core.config import settings

broker_url = os.getenv("REDIS_URL", getattr(settings, "REDIS_URL", "redis://localhost:6379/0"))

celery_app = Celery(
    "reputex_workers",
    broker=broker_url,
    backend=broker_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "periodic-data-ingestion": {
            "task": "tasks.schedule_periodic_ingestion",
            "schedule": timedelta(minutes=settings.INGESTION_SCHEDULE_INTERVAL_MINUTES),
        },
    },
)

# Ensure tasks are loaded into task registry
import app.workers.tasks  # noqa: F401, E402
