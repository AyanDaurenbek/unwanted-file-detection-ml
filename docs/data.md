# Data

Datasets are organized under the `data/` directory. Use `src/data_collection/downloader.py` to prepare directories in dry-run mode, leaving instructions for manual downloads that respect licenses.

Synthetic data generation is supported through `src/models/synthetic_data_generator.py`, producing reproducible tabular features across five classes: benign, malware, potentially_unwanted, policy_violation, and confidential_suspected.

To add new datasets, create a new `DatasetSource` entry in `src/data_collection/sources.py` and extend the downloader to fetch or stage the dataset with proper license validation.
