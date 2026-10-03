# Limitations

- Recommendations are metadata similarity, not personalized user recommendations.
- No watch history, ratings, or relevance labels are fabricated or inferred.
- Duplicate title strings are deduplicated by retaining the first row, so editions with the same title are not separately addressable.
- TF-IDF is lexical and may miss semantic relationships and spelling variants.
- Similarity is based on one combined text document; field weighting has not been tuned.
- A production deployment should add artifact checksums, authentication, rate limits, metrics, and a versioned model registry.

Future improvements include hybrid or collaborative filtering when feedback exists, transformer embeddings, user profiles, feedback loops, and a vector database for very large catalogs.
