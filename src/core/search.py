"""Search normalization helpers."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable


def normalize_search(value: object) -> str:
    """Normalize text for accent-insensitive, case-insensitive search."""

    text = "" if value is None else str(value)
    decomposed = unicodedata.normalize("NFD", text)
    without_accents = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    compact = re.sub(r"\s+", " ", without_accents)
    return compact.strip().casefold()


def text_matches_query(values: Iterable[object], query: str) -> bool:
    needle = normalize_search(query)
    if not needle:
        return True
    haystack = " ".join(normalize_search(value) for value in values)
    return needle in haystack

