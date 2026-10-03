import pandas as pd
import pytest

from netflix_recommender.features.feature_engineering import build_content_text
from netflix_recommender.features.vectorizer import ContentVectorizer


def test_content_builder_ignores_missing_optional_columns() -> None:
    frame = pd.DataFrame({"title": ["Alpha"], "listed_in": ["Drama"]})
    assert build_content_text(frame, ["listed_in", "director"]).tolist() == ["Drama"]


def test_vectorizer_does_not_fit_on_empty_corpus() -> None:
    with pytest.raises(ValueError, match="empty"):
        ContentVectorizer().fit_transform(["", "  "])


def test_vectorizer_returns_square_similarity_input() -> None:
    matrix = ContentVectorizer(stop_words=None).fit_transform(["space drama", "space comedy"])
    assert matrix.shape == (2, matrix.shape[1])
