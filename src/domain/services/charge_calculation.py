"""Charge calculation boundaries.

No real formula for multa, juros or correcao is implemented here. The demo
service only sums explicit values provided by mock data or UI input.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True)
class ChargeCalculationInput:
    base_value: Decimal
    fine: Decimal = Decimal("0.00")
    interest: Decimal = Decimal("0.00")
    correction: Decimal = Decimal("0.00")
    other_items: Decimal = Decimal("0.00")


@dataclass(frozen=True)
class ChargeCalculationResult:
    total: Decimal
    fine: Decimal
    interest: Decimal
    correction: Decimal
    other_items: Decimal
    notes: str


class ChargeCalculationService(Protocol):
    def calculate(self, charge_input: ChargeCalculationInput) -> ChargeCalculationResult:
        ...


class DemoChargeCalculationService:
    """Mock implementation for screen flow only."""

    def calculate(self, charge_input: ChargeCalculationInput) -> ChargeCalculationResult:
        total = (
            charge_input.base_value
            + charge_input.fine
            + charge_input.interest
            + charge_input.correction
            + charge_input.other_items
        )
        return ChargeCalculationResult(
            total=total,
            fine=charge_input.fine,
            interest=charge_input.interest,
            correction=charge_input.correction,
            other_items=charge_input.other_items,
            notes="DEMO DATA: valores informados manualmente, sem regra financeira real.",
        )

