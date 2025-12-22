import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


def get_app(monkeypatch):
    os.environ["DATABASE_URL"] = "sqlite:///./test_api.db"
    from importlib import reload
    import src.api.main as main

    reload(main)
    return main.app


def test_health(monkeypatch):
    client = TestClient(get_app(monkeypatch))
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_scan_sync(monkeypatch, tmp_path):
    client = TestClient(get_app(monkeypatch))
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"hello world")
    files = {"file": ("sample.bin", sample.read_bytes(), "application/octet-stream")}
    resp = client.post("/api/v1/scan", files=files, data={"mode": "sync", "explain": True})
    assert resp.status_code == 200
    body = resp.json()
    assert "predicted_class" in body


def test_metrics(monkeypatch):
    client = TestClient(get_app(monkeypatch))
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert "scans_total" in resp.text
