"""Dashboard page."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QWidget

from src.application.dto import ColumnDefinition, FilterDefinition
from src.application.services import DemoDataStore
from src.ui.dialogs import RecordDetailDialog
from src.ui.widgets import MetricGrid, PageHeader, SearchableTable


class DashboardPage(QWidget):
    def __init__(self, data_store: DemoDataStore) -> None:
        super().__init__()
        self.setObjectName("Page")
        self._data_store = data_store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        layout.addWidget(
            PageHeader(
                "Visão Geral",
                "Painel operacional com indicadores fictícios para validação de navegação e densidade visual.",
            )
        )
        layout.addWidget(MetricGrid(data_store.dashboard_metrics()))

        recent_table = SearchableTable(
            columns=(
                ColumnDefinition("codigo", "Código", 92),
                ColumnDefinition("pessoa", "Pessoa", 190),
                ColumnDefinition("referencia", "Referência", 150),
                ColumnDefinition("vencimento", "Vencimento", 110),
                ColumnDefinition("valor", "Valor", 112, "right"),
                ColumnDefinition("status", "Status", 120),
            ),
            rows=data_store.recent_operations(),
            filters=(
                FilterDefinition("all", "Todos", lambda row: True),
                FilterDefinition("attention", "Atenção", lambda row: row.get("status") in ("Vencida", "A vencer")),
                FilterDefinition("paid", "Pagas", lambda row: row.get("status") == "Paga"),
            ),
            search_placeholder="Buscar operação, pessoa, referência ou status...",
            actions=("Abrir",),
            page_size=5,
        )
        recent_table.record_opened.connect(self._open_record)
        layout.addWidget(recent_table, 1)

    def _open_record(self, row: dict[str, object]) -> None:
        dialog = RecordDetailDialog("Operação", row, ("Resumo",), self)
        dialog.exec()


def show_development_message(parent: QWidget, title: str = "Funcionalidade em desenvolvimento") -> None:
    QMessageBox.information(
        parent,
        title,
        "Este fluxo está preparado visualmente, mas depende de regras reais e integrações futuras.",
    )

