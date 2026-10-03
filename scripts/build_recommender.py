"""Build the offline recommendation artifact."""

import argparse

from netflix_recommender.config import Settings
from netflix_recommender.logging_config import configure_logging
from netflix_recommender.recommender.artifacts import build_artifact


def main() -> None:
    settings = Settings.from_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(settings.dataset_path))
    parser.add_argument("--output", default=str(settings.artifact_path))
    args = parser.parse_args()
    configure_logging(settings.log_level)
    try:
        build_artifact(args.dataset, args.output, list(settings.content_fields))
    except FileNotFoundError:
        raise SystemExit(
            f"Dataset not found: {args.dataset}\n"
            "Place the real Netflix CSV there or pass --dataset <path-to-csv>."
        ) from None


if __name__ == "__main__":
    main()
