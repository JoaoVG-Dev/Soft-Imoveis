from __future__ import annotations

from src.app.router import Router
from src.application.services import DEFAULT_ROUTE, NAVIGATION


def test_navigation_has_required_routes() -> None:
    keys = {item.key for item in NAVIGATION}
    expected = {
        "dashboard",
        "landlords",
        "tenants",
        "properties",
        "contracts",
        "charges",
        "boletos",
        "delinquency",
        "finance",
        "transfers",
        "reports",
        "settings",
    }
    assert expected.issubset(keys)
    assert DEFAULT_ROUTE == "dashboard"


def test_router_registers_and_resolves_routes() -> None:
    router = Router(DEFAULT_ROUTE)
    router.register("dashboard", lambda: "page")
    assert router.resolve("dashboard") == "page"
    assert router.current_route == "dashboard"

