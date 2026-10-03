"""Validate and report the cleaned catalog without building model artifacts."""

import argparse

from netflix_recommender.config import Settings
from netflix_recommender.data.loader import load_dataset
from netflix_recommender.data.preprocessor import preprocess_dataset
from netflix_recommender.data.validator import validate_dataset


def main() -> None:
    settings = Settings.from_environment()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default=str(settings.dataset_path))
    args = parser.parse_args()
    raw = load_dataset(args.dataset)
    report = validate_dataset(raw)
    cleaned = preprocess_dataset(raw)
    print(f"Rows: {report.row_count}; cleaned rows: {len(cleaned)}")
    print(f"Duplicate titles removed: {report.duplicate_title_count}")
    print(f"Missing values: {report.missing_values}")


if __name__ == "__main__":
    main()
