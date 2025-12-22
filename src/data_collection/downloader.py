import logging
from pathlib import Path

from src.data_collection.sources import DatasetSource, default_sources

logger = logging.getLogger(__name__)


def prepare_directories(base_path: str = "data") -> None:
    path = Path(base_path)
    path.mkdir(exist_ok=True)
    for source in default_sources():
        source_dir = path / source.name.lower()
        source_dir.mkdir(exist_ok=True)
        (source_dir / "README.txt").write_text(
            f"Dataset: {source.name}\nURL: {source.url}\nLicense: {source.license_note}\nDownload manually with proper acceptance.\n"
        )
        logger.info("Prepared directory for %s", source.name)


def dry_run() -> None:
    logger.info("Performing dry-run dataset preparation")
    prepare_directories()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dry_run()
