from typing import Any, Dict

from src.feature_extraction.base import FeatureExtractor

try:
    import pefile
except Exception:  # pragma: no cover
    pefile = None

try:
    import lief
except Exception:  # pragma: no cover
    lief = None


class PEFeatureExtractor(FeatureExtractor):
    def supports(self, mime_type: str) -> bool:
        return mime_type in {"application/x-dosexec", "application/x-msdownload"}

    def extract(self, content: bytes, mime_type: str) -> Dict[str, Any]:
        if pefile is None:
            return {"num_sections": 0, "entry_point": 0, "imphash": None}
        pe = pefile.PE(data=content)
        num_sections = len(pe.sections)
        entry_point = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        imphash = pe.get_imphash()
        section_sizes = [section.SizeOfRawData for section in pe.sections]
        features: Dict[str, Any] = {
            "num_sections": num_sections,
            "entry_point": entry_point,
            "imphash": imphash,
            "section_sizes_mean": sum(section_sizes) / len(section_sizes) if section_sizes else 0,
        }
        if lief is not None:
            try:
                binary = lief.parse(list(content))
                features["has_signature"] = bool(binary.signatures)
            except Exception:
                features["has_signature"] = False
        return features
