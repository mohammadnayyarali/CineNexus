"""CSV dataset loading."""

import logging
from pathlib import Path

import pandas as pd

from netflix_recommender.utils.exceptions import DatasetValidationError

LOGGER = logging.getLogger(__name__)


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV dataset and provide actionable errors for common failures."""
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file does not exist: {dataset_path}")
    if dataset_path.suffix.lower() != ".csv":
        raise DatasetValidationError("Dataset must be a CSV file.")
    try:
        frame = pd.read_csv(dataset_path)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as exc:
        raise DatasetValidationError(f"Could not read dataset '{dataset_path}': {exc}") from exc
    LOGGER.info("Loaded dataset with %d rows and %d columns", *frame.shape)
    return frame
