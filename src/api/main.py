import time
import uuid
from typing import Any, Dict

import prometheus_client
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.feature_extraction.manager import FeatureExtractionManager
from src.models.infer import InferenceEngine
from src.storage import models
from src.storage.database import Base, engine, get_db
from src.tasks.celery_app import celery_app
from src.tasks.scan import scan_file_task
from src.utils.logging import configure_logging
from src.utils.security import API_KEY_HEADER, compute_sha256, verify_api_key

configure_logging()
settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Unwanted File Detection ML")
scan_counter = prometheus_client.Counter("scans_total", "Total number of scans")


@app.post("/api/v1/scan")
async def scan_file(
    mode: str = "async",
    explain: bool = True,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()
    if len(content) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
    sha256 = compute_sha256(content)
    mime_type = file.content_type or "application/octet-stream"

    existing = db.query(models.File).filter(models.File.sha256 == sha256).first()
    if existing:
        scan = (
            db.query(models.Scan)
            .filter(models.Scan.file_id == existing.id, models.Scan.status == "done")
            .first()
        )
        if scan:
            return {"scan_id": str(scan.id), "cached": True, "result": scan.probabilities}

    if mode == "sync":
        start = time.time()
        engine = InferenceEngine(settings.model_registry, settings.active_model_version)
        extractor = FeatureExtractionManager()
        features = extractor.extract(content, mime_type)
        result = engine.predict(content, mime_type)
        file_record = models.File(
            id=uuid.uuid4(),
            sha256=sha256,
            size_bytes=len(content),
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
            explain=result["explain"] if explain else {},
            model_version=settings.active_model_version,
            duration_ms=int((time.time() - start) * 1000),
        )
        db.add(scan_record)
        db.commit()
        scan_counter.inc()
        return {"scan_id": str(scan_record.id), **result}

    task = scan_file_task.delay(content, mime_type, settings.model_registry, settings.active_model_version)
    return {"job_id": task.id}


@app.get("/api/v1/jobs/{job_id}")
def job_status(job_id: str):
    async_result = celery_app.AsyncResult(job_id)
    if async_result.successful():
        return {"status": "done", "result": async_result.get()}
    return {"status": async_result.status}


@app.get("/api/v1/scan/{scan_id}")
def get_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {
        "scan_id": str(scan.id),
        "status": scan.status,
        "predicted_class": scan.predicted_class,
        "probabilities": scan.probabilities,
        "explain": scan.explain,
    }


@app.post("/api/v1/scan/hash")
def scan_by_hash(payload: Dict[str, str], db: Session = Depends(get_db)):
    sha256 = payload.get("sha256")
    if not sha256:
        raise HTTPException(status_code=400, detail="sha256 required")
    file = db.query(models.File).filter(models.File.sha256 == sha256).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    scan = db.query(models.Scan).filter(models.Scan.file_id == file.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return {
        "scan_id": str(scan.id),
        "predicted_class": scan.predicted_class,
        "probabilities": scan.probabilities,
    }


@app.get("/api/v1/admin/scans")
def admin_scans(limit: int = 50, api_key: str | None = Header(default=None, alias=API_KEY_HEADER), db: Session = Depends(get_db)):
    verify_api_key(settings.api_key, api_key)
    scans = db.query(models.Scan).order_by(models.Scan.created_at.desc()).limit(limit).all()
    return [
        {
            "scan_id": str(scan.id),
            "predicted_class": scan.predicted_class,
            "created_at": scan.created_at,
        }
        for scan in scans
    ]


@app.get("/api/v1/admin/models")
def admin_models(api_key: str | None = Header(default=None, alias=API_KEY_HEADER), db: Session = Depends(get_db)):
    verify_api_key(settings.api_key, api_key)
    models_db = db.query(models.ModelVersion).all()
    return [
        {
            "version": m.version,
            "algo": m.algo,
            "is_active": m.is_active,
        }
        for m in models_db
    ]


@app.post("/api/v1/admin/models/activate/{model_version}")
def activate_model(model_version: str, api_key: str | None = Header(default=None, alias=API_KEY_HEADER), db: Session = Depends(get_db)):
    verify_api_key(settings.api_key, api_key)
    model = db.query(models.ModelVersion).filter(models.ModelVersion.version == model_version).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    for m in db.query(models.ModelVersion).all():
        m.is_active = False
    model.is_active = True
    db.commit()
    return {"status": "ok", "active": model_version}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return prometheus_client.generate_latest()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/admin", response_class=PlainTextResponse)
def admin_page():
    return "Unwanted File Detection Admin: use API key protected endpoints for details."
