"""Fictitious data and page definitions for the first desktop version."""

from __future__ import annotations

from dataclasses import asdict
from datetime import date
from decimal import Decimal

from src.application.dto import ColumnDefinition, FilterDefinition, PageDefinition
from src.application.dto.records import Row
from src.core.formatters import format_brl, format_date
from src.domain.entities import (
    BankAccount,
    Boleto,
    Charge,
    Contract,
    Landlord,
    Payment,
    Property,
    Settlement,
    Tenant,
    Transfer,
)
from src.infrastructure.repositories import InMemoryRepository


def _status_filter(key: str, label: str, accepted: tuple[str, ...]) -> FilterDefinition:
    return FilterDefinition(key, label, lambda row: str(row.get("status", "")) in accepted)


def _all_filter() -> FilterDefinition:
    return FilterDefinition("all", "Todos", lambda row: True)


class DemoDataStore:
    """Application service that exposes mock data to the UI."""

    def __init__(self) -> None:
        self.landlords = InMemoryRepository(
            _landlords(),
            lambda item: item.code,
            ("code", "name", "document", "phone", "email", "status"),
        )
        self.tenants = InMemoryRepository(
            _tenants(),
            lambda item: item.code,
            ("code", "name", "document", "phone", "email", "contract", "status"),
        )
        self.properties = InMemoryRepository(
            _properties(),
            lambda item: item.code,
            ("code", "address", "landlord", "current_tenant", "contract", "status"),
        )
        self.contracts = InMemoryRepository(
            _contracts(),
            lambda item: item.code,
            ("code", "property_ref", "landlord", "tenant", "status"),
        )
        self.charges = InMemoryRepository(
            _charges(),
            lambda item: item.code,
            ("code", "tenant", "property_ref", "competence", "boleto", "status"),
        )
        self.boletos = InMemoryRepository(
            _boletos(),
            lambda item: item.id,
            ("id", "charge_code", "tenant", "property_ref", "status"),
        )
        self.payments = InMemoryRepository(
            _payments(),
            lambda item: item.code,
            ("code", "charge_code", "payer", "status"),
        )
        self.settlements = InMemoryRepository(
            _settlements(),
            lambda item: item.code,
            ("code", "payment_code", "status", "notes"),
        )
        self.bank_accounts = InMemoryRepository(
            _bank_accounts(),
            lambda item: item.code,
            ("code", "label", "bank_name", "status"),
        )
        self.transfers = InMemoryRepository(
            _transfers(),
            lambda item: item.code,
            ("code", "landlord", "contract", "reference", "status"),
        )

    def dashboard_metrics(self) -> tuple[Row, ...]:
        return (
            {"label": "Contratos", "value": "428", "tone": "default"},
            {"label": "A vencer", "value": "31", "tone": "default"},
            {"label": "Vencidos", "value": "12", "tone": "attention"},
            {"label": "Repasses", "value": "07", "tone": "attention"},
        )

    def recent_operations(self) -> tuple[Row, ...]:
        return tuple(
            {
                "codigo": charge.code,
                "pessoa": charge.tenant,
                "referencia": charge.competence,
                "vencimento": format_date(charge.due_date),
                "valor": format_brl(charge.amount),
                "status": charge.status,
            }
            for charge in self.charges.list()
        )

    def page(self, key: str) -> PageDefinition:
        pages = {
            "landlords": self._landlords_page,
            "tenants": self._tenants_page,
            "properties": self._properties_page,
            "contracts": self._contracts_page,
            "charges": self._charges_page,
            "boletos": self._boletos_page,
            "delinquency": self._delinquency_page,
            "finance": self._finance_page,
            "transfers": self._transfers_page,
        }
        return pages[key]()

    def _landlords_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.code,
                "nome": item.name,
                "documento": item.document,
                "telefone": item.phone,
                "email": item.email,
                "imoveis": item.property_count,
                "status": item.status,
            }
            for item in self.landlords.list()
        )
        return PageDefinition(
            key="landlords",
            title="Locadores",
            subtitle="Cadastro provisório de proprietários com dados fictícios.",
            search_placeholder="Buscar por nome, documento, telefone ou e-mail...",
            columns=(
                ColumnDefinition("codigo", "Código", 82),
                ColumnDefinition("nome", "Nome", 210),
                ColumnDefinition("documento", "Documento", 135),
                ColumnDefinition("telefone", "Telefone", 120),
                ColumnDefinition("email", "E-mail", 210),
                ColumnDefinition("imoveis", "Imóveis", 90, "right"),
                ColumnDefinition("status", "Status", 110),
            ),
            filters=(_all_filter(), _status_filter("active", "Ativos", ("Ativo",)), _status_filter("inactive", "Inativos", ("Inativo",))),
            rows=rows,
        )

    def _tenants_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.code,
                "nome": item.name,
                "documento": item.document,
                "telefone": item.phone,
                "email": item.email,
                "contrato": item.contract,
                "status": item.status,
            }
            for item in self.tenants.list()
        )
        return PageDefinition(
            key="tenants",
            title="Locatários",
            subtitle="Cadastro provisório de locatários e vínculos contratuais.",
            search_placeholder="Buscar locatário, documento, contrato ou e-mail...",
            columns=(
                ColumnDefinition("codigo", "Código", 82),
                ColumnDefinition("nome", "Nome", 210),
                ColumnDefinition("documento", "Documento", 135),
                ColumnDefinition("telefone", "Telefone", 120),
                ColumnDefinition("email", "E-mail", 210),
                ColumnDefinition("contrato", "Contrato", 112),
                ColumnDefinition("status", "Status", 110),
            ),
            filters=(_all_filter(), _status_filter("active", "Ativos", ("Ativo",)), _status_filter("analysis", "Em análise", ("Em análise",))),
            rows=rows,
        )

    def _properties_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.code,
                "endereco": item.address,
                "locador": item.landlord,
                "locatario": item.current_tenant,
                "contrato": item.contract,
                "status": item.status,
            }
            for item in self.properties.list()
        )
        return PageDefinition(
            key="properties",
            title="Imóveis",
            subtitle="Imóveis administrados em mock operacional.",
            search_placeholder="Buscar por endereço, locador, locatário ou contrato...",
            columns=(
                ColumnDefinition("codigo", "Código", 82),
                ColumnDefinition("endereco", "Endereço", 280),
                ColumnDefinition("locador", "Locador", 180),
                ColumnDefinition("locatario", "Locatário atual", 180),
                ColumnDefinition("contrato", "Contrato", 110),
                ColumnDefinition("status", "Status", 130),
            ),
            filters=(_all_filter(), _status_filter("occupied", "Locados", ("Locado",)), _status_filter("vacant", "Vagos", ("Vago",))),
            rows=rows,
        )

    def _contracts_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.code,
                "imovel": item.property_ref,
                "locador": item.landlord,
                "locatario": item.tenant,
                "inicio": format_date(item.start_date),
                "vencimento": format_date(item.end_date),
                "valor_base": format_brl(item.base_value),
                "status": item.status,
            }
            for item in self.contracts.list()
        )
        return PageDefinition(
            key="contracts",
            title="Contratos",
            subtitle="Listagem contratual sem regras financeiras definitivas.",
            search_placeholder="Buscar contrato, imóvel, locador ou locatário...",
            columns=(
                ColumnDefinition("codigo", "Código", 92),
                ColumnDefinition("imovel", "Imóvel", 210),
                ColumnDefinition("locador", "Locador", 160),
                ColumnDefinition("locatario", "Locatário", 160),
                ColumnDefinition("inicio", "Início", 100),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor_base", "Valor base", 118, "right"),
                ColumnDefinition("status", "Status", 110),
            ),
            filters=(_all_filter(), _status_filter("active", "Ativos", ("Ativo",)), _status_filter("ending", "A vencer", ("A vencer",))),
            rows=rows,
            detail_tabs=("Resumo", "Partes", "Imóvel", "Valores", "Cobranças", "Histórico"),
        )

    def _charges_page(self) -> PageDefinition:
        rows = tuple(_charge_row(item) for item in self.charges.list())
        return PageDefinition(
            key="charges",
            title="Cobranças",
            subtitle="Cobranças mockadas, sem cálculo de multa, juros ou correção.",
            search_placeholder="Buscar locatário, imóvel, competência ou boleto...",
            columns=(
                ColumnDefinition("codigo", "Código", 92),
                ColumnDefinition("locatario", "Locatário", 190),
                ColumnDefinition("imovel", "Imóvel", 230),
                ColumnDefinition("competencia", "Competência", 115),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("boleto", "Boleto", 100),
                ColumnDefinition("status", "Situação", 120),
            ),
            filters=(
                _all_filter(),
                _status_filter("due", "A vencer", ("A vencer",)),
                _status_filter("overdue", "Vencidas", ("Vencida",)),
                _status_filter("paid", "Pagas", ("Paga",)),
            ),
            rows=rows,
            actions=("Abrir", "Emitir boleto", "Editar"),
        )

    def _boletos_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.id,
                "cobranca": item.charge_code,
                "locatario": item.tenant,
                "imovel": item.property_ref,
                "emissao": format_date(item.issue_date),
                "vencimento": format_date(item.due_date),
                "valor": format_brl(item.amount),
                "status": item.status,
            }
            for item in self.boletos.list()
        )
        return PageDefinition(
            key="boletos",
            title="Boletos",
            subtitle="Interface preparatória para emissão, reemissão e consulta.",
            search_placeholder="Buscar locatário, imóvel, documento ou cobrança...",
            columns=(
                ColumnDefinition("codigo", "Boleto", 95),
                ColumnDefinition("cobranca", "Cobrança", 100),
                ColumnDefinition("locatario", "Locatário", 185),
                ColumnDefinition("imovel", "Imóvel", 230),
                ColumnDefinition("emissao", "Emissão", 100),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("status", "Status", 115),
            ),
            filters=(
                _all_filter(),
                _status_filter("due", "A vencer", ("A vencer",)),
                _status_filter("overdue", "Vencidos", ("Vencido",)),
                _status_filter("settled", "Baixados", ("Baixado",)),
            ),
            rows=rows,
            actions=("Visualizar", "Abrir cobrança", "Emitir", "Reemitir", "Cancelar"),
        )

    def _delinquency_page(self) -> PageDefinition:
        rows = tuple(row for row in (_charge_row(item) for item in self.charges.list()) if row["status"] == "Vencida")
        return PageDefinition(
            key="delinquency",
            title="Inadimplência",
            subtitle="Recorte operacional de cobranças vencidas em dados mockados.",
            search_placeholder="Buscar locatário, imóvel ou competência...",
            columns=(
                ColumnDefinition("codigo", "Código", 92),
                ColumnDefinition("locatario", "Locatário", 190),
                ColumnDefinition("imovel", "Imóvel", 260),
                ColumnDefinition("competencia", "Competência", 115),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("status", "Situação", 120),
            ),
            filters=(_all_filter(), _status_filter("overdue", "Vencidas", ("Vencida",))),
            rows=rows,
            actions=("Abrir", "Emitir boleto"),
        )

    def _finance_page(self) -> PageDefinition:
        rows = (
            {
                "documento": "REC-0001",
                "pessoa": "João Silva",
                "referencia": "Aluguel 08/2026",
                "vencimento": "10/08/2026",
                "pagamento": "-",
                "valor": "R$ 2.450,00",
                "status": "A receber",
            },
            {
                "documento": "REC-0002",
                "pessoa": "Maria Oliveira",
                "referencia": "Aluguel 08/2026",
                "vencimento": "08/08/2026",
                "pagamento": "08/08/2026",
                "valor": "R$ 3.120,00",
                "status": "Recebido",
            },
            {
                "documento": "BX-0003",
                "pessoa": "Carlos Almeida",
                "referencia": "Baixa manual em validação",
                "vencimento": "05/08/2026",
                "pagamento": "07/08/2026",
                "valor": "R$ 1.980,00",
                "status": "Baixa pendente",
            },
        )
        return PageDefinition(
            key="finance",
            title="Financeiro",
            subtitle="Estrutura inicial para A receber, Recebidos e Baixas.",
            search_placeholder="Buscar documento, pessoa ou referência...",
            columns=(
                ColumnDefinition("documento", "Documento", 120),
                ColumnDefinition("pessoa", "Pessoa", 190),
                ColumnDefinition("referencia", "Referência", 240),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("pagamento", "Pagamento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("status", "Status", 135),
            ),
            filters=(
                _all_filter(),
                _status_filter("receivable", "A receber", ("A receber",)),
                _status_filter("received", "Recebidos", ("Recebido",)),
                _status_filter("settlement", "Baixas", ("Baixa pendente",)),
            ),
            rows=rows,
            actions=("Abrir",),
        )

    def _transfers_page(self) -> PageDefinition:
        rows = tuple(
            {
                "codigo": item.code,
                "locador": item.landlord,
                "contrato": item.contract,
                "referencia": item.reference,
                "vencimento": format_date(item.due_date),
                "valor": format_brl(item.amount),
                "status": item.status,
            }
            for item in self.transfers.list()
        )
        return PageDefinition(
            key="transfers",
            title="Repasses",
            subtitle="Módulos de A realizar, Realizados e Prestação de Contas sem cálculo definitivo.",
            search_placeholder="Buscar locador, contrato ou referência...",
            columns=(
                ColumnDefinition("codigo", "Código", 100),
                ColumnDefinition("locador", "Locador", 210),
                ColumnDefinition("contrato", "Contrato", 110),
                ColumnDefinition("referencia", "Referência", 180),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("status", "Status", 145),
            ),
            filters=(
                _all_filter(),
                _status_filter("pending", "A realizar", ("A realizar",)),
                _status_filter("done", "Realizados", ("Realizado",)),
                _status_filter("accounting", "Prestação", ("Prestação pendente",)),
            ),
            rows=rows,
            actions=("Abrir",),
        )

    def raw_record(self, entity: str, key: str) -> dict[str, object] | None:
        repositories = {
            "landlords": self.landlords,
            "tenants": self.tenants,
            "properties": self.properties,
            "contracts": self.contracts,
            "charges": self.charges,
            "boletos": self.boletos,
            "transfers": self.transfers,
        }
        repository = repositories.get(entity)
        if repository is None:
            return None
        record = repository.get(key)
        return asdict(record) if record is not None else None


def _charge_row(item: Charge) -> Row:
    return {
        "codigo": item.code,
        "locatario": item.tenant,
        "imovel": item.property_ref,
        "competencia": item.competence,
        "vencimento": format_date(item.due_date),
        "valor": format_brl(item.amount),
        "boleto": item.boleto,
        "status": item.status,
    }


def _landlords() -> tuple[Landlord, ...]:
    return (
        Landlord("LOC-001", "Maria Oliveira", "000.000.000-01", "(11) 3000-1001", "maria.demo@example.com", 3, "Ativo"),
        Landlord("LOC-002", "Carlos Almeida", "000.000.000-02", "(11) 3000-1002", "carlos.demo@example.com", 1, "Ativo"),
        Landlord("LOC-003", "Helena Duarte", "000.000.000-03", "(11) 3000-1003", "helena.demo@example.com", 2, "Inativo"),
        Landlord("LOC-004", "Roberto Martins", "000.000.000-04", "(11) 3000-1004", "roberto.demo@example.com", 4, "Ativo"),
    )


def _tenants() -> tuple[Tenant, ...]:
    return (
        Tenant("LAT-001", "João Silva", "111.111.111-01", "(11) 4000-2001", "joao.demo@example.com", "CTR-001", "Ativo"),
        Tenant("LAT-002", "Ana Pereira", "111.111.111-02", "(11) 4000-2002", "ana.demo@example.com", "CTR-002", "Ativo"),
        Tenant("LAT-003", "Bruno Costa", "111.111.111-03", "(11) 4000-2003", "bruno.demo@example.com", "CTR-003", "Em análise"),
        Tenant("LAT-004", "Lívia Santos", "111.111.111-04", "(11) 4000-2004", "livia.demo@example.com", "CTR-004", "Ativo"),
    )


def _properties() -> tuple[Property, ...]:
    return (
        Property("IMO-001", "Rua Exemplo, 100 - Apto 302", "Maria Oliveira", "João Silva", "CTR-001", "Locado"),
        Property("IMO-002", "Av. Central, 455 - Sala 12", "Carlos Almeida", "Ana Pereira", "CTR-002", "Locado"),
        Property("IMO-003", "Rua das Flores, 88 - Casa", "Helena Duarte", "-", "-", "Vago"),
        Property("IMO-004", "Alameda Norte, 77 - Apto 41", "Roberto Martins", "Lívia Santos", "CTR-004", "Locado"),
    )


def _contracts() -> tuple[Contract, ...]:
    return (
        Contract("CTR-001", "Rua Exemplo, 100 - Apto 302", "Maria Oliveira", "João Silva", date(2025, 8, 10), date(2027, 8, 9), Decimal("2450.00"), "Ativo"),
        Contract("CTR-002", "Av. Central, 455 - Sala 12", "Carlos Almeida", "Ana Pereira", date(2024, 11, 1), date(2026, 10, 31), Decimal("3120.00"), "A vencer"),
        Contract("CTR-003", "Rua das Flores, 88 - Casa", "Helena Duarte", "Bruno Costa", date(2026, 1, 15), date(2028, 1, 14), Decimal("1980.00"), "Em análise"),
        Contract("CTR-004", "Alameda Norte, 77 - Apto 41", "Roberto Martins", "Lívia Santos", date(2025, 3, 20), date(2027, 3, 19), Decimal("2760.00"), "Ativo"),
    )


def _charges() -> tuple[Charge, ...]:
    return (
        Charge("COB-001", "João Silva", "Rua Exemplo, 100 - Apto 302", "08/2026", date(2026, 8, 10), Decimal("2450.00"), "BOL-001", "Vencida"),
        Charge("COB-002", "Ana Pereira", "Av. Central, 455 - Sala 12", "08/2026", date(2026, 8, 25), Decimal("3120.00"), "BOL-002", "A vencer"),
        Charge("COB-003", "Lívia Santos", "Alameda Norte, 77 - Apto 41", "08/2026", date(2026, 8, 20), Decimal("2760.00"), "Não emitido", "A vencer"),
        Charge("COB-004", "João Silva", "Rua Exemplo, 100 - Apto 302", "07/2026", date(2026, 7, 10), Decimal("2450.00"), "BOL-004", "Paga"),
    )


def _boletos() -> tuple[Boleto, ...]:
    return (
        Boleto("BOL-001", "COB-001", "João Silva", "Rua Exemplo, 100 - Apto 302", date(2026, 8, 1), date(2026, 8, 10), Decimal("2450.00"), "Vencido"),
        Boleto("BOL-002", "COB-002", "Ana Pereira", "Av. Central, 455 - Sala 12", date(2026, 8, 1), date(2026, 8, 25), Decimal("3120.00"), "A vencer"),
        Boleto("BOL-004", "COB-004", "João Silva", "Rua Exemplo, 100 - Apto 302", date(2026, 7, 1), date(2026, 7, 10), Decimal("2450.00"), "Baixado"),
    )


def _payments() -> tuple[Payment, ...]:
    return (
        Payment("PAG-001", "COB-004", "João Silva", date(2026, 7, 9), Decimal("2450.00"), "Recebido"),
    )


def _settlements() -> tuple[Settlement, ...]:
    return (
        Settlement("BAI-001", "PAG-001", date(2026, 7, 9), "Baixado", "Baixa mockada para fluxo visual."),
    )


def _bank_accounts() -> tuple[BankAccount, ...]:
    return (
        BankAccount("CTA-001", "Conta operacional demonstrativa", None, None, None, "Pendente de descoberta"),
    )


def _transfers() -> tuple[Transfer, ...]:
    return (
        Transfer("REP-001", "Maria Oliveira", "CTR-001", "08/2026", date(2026, 8, 30), Decimal("2100.00"), "A realizar"),
        Transfer("REP-002", "Carlos Almeida", "CTR-002", "08/2026", date(2026, 8, 30), Decimal("2680.00"), "Prestação pendente"),
        Transfer("REP-003", "Maria Oliveira", "CTR-001", "07/2026", date(2026, 7, 30), Decimal("2100.00"), "Realizado"),
    )
