import logging
from pathlib import Path
from typing import Iterable

from src.data_collection.sources import DatasetSource, default_sources

logger = logging.getLogger(__name__)


def write_readme(directory: Path, source: DatasetSource) -> None:
    directory.mkdir(exist_ok=True, parents=True)
    (directory / "README.txt").write_text(
        "\n".join(
            [
                f"Dataset: {source.name}",
                f"URL: {source.url}",
                f"License: {source.license_note}",
                "Download manually with proper acceptance.",
                "Do not store raw malicious binaries unless explicitly permitted.",
            ]
        )
    )
    logger.info("Prepared directory for %s", source.name)


def prepare_directories(base_path: str = "data", sources: Iterable[DatasetSource] | None = None) -> None:
    path = Path(base_path)
    path.mkdir(exist_ok=True, parents=True)
    for source in sources or default_sources():
        source_dir = path / source.name.lower()
        write_readme(source_dir, source)


def dry_run(base_path: str = "data") -> None:
    logger.info("Performing dry-run dataset preparation")
    prepare_directories(base_path=base_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dry_run()
