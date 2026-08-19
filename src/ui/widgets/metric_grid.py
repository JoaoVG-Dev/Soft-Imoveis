"""Operational metrics grid."""

from __future__ import annotations

from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from src.application.dto.records import Row


class MetricGrid(QWidget):
    def __init__(self, metrics: tuple[Row, ...]) -> None:
        super().__init__()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        band = QFrame()
        band.setObjectName("MetricBand")
        layout = QGridLayout(band)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        column_count = min(5, max(1, len(metrics)))
        for column in range(column_count):
            layout.setColumnStretch(column, 1)

        for index, metric in enumerate(metrics):
            cell = QFrame()
            cell.setObjectName("MetricCell")
            cell.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(14, 9, 14, 11)
            cell_layout.setSpacing(5)

            label = QLabel(str(metric["label"]).upper())
            label.setObjectName("MetricLabel")
            value = QLabel(str(metric["value"]))
            value.setObjectName("MetricValue")
            value.setProperty("tone", metric.get("tone", "default"))

            cell_layout.addWidget(label)
            cell_layout.addWidget(value)
            row = index // column_count
            column = index % column_count
            layout.addWidget(cell, row, column)
        root.addWidget(band)
