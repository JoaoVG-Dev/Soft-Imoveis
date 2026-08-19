"""Central navigation definition."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NavigationItem:
    key: str
    label: str
    group: str
    icon: str


NAVIGATION: tuple[NavigationItem, ...] = (
    NavigationItem("dashboard", "Visão Geral", "OPERAÇÃO", "dashboard.svg"),
    NavigationItem("landlords", "Locadores", "CADASTROS", "person.svg"),
    NavigationItem("tenants", "Locatários", "CADASTROS", "people.svg"),
    NavigationItem("properties", "Imóveis", "CADASTROS", "building.svg"),
    NavigationItem("contracts", "Contratos", "CONTRATOS", "document.svg"),
    NavigationItem("charges", "Cobranças", "COBRANÇAS", "invoice.svg"),
    NavigationItem("boletos", "Boletos", "COBRANÇAS", "barcode.svg"),
    NavigationItem("delinquency", "Inadimplência", "COBRANÇAS", "alert.svg"),
    NavigationItem("finance", "Financeiro", "FINANCEIRO", "money.svg"),
    NavigationItem("transfers", "Repasses", "REPASSES", "transfer.svg"),
    NavigationItem("reports", "Relatórios", "RELATÓRIOS", "report.svg"),
    NavigationItem("settings", "Configurações", "SISTEMA", "settings.svg"),
)


DEFAULT_ROUTE = "dashboard"
