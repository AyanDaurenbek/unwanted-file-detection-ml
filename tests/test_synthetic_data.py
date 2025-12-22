import numpy as np

from src.models.synthetic_data_generator import (
    CLASSES,
    create_hybrid_features,
    export_feature_schema,
    generate_synthetic_dataset,
)


def test_generate_synthetic_dataset_shape(tmp_path):
    X, y = generate_synthetic_dataset(20, seed=1)
    assert X.shape[0] == 20
    assert set(y).issubset(set(CLASSES))


def test_create_hybrid_features():
    primary = {"a": 1.0, "b": 2.0}
    secondary = {"a": 0.0, "b": 0.0}
    hybrid = create_hybrid_features(primary, secondary)
    assert hybrid["a"] == 0.7


def test_export_feature_schema(tmp_path):
    path = tmp_path / "schema.json"
    export_feature_schema(str(path), ["f1", "f2"])
    assert path.exists()
