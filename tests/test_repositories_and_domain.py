from __future__ import annotations

from src.application.services import DemoDataStore
from src.domain.entities import Boleto, Charge, Contract, Landlord, Payment, Property, Settlement, Tenant, Transfer


def test_demo_data_exposes_main_domain_models() -> None:
    data = DemoDataStore()
    assert isinstance(data.landlords.list()[0], Landlord)
    assert isinstance(data.tenants.list()[0], Tenant)
    assert isinstance(data.properties.list()[0], Property)
    assert isinstance(data.contracts.list()[0], Contract)
    assert isinstance(data.charges.list()[0], Charge)
    assert isinstance(data.boletos.list()[0], Boleto)
    assert isinstance(data.payments.list()[0], Payment)
    assert isinstance(data.settlements.list()[0], Settlement)
    assert isinstance(data.transfers.list()[0], Transfer)


def test_in_memory_repository_get_and_accent_insensitive_search() -> None:
    data = DemoDataStore()
    assert data.tenants.get("LAT-001").name == "João Silva"
    matches = data.tenants.search("joao")
    assert [item.code for item in matches] == ["LAT-001"]


def test_page_definitions_are_populated() -> None:
    data = DemoDataStore()
    page = data.page("boletos")
    assert page.title == "Boletos"
    assert page.rows
    assert any(action == "Emitir" for action in page.actions)

