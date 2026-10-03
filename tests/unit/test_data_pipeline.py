import pandas as pd
import pytest

from netflix_recommender.data.loader import load_dataset
from netflix_recommender.data.preprocessor import normalize_text, preprocess_dataset
from netflix_recommender.data.validator import validate_dataset
from netflix_recommender.utils.exceptions import DatasetValidationError


def test_missing_title_column_is_rejected() -> None:
    with pytest.raises(DatasetValidationError, match="title"):
        validate_dataset(pd.DataFrame({"description": ["text"]}))


def test_empty_dataset_is_rejected() -> None:
    with pytest.raises(DatasetValidationError, match="empty"):
        validate_dataset(pd.DataFrame({"title": []}))


def test_preprocessing_normalizes_missing_values_and_deduplicates() -> None:
    frame = pd.DataFrame({"title": [" Alpha ", "Alpha", None], "description": [" a  b ", None, "ignored"]})
    cleaned = preprocess_dataset(frame)
    assert cleaned["title"].tolist() == ["Alpha"]
    assert normalize_text(None) == ""


def test_loader_rejects_missing_file(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "missing.csv")
