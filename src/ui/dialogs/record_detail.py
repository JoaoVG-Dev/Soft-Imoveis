"""Record detail dialog."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class RecordDetailDialog(QDialog):
    def __init__(self, title: str, record: dict[str, object], tabs: tuple[str, ...], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(760, 520)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        heading = QLabel(title.upper())
        heading.setObjectName("PageTitle")
        layout.addWidget(heading)

        tab_widget = QTabWidget()
        for tab in tabs:
            tab_widget.addTab(_detail_tab(record, tab), tab.upper())
        layout.addWidget(tab_widget, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


def _detail_tab(record: dict[str, object], tab_name: str) -> QWidget:
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    content = QWidget()
    grid = QGridLayout(content)
    grid.setContentsMargins(12, 12, 12, 12)
    grid.setHorizontalSpacing(22)
    grid.setVerticalSpacing(10)

    if tab_name.lower() != "resumo":
        note = QLabel(
            "Estrutura preparada para descoberta futura. Nenhuma regra operacional foi assumida nesta aba."
        )
        note.setObjectName("HelperText")
        note.setWordWrap(True)
        grid.addWidget(note, 0, 0, 1, 2)
        start_row = 1
    else:
        start_row = 0

    for index, (key, value) in enumerate(record.items(), start=start_row):
        label = QLabel(str(key).replace("_", " ").upper())
        label.setObjectName("MetricLabel")
        value_label = QLabel(str(value))
        value_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        value_label.setWordWrap(True)
        grid.addWidget(label, index, 0)
        grid.addWidget(value_label, index, 1)
    grid.setColumnStretch(1, 1)
    scroll.setWidget(content)
    return scroll

