"""Reports page."""

from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.application.dto import ColumnDefinition, FilterDefinition
from src.ui.dialogs import RecordDetailDialog
from src.ui.widgets import PageHeader, SearchableTable


class ReportsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Page")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        layout.addWidget(
            PageHeader(
                "Relatórios",
                "Estrutura inicial para categorias herdadas do fluxo administrativo, sem geração definitiva.",
            )
        )

        rows = tuple(
            {"codigo": f"REL-{index:03d}", "categoria": category, "escopo": scope, "status": "Preparado"}
            for index, (category, scope) in enumerate(
                (
                    ("Recibo do Locatário", "Locatário"),
                    ("Prestação de Contas ao Locador", "Locador"),
                    ("Aluguéis a Receber", "Financeiro"),
                    ("Aluguéis Recebidos", "Financeiro"),
                    ("Pagamentos a Realizar ao Locador", "Repasse"),
                    ("Pagamentos Realizados ao Locador", "Repasse"),
                    ("Contratos", "Contratos"),
                    ("Contratos a Vencer", "Contratos"),
                    ("Reajustes", "Contratos"),
                    ("Balancetes", "Financeiro"),
                    ("Inadimplência", "Cobranças"),
                    ("Taxas Administrativas", "Financeiro"),
                    ("Históricos", "Auditoria futura"),
                ),
                start=1,
            )
        )

        table = SearchableTable(
            columns=(
                ColumnDefinition("codigo", "Código", 100),
                ColumnDefinition("categoria", "Categoria", 320),
                ColumnDefinition("escopo", "Escopo", 180),
                ColumnDefinition("status", "Status", 135),
            ),
            rows=rows,
            filters=(
                FilterDefinition("all", "Todos", lambda row: True),
                FilterDefinition("finance", "Financeiro", lambda row: row.get("escopo") == "Financeiro"),
                FilterDefinition("contracts", "Contratos", lambda row: row.get("escopo") == "Contratos"),
            ),
            search_placeholder="Buscar relatório ou escopo...",
            actions=("Abrir",),
        )
        table.record_opened.connect(lambda row: RecordDetailDialog("Relatório", row, ("Resumo",), self).exec())
        layout.addWidget(table, 1)

