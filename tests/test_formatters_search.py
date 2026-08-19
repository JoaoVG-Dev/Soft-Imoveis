from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from src.core.formatters import format_brl, format_date
from src.core.search import normalize_search, text_matches_query


def test_format_brl_uses_brazilian_format() -> None:
    assert format_brl(Decimal("1234.56")) == "R$ 1.234,56"
    assert format_brl(Decimal("-12.3")) == "-R$ 12,30"
    assert format_brl(None) == "R$ 0,00"


def test_format_date_accepts_date_and_datetime() -> None:
    assert format_date(date(2026, 8, 18)) == "18/08/2026"
    assert format_date(datetime(2026, 8, 18, 12, 30)) == "18/08/2026"
    assert format_date(None) == "-"


def test_normalize_search_ignores_accents_case_and_extra_spaces() -> None:
    assert normalize_search(" João   SILVA ") == "joao silva"
    assert normalize_search("SOFT-IMÓVEIS") == "soft-imoveis"
    assert text_matches_query(["Maria Oliveira", "Apto 302"], "maria")
    assert text_matches_query(["João Silva"], "JOAO")

