"""Reusable TF-IDF vectorization."""

import math
import re
from pathlib import Path

import numpy as np
from scipy import sparse

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except ImportError:  # pragma: no cover - depends on the host's native DLL policy
    TfidfVectorizer = None


class _FallbackTfidfVectorizer:
    """Small pure-Python fallback for hosts that cannot load scikit-learn DLLs."""

    def __init__(self, stop_words: object = "english", ngram_range: tuple[int, int] = (1, 2), **_: object) -> None:
        self.stop_words = {"a", "an", "and", "are", "as", "at", "by", "for", "in", "is", "of", "on", "or", "the", "to"} if stop_words == "english" else set()
        self.ngram_range = ngram_range
        self.vocabulary_: dict[str, int] = {}
        self.idf_: np.ndarray = np.array([])

    def _tokens(self, text: str) -> list[str]:
        words = [word for word in re.findall(r"[a-z0-9]+", text.casefold()) if word not in self.stop_words]
        tokens = []
        for size in range(self.ngram_range[0], self.ngram_range[1] + 1):
            tokens.extend("_".join(words[index:index + size]) for index in range(len(words) - size + 1))
        return tokens

    def fit_transform(self, content: list[str]) -> sparse.csr_matrix:
        tokenized = [self._tokens(text) for text in content]
        document_frequency: dict[str, int] = {}
        for tokens in tokenized:
            for token in set(tokens):
                document_frequency[token] = document_frequency.get(token, 0) + 1
        self.vocabulary_ = {token: index for index, token in enumerate(sorted(document_frequency))}
        count = len(content)
        self.idf_ = np.array([math.log((1 + count) / (1 + document_frequency[token])) + 1 for token in self.vocabulary_])
        return self._transform_tokens(tokenized)

    def _transform_tokens(self, tokenized: list[list[str]]) -> sparse.csr_matrix:
        rows, columns, values = [], [], []
        for row_index, tokens in enumerate(tokenized):
            frequencies: dict[int, int] = {}
            for token in tokens:
                if token in self.vocabulary_:
                    column = self.vocabulary_[token]
                    frequencies[column] = frequencies.get(column, 0) + 1
            weights = {column: frequency * self.idf_[column] for column, frequency in frequencies.items()}
            norm = math.sqrt(sum(value * value for value in weights.values())) or 1.0
            for column, value in weights.items():
                rows.append(row_index)
                columns.append(column)
                values.append(value / norm)
        return sparse.csr_matrix((values, (rows, columns)), shape=(len(tokenized), len(self.vocabulary_)))

    def transform(self, content: list[str]) -> sparse.csr_matrix:
        return self._transform_tokens([self._tokens(text) for text in content])


class ContentVectorizer:
    """Fit once offline, then transform content using the same vocabulary."""

    def __init__(self, **kwargs: object) -> None:
        vectorizer_type = TfidfVectorizer or _FallbackTfidfVectorizer
        self.vectorizer = vectorizer_type(
            stop_words=kwargs.get("stop_words", "english"),
            ngram_range=kwargs.get("ngram_range", (1, 2)),
            min_df=kwargs.get("min_df", 1),
            max_df=kwargs.get("max_df", 1.0),
            max_features=kwargs.get("max_features"),
        )

    def fit_transform(self, content: list[str]) -> sparse.csr_matrix:
        """Fit vocabulary and return a sparse TF-IDF matrix."""
        if not any(text.strip() for text in content):
            raise ValueError("Cannot fit TF-IDF on completely empty content.")
        return self.vectorizer.fit_transform(content).tocsr()

    def transform(self, content: list[str]) -> sparse.csr_matrix:
        """Transform inference content without refitting."""
        return self.vectorizer.transform(content).tocsr()

    def save(self, path: str | Path) -> None:
        import joblib

        joblib.dump(self.vectorizer, path)

    @classmethod
    def load(cls, path: str | Path) -> "ContentVectorizer":
        import joblib

        instance = cls()
        instance.vectorizer = joblib.load(path)
        return instance
