"""In-memory repositories used by the first functional demo."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Generic, TypeVar

from src.core.search import text_matches_query

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(
        self,
        records: Iterable[T],
        key_getter: Callable[[T], str],
        searchable_fields: Iterable[str],
    ) -> None:
        self._records = list(records)
        self._key_getter = key_getter
        self._searchable_fields = tuple(searchable_fields)

    def list(self) -> list[T]:
        return list(self._records)

    def get(self, key: str) -> T | None:
        return next((record for record in self._records if self._key_getter(record) == key), None)

    def search(self, query: str) -> list[T]:
        return [
            record
            for record in self._records
            if text_matches_query(
                (getattr(record, field, "") for field in self._searchable_fields),
                query,
            )
        ]

