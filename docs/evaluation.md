# Evaluation

Run `python scripts/evaluate.py --artifact data/artifacts/recommender.joblib` after building an artifact. The script reports catalog size, a real catalog example, and request latency.

Qualitative evaluation should inspect recommendations for titles from different genres and formats. Coverage can be measured as the fraction of catalog titles that can be used as queries. Precision@K requires external relevance labels, editorial judgments, user clicks, or watch history. None are present in the metadata-only input, so no precision number is claimed.
