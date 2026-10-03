"""Construction of configurable content text."""

import pandas as pd

DEFAULT_CONTENT_FIELDS = ["type", "listed_in", "director", "cast", "country", "rating", "description"]


def build_content_text(frame: pd.DataFrame, fields: list[str] | None = None) -> pd.Series:
    """Combine available configured fields; absent optional columns contribute no text."""
    selected_fields = fields or DEFAULT_CONTENT_FIELDS
    available = [field for field in selected_fields if field in frame.columns]
    if not available:
        return pd.Series([""] * len(frame), index=frame.index, dtype="object")
    return frame[available].fillna("").astype(str).agg(" ".join, axis=1).str.replace(r"\s+", " ", regex=True).str.strip()
