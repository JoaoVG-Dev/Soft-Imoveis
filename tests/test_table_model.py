from __future__ import annotations

from PySide6.QtCore import Qt

from src.application.dto import ColumnDefinition
from src.ui.models import RecordsTableModel


def test_table_model_exposes_rows_and_headers() -> None:
    model = RecordsTableModel(
        (ColumnDefinition("codigo", "Código"), ColumnDefinition("valor", "Valor", align="right")),
        ({"codigo": "COB-002", "valor": "R$ 20,00"}, {"codigo": "COB-001", "valor": "R$ 10,00"}),
    )
    assert model.rowCount() == 2
    assert model.columnCount() == 2
    assert model.headerData(0, Qt.Orientation.Horizontal) == "Código"
    assert model.index(0, 0).data() == "COB-002"


def test_table_model_sorts_money_values() -> None:
    model = RecordsTableModel(
        (ColumnDefinition("codigo", "Código"), ColumnDefinition("valor", "Valor", align="right")),
        ({"codigo": "A", "valor": "R$ 20,00"}, {"codigo": "B", "valor": "R$ 10,00"}),
    )
    model.sort(1, Qt.SortOrder.AscendingOrder)
    assert model.index(0, 0).data() == "B"

