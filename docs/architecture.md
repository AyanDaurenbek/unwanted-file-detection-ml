# Architecture

The system is composed of distinct modules:

- **API Gateway (FastAPI)** exposes synchronous and asynchronous endpoints for file scanning, health checks, and metrics.
- **Task Queue (Celery + Redis)** processes heavy scanning jobs asynchronously on the `scan_queue` queue.
- **Feature Extraction Engine** provides pluggable extractors for PE, OLE, and generic file attributes through a unified manager.
- **ML Pipeline** delivers training and inference with a registry of model versions stored on disk.
- **Storage (PostgreSQL/SQLAlchemy)** persists files, scans, datasets, and model versions with Alembic migrations.
- **Observability** integrates Prometheus metrics and structured JSON logging via structlog.

Data flows from file upload to feature extraction, model inference, persistence of results, and exposure of metrics for monitoring.
