"""Qt table model for reusable list pages."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QColor

from src.application.dto import ColumnDefinition
from src.application.dto.records import Row
from src.core.search import normalize_search
from src.ui.styles.tokens import Colors


class RecordsTableModel(QAbstractTableModel):
    def __init__(self, columns: tuple[ColumnDefinition, ...], rows: tuple[Row, ...]) -> None:
        super().__init__()
        self._columns = columns
        self._rows = list(rows)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> object:
        if not index.isValid():
            return None

        row = self._rows[index.row()]
        column = self._columns[index.column()]
        value = row.get(column.key, "")

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            horizontal = Qt.AlignmentFlag.AlignRight if column.align == "right" else Qt.AlignmentFlag.AlignLeft
            return int(horizontal | Qt.AlignmentFlag.AlignVCenter)

        if role == Qt.ItemDataRole.ForegroundRole and column.key == "status":
            status = normalize_search(value)
            if any(word in status for word in ("vencid", "pendente", "atras", "cancel")):
                return QColor(Colors.ATTENTION_DARK)
            if any(word in status for word in ("ativo", "paga", "baixado", "recebido", "realizado", "locado")):
                return QColor(Colors.ACCENT_TEXT)

        if role == Qt.ItemDataRole.UserRole:
            return row

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._columns[section].label
        return str(section + 1)

    def sort(self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder) -> None:
        if column < 0 or column >= len(self._columns):
            return
        key = self._columns[column].key
        reverse = order == Qt.SortOrder.DescendingOrder
        self.layoutAboutToBeChanged.emit()
        self._rows.sort(key=lambda row: _sort_value(row.get(key, "")), reverse=reverse)
        self.layoutChanged.emit()

    def update_rows(self, rows: tuple[Row, ...]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def row_at(self, row_index: int) -> Row | None:
        if row_index < 0 or row_index >= len(self._rows):
            return None
        return self._rows[row_index]


def _sort_value(value: object) -> tuple[int, object]:
    text = str(value)
    money = text.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return (0, Decimal(money))
    except (InvalidOperation, ValueError):
        return (1, normalize_search(text))

