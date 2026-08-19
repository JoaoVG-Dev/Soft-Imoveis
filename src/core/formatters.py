"""Formatting helpers for dates and money."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP


def format_date(value: date | datetime | None) -> str:
    if value is None:
        return "-"
    if isinstance(value, datetime):
        value = value.date()
    return value.strftime("%d/%m/%Y")


def format_brl(value: Decimal | int | str | None) -> str:
    if value is None:
        return "R$ 0,00"

    decimal_value = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sign = "-" if decimal_value < 0 else ""
    decimal_value = abs(decimal_value)
    integer_part, cents = f"{decimal_value:.2f}".split(".")

    groups: list[str] = []
    while integer_part:
        groups.append(integer_part[-3:])
        integer_part = integer_part[:-3]
    grouped = ".".join(reversed(groups))
    return f"{sign}R$ {grouped},{cents}"

