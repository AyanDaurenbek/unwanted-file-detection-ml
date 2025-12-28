import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib


class ModelRegistry:
    def __init__(self, registry_path: str) -> None:
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)

    def save(self, version: str, model: Any, preprocess: Any, metrics: Dict[str, Any]) -> str:
        version_dir = self.registry_path / version
        version_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, version_dir / "model.pkl")
        joblib.dump(preprocess, version_dir / "preprocess.pkl")
        with open(version_dir / "metrics.json", "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        return str(version_dir)

    def load(self, version: str) -> Tuple[Any, Any]:
        version_dir = self.registry_path / version
        model = joblib.load(version_dir / "model.pkl")
        preprocess = joblib.load(version_dir / "preprocess.pkl")
        return model, preprocess

    def active_version(self) -> str:
        marker = self.registry_path / "active.txt"
        if marker.exists():
            return marker.read_text().strip()
        return ""

    def set_active(self, version: str) -> None:
        marker = self.registry_path / "active.txt"
        marker.write_text(version)
