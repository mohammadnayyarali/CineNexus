"""Catalog cleaning and normalization."""

import re

import pandas as pd


def normalize_text(value: object) -> str:
    """Normalize missing values and whitespace while preserving useful punctuation."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def preprocess_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a clean, deterministic catalog with one row per title."""
    cleaned = frame.copy()
    for column in cleaned.columns:
        if cleaned[column].dtype == "object":
            cleaned[column] = cleaned[column].map(normalize_text)
    cleaned = cleaned[cleaned["title"] != ""].copy()
    cleaned = cleaned.drop_duplicates(subset=["title"], keep="first").reset_index(drop=True)
    return cleaned
