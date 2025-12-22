import json
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

CLASSES = [
    "benign",
    "malware",
    "potentially_unwanted",
    "policy_violation",
    "confidential_suspected",
]


@dataclass
class SyntheticSample:
    features: Dict[str, float]
    label: str


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def _base_feature_vector(label: str) -> Dict[str, float]:
    base_entropy = {
        "benign": 4.0,
        "malware": 7.5,
        "potentially_unwanted": 6.5,
        "policy_violation": 5.0,
        "confidential_suspected": 5.5,
    }
    base_strings = {
        "benign": (200, 12),
        "malware": (40, 6),
        "potentially_unwanted": (70, 8),
        "policy_violation": (120, 10),
        "confidential_suspected": (180, 20),
    }
    file_size = random.randint(50_000, 2_000_000)
    entropy = np.random.normal(base_entropy[label], 0.5)
    num_strings, avg_string_len = base_strings[label]
    num_sections = int(np.clip(np.random.normal(5, 1), 1, 10))
    return {
        "file_size": float(file_size),
        "entropy": float(max(entropy, 0.1)),
        "num_printable_strings": float(np.random.normal(num_strings, 10)),
        "avg_string_len": float(np.random.normal(avg_string_len, 2)),
        "num_sections": float(num_sections),
    }


def create_hybrid_features(primary: Dict[str, float], secondary: Dict[str, float], alpha: float = 0.7) -> Dict[str, float]:
    return {k: alpha * primary[k] + (1 - alpha) * secondary[k] for k in primary}


def generate_synthetic_dataset(n_samples: int, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    set_seed(seed)
    samples: List[Dict[str, float]] = []
    labels: List[str] = []
    for _ in range(n_samples):
        label = random.choice(CLASSES)
        primary = _base_feature_vector(label)
        secondary = _base_feature_vector(random.choice(CLASSES))
        features = create_hybrid_features(primary, secondary)
        samples.append(list(features.values()))
        labels.append(label)
    return np.array(samples), np.array(labels)


def export_feature_schema(path: str, feature_names: List[str]) -> None:
    schema = {"features": feature_names, "classes": CLASSES}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
