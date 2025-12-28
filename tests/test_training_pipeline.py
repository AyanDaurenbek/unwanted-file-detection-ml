import json
import os
from pathlib import Path

from src.models.train import train


def test_train_creates_artifacts(tmp_path, monkeypatch):
    cfg_path = tmp_path / "train.yaml"
    cfg_path.write_text(
        """
seed: 1
model_registry: {registry}
train_samples: 50
val_samples: 10
test_samples: 10
features:
  categorical: ["mime_type"]
  numeric: ["file_size", "entropy", "num_printable_strings", "avg_string_len", "num_sections"]
model:
  baseline:
    type: "random_forest"
    params:
      n_estimators: 10
  advanced:
    type: "lightgbm"
    params:
      n_estimators: 10
output:
  model_version: "test-version"
  metrics_path: "{metrics}"
  model_card_path: "{card}"
""".format(
            registry=tmp_path / "models",
            metrics=tmp_path / "metrics.json",
            card=tmp_path / "model_card.md",
        )
    )
    result = train(str(cfg_path))
    assert Path(result["model_path"]).exists()
    assert Path(tmp_path / "metrics.json").exists()
    metrics = json.loads(Path(tmp_path / "metrics.json").read_text())
    assert "f1_macro" in metrics
