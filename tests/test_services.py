from __future__ import annotations

from decimal import Decimal

from src.domain.services import ChargeCalculationInput, DemoChargeCalculationService


def test_demo_charge_calculation_only_sums_explicit_values() -> None:
    service = DemoChargeCalculationService()
    result = service.calculate(ChargeCalculationInput(base_value=Decimal("100.00")))
    assert result.total == Decimal("100.00")
    assert "DEMO DATA" in result.notes


def test_demo_charge_calculation_accepts_manual_components_without_percent_formula() -> None:
    service = DemoChargeCalculationService()
    result = service.calculate(
        ChargeCalculationInput(
            base_value=Decimal("100.00"),
            fine=Decimal("5.00"),
            interest=Decimal("2.00"),
            correction=Decimal("1.00"),
            other_items=Decimal("3.00"),
        )
    )
    assert result.total == Decimal("111.00")

