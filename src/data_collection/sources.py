from dataclasses import dataclass
from typing import List


@dataclass
class DatasetSource:
    name: str
    url: str
    license_note: str


def default_sources() -> List[DatasetSource]:
    return [
        DatasetSource("EMBER", "https://example.com/ember", "Check EMBER license"),
        DatasetSource("MalwareBazaar", "https://bazaar.abuse.ch/", "Requires terms acceptance"),
        DatasetSource("BODMAS", "https://example.com/bodmas", "Placeholder source"),
    ]
