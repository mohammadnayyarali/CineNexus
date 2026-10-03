"""Offline artifact construction and loading."""

import logging
from pathlib import Path

import joblib

LOGGER = logging.getLogger(__name__)


def build_artifact(dataset_path: str | Path, artifact_path: str | Path, content_fields: list[str] | None = None) -> Path:
    """Build and serialize the fitted catalog engine for online reuse."""
    from netflix_recommender.data.loader import load_dataset
    from netflix_recommender.data.preprocessor import preprocess_dataset
    from netflix_recommender.data.validator import validate_dataset
    from netflix_recommender.features.feature_engineering import build_content_text
    from netflix_recommender.features.vectorizer import ContentVectorizer

    raw = load_dataset(dataset_path)
    validate_dataset(raw)
    metadata = preprocess_dataset(raw)
    content = build_content_text(metadata, content_fields)
    vectorizer = ContentVectorizer()
    matrix = vectorizer.fit_transform(content.tolist())
    output = Path(artifact_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"metadata": metadata, "matrix": matrix}, output)
    LOGGER.info("Wrote recommendation artifact to %s", output)
    return output


def load_engine(artifact_path: str | Path) -> object:
    """Load a prebuilt engine; no CSV parsing or vectorizer fitting occurs here."""
    from netflix_recommender.recommender.engine import RecommendationEngine

    bundle = joblib.load(artifact_path)
    return RecommendationEngine(bundle["metadata"], bundle["matrix"])
