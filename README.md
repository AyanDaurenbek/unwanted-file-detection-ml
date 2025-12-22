# Unwanted File Detection ML

End-to-end system for detecting unwanted files using machine learning. Includes FastAPI service, Celery worker, PostgreSQL storage, Redis queue, Prometheus metrics, and a synthetic training pipeline.

## Features
- REST API with sync and async scanning modes.
- Pluggable feature extraction (PE, OLE, generic) with graceful fallbacks.
- Celery-powered background scanning with Redis.
- PostgreSQL storage managed via Alembic migrations.
- Synthetic data generator and LightGBM/RandomForest training pipeline.
- Structured JSON logging and Prometheus metrics.

## Quickstart

1. Copy environment variables and start services:
   ```bash
   cp .env.example .env
   make up
   ```

2. Train a demo model (runs on synthetic data):
   ```bash
   make train
   ```

3. Run tests and linters:
   ```bash
   make test
   make lint
   ```

4. Sample curl requests:
   ```bash
   curl -X POST -F "file=@tests/fixtures/sample.bin" "http://localhost:8000/api/v1/scan?mode=sync"
   curl http://localhost:8000/api/v1/health
   curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/v1/admin/scans
   ```

## Project Structure

- `src/api/` — FastAPI application and routes.
- `src/tasks/` — Celery configuration and scan task.
- `src/feature_extraction/` — Feature extractors for different file types.
- `src/models/` — Training, inference, registry, and synthetic data generation.
- `src/storage/` — SQLAlchemy models and database session utilities.
- `configs/` — YAML configuration files for app and training.
- `docs/` — Architecture, API, operations, and experiments documentation.
- `tests/` — Pytest suites covering feature extraction, training, and API.

## Migrations

Run Alembic migrations once the database is available:

```bash
alembic upgrade head
```

## Security Notes

- Admin endpoints require an API key (`X-API-Key`).
- Maximum file size defaults to 20 MB.
- Raw file contents are not persisted by default; only metadata and hashes are stored.
