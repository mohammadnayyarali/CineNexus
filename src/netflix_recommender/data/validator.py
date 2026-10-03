"""Dataset quality checks."""

import logging
from dataclasses import dataclass

import pandas as pd

from netflix_recommender.utils.exceptions import DatasetValidationError

LOGGER = logging.getLogger(__name__)
REQUIRED_COLUMNS = {"title"}


@dataclass(frozen=True)
class ValidationReport:
    """Non-fatal quality information discovered during validation."""

    row_count: int
    duplicate_title_count: int
    missing_values: dict[str, int]


def validate_dataset(frame: pd.DataFrame) -> ValidationReport:
    """Validate the minimum catalog contract without requiring optional metadata."""
    missing_columns = REQUIRED_COLUMNS - set(frame.columns)
    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise DatasetValidationError(f"Required column(s) missing: {names}")
    if frame.empty:
        raise DatasetValidationError("Dataset is empty and cannot build recommendations.")
    title_values = frame["title"].fillna("").astype(str).str.strip()
    if (title_values == "").all():
        raise DatasetValidationError("Dataset contains no usable titles.")
    report = ValidationReport(
        row_count=len(frame),
        duplicate_title_count=int(title_values.duplicated(keep="first").sum()),
        missing_values={key: int(value) for key, value in frame.isna().sum().items()},
    )
    LOGGER.info("Validated %d rows; found %d duplicate titles", report.row_count, report.duplicate_title_count)
    return report
