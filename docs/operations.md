# Operations

## Running with Docker Compose

```bash
cp .env.example .env
make up
```

Services started: FastAPI at `:8000`, Celery worker, PostgreSQL, and Redis.

## Local Development

```bash
python -m src.data_collection.downloader  # prepare dataset directories
python -m src.models.train --config configs/train.yaml
uvicorn src.api.main:app --reload
```

## Metrics and Logs

- Prometheus metrics exposed at `/metrics`.
- Structured JSON logs via structlog; adjust log level through environment variables if needed.
