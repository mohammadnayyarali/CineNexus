# Architecture

CineNexus separates offline model construction from online serving.

```mermaid
flowchart TD
    A[Netflix CSV] --> B[Loader and Validator]
    B --> C[Preprocessor]
    C --> D[Content Feature Builder]
    D --> E[TF-IDF Vectorizer]
    E --> F[Joblib Artifact]
    F --> G[Recommendation Engine]
    G --> H[FastAPI]
    G --> I[Streamlit]
```

The artifact contains cleaned metadata and a sparse TF-IDF matrix. The API loads it once during app creation. A request performs title lookup, cosine similarity against the query row, self-exclusion, and stable top-N ranking.

The engine does not import FastAPI or Streamlit, so it can also be reused by a CLI, batch job, or future service.
