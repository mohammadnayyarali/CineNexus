"""In-memory recommendation engine."""

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:  # pragma: no cover - depends on the host's native DLL policy
    cosine_similarity = None

from netflix_recommender.utils.exceptions import TitleNotFoundError

LOGGER = logging.getLogger(__name__)


@dataclass
class RecommendationEngine:
    """Rank catalog rows by cosine similarity to a selected title."""

    metadata: pd.DataFrame
    matrix: object

    def __post_init__(self) -> None:
        self._title_lookup = {
            str(title).casefold(): index for index, title in enumerate(self.metadata["title"])
        }

    def titles(self) -> list[str]:
        return self.metadata["title"].astype(str).tolist()

    def recommend(self, title: str, top_n: int = 10) -> list[dict[str, object]]:
        """Return metadata-rich recommendations, excluding the selected row."""
        if not title or not title.strip():
            raise TitleNotFoundError("Title must not be empty.")
        if top_n < 1:
            raise ValueError("top_n must be at least 1.")
        index = self._title_lookup.get(title.strip().casefold())
        if index is None:
            raise TitleNotFoundError(f"Title not found: {title}")
        if cosine_similarity is not None:
            scores = cosine_similarity(self.matrix[index], self.matrix).ravel()
        else:
            scores = self.matrix[index].dot(self.matrix.T).toarray().ravel()
        candidate_indices = np.argsort(-scores, kind="stable")
        recommendations = []
        for candidate in candidate_indices:
            if int(candidate) == index:
                continue
            row = self.metadata.iloc[int(candidate)]
            item = {
                "title": str(row["title"]),
                "similarity_score": round(float(scores[candidate]), 6),
            }
            for field in ("type", "listed_in", "release_year", "rating", "description"):
                if field in row.index:
                    value = row[field]
                    item[field] = None if pd.isna(value) else value
            recommendations.append(item)
            if len(recommendations) == top_n:
                break
        LOGGER.info("Generated %d recommendations for title '%s'", len(recommendations), title)
        return recommendations
