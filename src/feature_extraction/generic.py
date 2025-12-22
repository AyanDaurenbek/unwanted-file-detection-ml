import io
import math
from typing import Any, Dict

import magic

from src.feature_extraction.base import FeatureExtractor


def _shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = 0.0
    for f in freq:
        if f == 0:
            continue
        p = f / len(data)
        entropy -= p * math.log2(p)
    return entropy


def _string_stats(data: bytes) -> tuple[int, float]:
    try:
        text = data.decode(errors="ignore")
    except Exception:
        text = ""
    strings = [s for s in text.split("\n") if s.strip()]
    if not strings:
        return 0, 0.0
    lengths = [len(s) for s in strings]
    return len(strings), sum(lengths) / len(lengths)


class GenericFeatureExtractor(FeatureExtractor):
    def supports(self, mime_type: str) -> bool:
        return True

    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        detected = magic.from_buffer(content, mime=True)
        num_strings, avg_len = _string_stats(content)
        return {
            "file_size": len(content),
            "entropy": _shannon_entropy(content[:4096]),
            "num_printable_strings": num_strings,
            "avg_string_len": avg_len,
            "mime_type": mime_type or detected,
        }
