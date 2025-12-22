from typing import Any, Dict

from src.feature_extraction.base import FeatureExtractor

try:
    from oletools.olevba3 import VBA_Parser
except Exception:  # pragma: no cover
    VBA_Parser = None


class OLEFeatureExtractor(FeatureExtractor):
    def supports(self, mime_type: str) -> bool:
        return mime_type in {
            "application/vnd.ms-word",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
        }

    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        if VBA_Parser is None:
            return {"has_macros": False, "suspicious_macros": 0}
        has_macros = False
        suspicious = 0
        try:
            parser = VBA_Parser("scanned.doc", data=content)
            if parser.detect_vba_macros():
                has_macros = True
                analysis = parser.analyze_macros()
                suspicious = len([item for item in analysis if item.type != "None"])
        except Exception:
            has_macros = False
            suspicious = 0
        return {"has_macros": has_macros, "suspicious_macros": suspicious}
