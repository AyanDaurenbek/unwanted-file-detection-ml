import argparse
import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from lightgbm import LGBMClassifier
except Exception:  # pragma: no cover
    LGBMClassifier = None

from src.models.model_registry import ModelRegistry
from src.models.synthetic_data_generator import CLASSES, export_feature_schema, generate_synthetic_dataset


def build_model(config: Dict[str, Any], categorical: list[str], numeric: list[str]) -> Tuple[Any, ColumnTransformer]:
    preprocess = ColumnTransformer(
        [
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("numeric", Pipeline([("scaler", StandardScaler())]), numeric),
        ]
    )
    model_cfg = config["model"]["baseline"]
    if model_cfg["type"] == "random_forest":
        classifier = RandomForestClassifier(**model_cfg.get("params", {}))
    else:
        classifier = RandomForestClassifier(n_estimators=50)

    if config["model"].get("advanced", {}).get("type") == "lightgbm" and LGBMClassifier is not None:
        advanced_params = config["model"]["advanced"].get("params", {})
        classifier = LGBMClassifier(**advanced_params)

    clf = Pipeline(steps=[("preprocess", preprocess), ("model", classifier)])
    return clf, preprocess


def evaluate(model: Any, X_test: pd.DataFrame, y_test: np.ndarray) -> Dict[str, Any]:
    y_pred = model.predict(X_test)
    metrics = {
        "f1_macro": f1_score(y_test, y_pred, average="macro"),
        "precision_macro": precision_score(y_test, y_pred, average="macro"),
        "recall_macro": recall_score(y_test, y_pred, average="macro"),
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
    }
    return metrics


def train(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    categorical = cfg["features"]["categorical"]
    numeric = cfg["features"]["numeric"]

    X, y = generate_synthetic_dataset(cfg.get("train_samples", 500), seed=cfg.get("seed", 42))
    columns = numeric + categorical
    df = pd.DataFrame(X, columns=numeric + ["num_sections", "dummy", "dummy2"][: len(categorical)])
    df[categorical[0]] = np.random.choice(["application/pdf", "application/octet-stream"], size=len(df))
    df = df[numeric + categorical]
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=cfg.get("seed", 42))

    model, preprocess = build_model(cfg, categorical, numeric)
    model.fit(X_train, y_train)

    metrics = evaluate(model, X_test, y_test)

    registry = ModelRegistry(cfg["model_registry"])
    version = cfg["output"]["model_version"]
    path = registry.save(version, model, preprocess, metrics)
    registry.set_active(version)

    feature_schema_path = Path(cfg["model_registry"]) / version / "feature_schema.json"
    export_feature_schema(str(feature_schema_path), numeric + categorical)

    with open(cfg["output"]["metrics_path"], "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(cfg["output"]["model_card_path"], "w", encoding="utf-8") as f:
        f.write(
            "# Model Card\n\n"
            f"Version: {version}\n\n"
            "Training data: synthetic\n\n"
            f"Classes: {', '.join(CLASSES)}\n\n"
            f"Metrics: {json.dumps(metrics, indent=2)}\n"
        )

    return {"model_path": path, "metrics": metrics}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    train(args.config)


if __name__ == "__main__":
    main()
