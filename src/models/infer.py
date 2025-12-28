import json
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd

from src.feature_extraction.manager import FeatureExtractionManager
from src.models.model_registry import ModelRegistry
from src.models.synthetic_data_generator import CLASSES


class InferenceEngine:
    def __init__(self, registry_path: str, active_version: str):
        self.registry = ModelRegistry(registry_path)
        self.version = active_version or self.registry.active_version()
        self.model, self.preprocess = self.registry.load(self.version)
        self.extractor = FeatureExtractionManager()

    def predict(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        features = self.extractor.extract(content, mime_type)
        df = pd.DataFrame([features])
        probs = self.model.predict_proba(df)[0]
        top_idx = int(np.argmax(probs))
        return {
            "predicted_class": CLASSES[top_idx] if top_idx < len(CLASSES) else str(top_idx),
            "probabilities": {cls: float(prob) for cls, prob in zip(CLASSES, probs)},
            "explain": sorted(features.items(), key=lambda x: abs(x[1]), reverse=True)[:5],
            "model_version": self.version,
        }


def load_for_cli(model_dir: str) -> Any:
    model = joblib.load(Path(model_dir) / "model.pkl")
    return model


def local_infer(model_dir: str, file_path: str, mime_type: str = "application/octet-stream") -> Dict[str, Any]:
    model = load_for_cli(model_dir)
    extractor = FeatureExtractionManager()
    with open(file_path, "rb") as f:
        content = f.read()
    features = extractor.extract(content, mime_type)
    df = pd.DataFrame([features])
    probs = model.predict_proba(df)[0]
    return {
        "probabilities": probs.tolist(),
        "predicted_class": CLASSES[int(np.argmax(probs))],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--mime_type", default="application/octet-stream")
    args = parser.parse_args()
    result = local_infer(args.model_dir, args.file, args.mime_type)
    print(json.dumps(result, indent=2))
