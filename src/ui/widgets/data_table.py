"""Reusable searchable, filterable and paginated table."""

from __future__ import annotations

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.application.dto import ColumnDefinition, FilterDefinition
from src.application.dto.records import Row
from src.core.search import text_matches_query
from src.ui.models import RecordsTableModel
from src.ui.widgets.filter_chip import FilterChip
from src.ui.widgets.message_panel import MessagePanel


class SearchableTable(QWidget):
    record_opened = Signal(dict)
    action_triggered = Signal(str, dict)

    def __init__(
        self,
        columns: tuple[ColumnDefinition, ...],
        rows: tuple[Row, ...],
        filters: tuple[FilterDefinition, ...],
        search_placeholder: str,
        actions: tuple[str, ...] = ("Abrir", "Cadastrar", "Editar"),
        page_size: int = 8,
    ) -> None:
        super().__init__()
        self._columns = columns
        self._all_rows = tuple(rows)
        self._filters = filters
        self._active_filter = filters[0].key if filters else ""
        self._page_size = page_size
        self._page = 0
        self._filtered_rows: tuple[Row, ...] = tuple(rows)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setSpacing(8)

        self.search = QLineEdit()
        self.search.setPlaceholderText(search_placeholder)
        self.search.textChanged.connect(self._apply_filters)
        toolbar.addWidget(self.search, 1)

        for action in actions:
            button = QPushButton(action)
            if action in ("Cadastrar", "Emitir", "Emitir boleto"):
                button.setObjectName("PrimaryActionButton")
            elif action == "Cancelar":
                button.setObjectName("DangerButton")
            else:
                button.setObjectName("ActionButton")
            button.clicked.connect(lambda checked=False, action=action: self._trigger_action(action))
            toolbar.addWidget(button)

        root.addLayout(toolbar)

        chips = QHBoxLayout()
        chips.setContentsMargins(0, 0, 0, 0)
        chips.setSpacing(7)
        self._chips: dict[str, FilterChip] = {}
        for filter_definition in filters:
            chip = FilterChip(filter_definition.label, filter_definition.key)
            chip.clicked.connect(lambda checked=False, key=filter_definition.key: self._select_filter(key))
            self._chips[filter_definition.key] = chip
            chips.addWidget(chip)
        chips.addStretch(1)
        root.addLayout(chips)

        frame = QFrame()
        frame.setObjectName("SectionFrame")
        frame_layout = QStackedLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        self._stack = frame_layout

        self.model = RecordsTableModel(columns, tuple())
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.doubleClicked.connect(self._open_selected)
        for index, column in enumerate(columns):
            self.table.setColumnWidth(index, column.width)
        frame_layout.addWidget(self.table)

        self.empty = MessagePanel(
            "NENHUM REGISTRO ENCONTRADO",
            "Não existem registros correspondentes aos filtros atuais.",
            "Limpar filtros",
        )
        frame_layout.addWidget(self.empty)

        root.addWidget(frame, 1)

        pagination = QHBoxLayout()
        pagination.setContentsMargins(0, 0, 0, 0)
        pagination.addStretch(1)
        self.counter = QLabel("")
        self.counter.setObjectName("MutedLabel")
        self.previous_button = QPushButton("Anterior")
        self.next_button = QPushButton("Próxima")
        self.previous_button.clicked.connect(self._previous_page)
        self.next_button.clicked.connect(self._next_page)
        pagination.addWidget(self.counter)
        pagination.addWidget(self.previous_button)
        pagination.addWidget(self.next_button)
        root.addLayout(pagination)

        self._refresh_chip_labels()
        self._select_filter(self._active_filter)

    def selected_row(self) -> Row | None:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return None
        return self.model.row_at(indexes[0].row())

    def set_loading(self, message: str = "Carregando registros...") -> None:
        self.empty = MessagePanel("CARREGANDO", message)
        self._stack.addWidget(self.empty)
        self._stack.setCurrentWidget(self.empty)

    def set_error(self, message: str) -> None:
        self.empty = MessagePanel("NÃO FOI POSSÍVEL CARREGAR", message, "Tentar novamente")
        self._stack.addWidget(self.empty)
        self._stack.setCurrentWidget(self.empty)

    def _select_filter(self, key: str) -> None:
        self._active_filter = key
        for chip_key, chip in self._chips.items():
            chip.setChecked(chip_key == key)
        self._page = 0
        self._apply_filters()

    def _apply_filters(self) -> None:
        query = self.search.text()
        filter_definition = next((item for item in self._filters if item.key == self._active_filter), None)
        filtered: list[Row] = []
        for row in self._all_rows:
            if filter_definition is not None and not filter_definition.predicate(row):
                continue
            if not text_matches_query(row.values(), query):
                continue
            filtered.append(row)
        self._filtered_rows = tuple(filtered)
        self._page = min(self._page, self._max_page())
        self._update_page()
        self._refresh_chip_labels()

    def _update_page(self) -> None:
        start = self._page * self._page_size
        end = start + self._page_size
        page_rows = self._filtered_rows[start:end]
        self.model.update_rows(tuple(page_rows))
        if page_rows:
            self._stack.setCurrentWidget(self.table)
        else:
            self._stack.setCurrentWidget(self.empty)

        total = len(self._filtered_rows)
        if total == 0:
            self.counter.setText("0 registros")
        else:
            self.counter.setText(f"{start + 1}-{min(end, total)} de {total}")
        self.previous_button.setEnabled(self._page > 0)
        self.next_button.setEnabled(self._page < self._max_page())

    def _refresh_chip_labels(self) -> None:
        for filter_definition in self._filters:
            count = sum(1 for row in self._all_rows if filter_definition.predicate(row))
            chip = self._chips.get(filter_definition.key)
            if chip is not None:
                chip.setText(f"{filter_definition.label} {count:02d}")

    def _max_page(self) -> int:
        if not self._filtered_rows:
            return 0
        return (len(self._filtered_rows) - 1) // self._page_size

    def _previous_page(self) -> None:
        self._page = max(0, self._page - 1)
        self._update_page()

    def _next_page(self) -> None:
        self._page = min(self._max_page(), self._page + 1)
        self._update_page()

    def _open_selected(self) -> None:
        row = self.selected_row()
        if row is not None:
            self.record_opened.emit(dict(row))

    def _trigger_action(self, action: str) -> None:
        row = self.selected_row() or {}
        if action in ("Abrir", "Visualizar", "Abrir cobrança"):
            if row:
                self.record_opened.emit(dict(row))
            return
        self.action_triggered.emit(action, dict(row))
