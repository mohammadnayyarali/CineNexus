"""Produce metadata-only evaluation information and examples."""

import argparse
import time

from netflix_recommender.config import Settings
from netflix_recommender.recommender.artifacts import load_engine


def main() -> None:
    settings = Settings.from_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", default=str(settings.artifact_path))
    parser.add_argument("--title", default=None)
    args = parser.parse_args()
    engine = load_engine(args.artifact)
    title = args.title or engine.titles()[0]
    started = time.perf_counter()
    results = engine.recommend(title, 5)
    elapsed_ms = (time.perf_counter() - started) * 1000
    print(f"Catalog titles: {len(engine.metadata)}")
    print(f"Example query: {title}")
    print(f"Recommendation latency: {elapsed_ms:.2f} ms")
    for item in results:
        print(f"- {item['title']} ({item['similarity_score']:.3f})")
    print("Precision@K is unavailable without relevance labels or user feedback.")


if __name__ == "__main__":
    main()
