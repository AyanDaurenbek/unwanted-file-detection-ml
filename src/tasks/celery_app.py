import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("tasks", broker=REDIS_URL)
celery_app.conf.task_routes = {"src.tasks.scan.scan_file_task": {"queue": "scan_queue"}}
celery_app.conf.result_backend = REDIS_URL
