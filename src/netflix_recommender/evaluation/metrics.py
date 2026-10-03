"""Evaluation metrics that require explicit relevance labels."""


def precision_at_k(recommended: list[str], relevant: set[str], k: int) -> float:
    """Compute Precision@K; callers must supply real relevance labels."""
    if k < 1:
        raise ValueError("k must be at least 1")
    top_k = recommended[:k]
    return sum(title in relevant for title in top_k) / k
