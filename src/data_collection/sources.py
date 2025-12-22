from dataclasses import dataclass
from typing import List


@dataclass
class DatasetSource:
    name: str
    url: str
    license_note: str


def default_sources() -> List[DatasetSource]:
    return [
        DatasetSource("EMBER", "https://github.com/elastic/ember", "CC BY-SA 4.0"),
        DatasetSource("MalwareBazaar", "https://bazaar.abuse.ch/", "Requires terms acceptance; metadata only by default"),
        DatasetSource("BODMAS", "https://www.kaggle.com/datasets/mahyarelsayad/bodmas", "Kaggle terms acceptance required"),
    ]
