import pandas as pd
import pytest

from netflix_recommender.data.preprocessor import preprocess_dataset
from netflix_recommender.features.feature_engineering import build_content_text
from netflix_recommender.features.vectorizer import ContentVectorizer
from netflix_recommender.recommender.engine import RecommendationEngine
from netflix_recommender.utils.exceptions import TitleNotFoundError


def make_engine() -> RecommendationEngine:
    frame = pd.DataFrame(
        {
            "title": ["Alpha", "Beta", "Gamma"],
            "type": ["Movie", "Movie", "TV Show"],
            "listed_in": ["Drama", "Drama", "Comedy"],
            "description": ["space travel", "space mission", "cooking contest"],
        }
    )
    frame = preprocess_dataset(frame)
    vectorizer = ContentVectorizer(stop_words=None, ngram_range=(1, 1))
    matrix = vectorizer.fit_transform(build_content_text(frame).tolist())
    return RecommendationEngine(frame, matrix)


def test_recommendation_excludes_query_and_ranks_similar_content() -> None:
    results = make_engine().recommend("alpha", top_n=1)
    assert results[0]["title"] == "Beta"
    assert results[0]["similarity_score"] > 0


def test_unknown_title_is_domain_error() -> None:
    with pytest.raises(TitleNotFoundError):
        make_engine().recommend("missing")
