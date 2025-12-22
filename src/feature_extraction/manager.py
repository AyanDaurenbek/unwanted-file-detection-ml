from typing import Any, Dict, List

from src.feature_extraction.base import FeatureExtractor
from src.feature_extraction.generic import GenericFeatureExtractor
from src.feature_extraction.ole import OLEFeatureExtractor
from src.feature_extraction.pe import PEFeatureExtractor


class FeatureExtractionManager:
    def __init__(self) -> None:
        self.extractors: List[FeatureExtractor] = [
            PEFeatureExtractor(),
            OLEFeatureExtractor(),
            GenericFeatureExtractor(),
        ]

    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        combined: Dict[str, Any] = {}
        for extractor in self.extractors:
            if extractor.supports(mime_type) or isinstance(extractor, GenericFeatureExtractor):
                combined.update(extractor.extract(content, mime_type))
        return combined
