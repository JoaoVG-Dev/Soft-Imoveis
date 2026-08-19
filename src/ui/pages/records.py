"""Generic records page."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QWidget

from src.application.dto import PageDefinition
from src.application.services import DemoDataStore
from src.ui.dialogs import BoletoEmissionDialog, RecordDetailDialog
from src.ui.pages.dashboard import show_development_message
from src.ui.widgets import PageHeader, SearchableTable


class RecordsPage(QWidget):
    def __init__(self, definition: PageDefinition, data_store: DemoDataStore) -> None:
        super().__init__()
        self.setObjectName("Page")
        self._definition = definition
        self._data_store = data_store

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        layout.addWidget(PageHeader(definition.title, definition.subtitle))

        self.table = SearchableTable(
            columns=definition.columns,
            rows=definition.rows,
            filters=definition.filters,
            search_placeholder=definition.search_placeholder,
            actions=definition.actions,
        )
        self.table.record_opened.connect(self._open_record)
        self.table.action_triggered.connect(self._handle_action)
        layout.addWidget(self.table, 1)

    def _open_record(self, row: dict[str, object]) -> None:
        key = str(row.get("codigo", row.get("cobranca", "")))
        raw = self._data_store.raw_record(self._definition.key, key)
        detail = raw or row
        dialog = RecordDetailDialog(self._definition.title, detail, self._definition.detail_tabs, self)
        dialog.exec()

    def _handle_action(self, action: str, row: dict[str, object]) -> None:
        if action in ("Emitir boleto", "Emitir", "Reemitir"):
            if not row:
                QMessageBox.information(self, "Selecione um registro", "Escolha uma cobrança ou boleto antes de continuar.")
                return
            dialog = BoletoEmissionDialog(row, self)
            dialog.exec()
            return

        if action == "Cancelar":
            QMessageBox.information(
                self,
                "Cancelamento não executado",
                "Fluxo destrutivo mantido como mock. Nenhuma cobrança ou boleto foi alterado.",
            )
            return

        show_development_message(self)

