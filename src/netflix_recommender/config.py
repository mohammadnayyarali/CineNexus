"""Environment-backed application settings."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Paths and runtime limits used by offline and online components."""

    dataset_path: Path = Path("data/raw/netflix_titles.csv")
    artifact_path: Path = Path("data/artifacts/recommender.joblib")
    content_fields: tuple[str, ...] = ("type", "listed_in", "director", "cast", "country", "rating", "description")
    max_top_n: int = 50
    log_level: str = "INFO"

    @classmethod
    def from_environment(cls) -> "Settings":
        fields = tuple(filter(None, os.getenv("CONTENT_FIELDS", ",".join(cls.content_fields)).split(",")))
        return cls(
            dataset_path=Path(os.getenv("DATASET_PATH", str(cls.dataset_path))),
            artifact_path=Path(os.getenv("ARTIFACT_PATH", str(cls.artifact_path))),
            content_fields=fields,
            max_top_n=int(os.getenv("MAX_TOP_N", str(cls.max_top_n))),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
        )
