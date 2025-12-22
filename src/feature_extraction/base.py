from abc import ABC, abstractmethod
from typing import Any, Dict


class FeatureExtractor(ABC):
    @abstractmethod
    def supports(self, mime_type: str) -> bool:
        ...

    @abstractmethod
    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        ...
