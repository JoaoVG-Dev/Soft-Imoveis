"""DTOs shared between application services and Qt pages."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


Row = dict[str, object]


@dataclass(frozen=True)
class ColumnDefinition:
    key: str
    label: str
    width: int = 120
    align: str = "left"


@dataclass(frozen=True)
class FilterDefinition:
    key: str
    label: str
    predicate: Callable[[Row], bool]


@dataclass(frozen=True)
class PageDefinition:
    key: str
    title: str
    subtitle: str
    search_placeholder: str
    columns: tuple[ColumnDefinition, ...]
    filters: tuple[FilterDefinition, ...]
    rows: tuple[Row, ...]
    actions: tuple[str, ...] = ("Abrir", "Cadastrar", "Editar")
    detail_tabs: tuple[str, ...] = ("Resumo",)

