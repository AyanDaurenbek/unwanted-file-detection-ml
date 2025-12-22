import time
import uuid
from typing import Any, Dict

from sqlalchemy.orm import Session

from src.feature_extraction.manager import FeatureExtractionManager
from src.models.infer import InferenceEngine
from src.storage import models
from src.storage.database import SessionLocal
from src.tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def scan_file_task(self: Any, file_content: bytes, mime_type: str, model_registry: str, model_version: str) -> Dict[str, Any]:
    db: Session = SessionLocal()
    start = time.time()
    try:
        engine = InferenceEngine(model_registry, model_version)
        extractor = FeatureExtractionManager()
        features = extractor.extract(file_content, mime_type)
        result = engine.predict(file_content, mime_type)

        file_record = models.File(
            id=uuid.uuid4(),
            sha256="",  # computed upstream
            size_bytes=len(file_content),
            mime_type=mime_type,
        )
        db.add(file_record)
        db.flush()

        scan_record = models.Scan(
            id=uuid.uuid4(),
            file_id=file_record.id,
            status="done",
            predicted_class=result["predicted_class"],
            probabilities=result["probabilities"],
            explain=result["explain"],
            model_version=model_version,
            duration_ms=int((time.time() - start) * 1000),
        )
        db.add(scan_record)
        db.commit()
        return {"scan_id": str(scan_record.id), **result}
    except Exception as exc:  # pragma: no cover - Celery retry path
        db.rollback()
        raise self.retry(exc=exc)
    finally:
        db.close()
