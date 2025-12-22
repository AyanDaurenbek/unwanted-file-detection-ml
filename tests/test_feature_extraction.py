import os

from src.feature_extraction.generic import GenericFeatureExtractor
from src.feature_extraction.manager import FeatureExtractionManager
from src.feature_extraction.pe import PEFeatureExtractor


def test_generic_extractor_strings(tmp_path):
    extractor = GenericFeatureExtractor()
    data = b"hello world\nthis is a test"
    features = extractor.extract(data, "text/plain")
    assert features["file_size"] == len(data)
    assert features["num_printable_strings"] >= 1


def test_pe_extractor_fallback():
    extractor = PEFeatureExtractor()
    features = extractor.extract(b"not-a-pe", "application/x-dosexec")
    assert "num_sections" in features


def test_manager_combines():
    manager = FeatureExtractionManager()
    data = b"random data"
    features = manager.extract(data, "application/octet-stream")
    assert "entropy" in features
