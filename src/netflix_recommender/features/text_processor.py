"""Lightweight text normalization used before feature construction."""

import re


def normalize_content(text: str) -> str:
    """Normalize whitespace and case while leaving meaningful tokens intact."""
    return re.sub(r"\s+", " ", text.casefold()).strip()
