"""Filter chip widget."""

from __future__ import annotations

from PySide6.QtWidgets import QPushButton


class FilterChip(QPushButton):
    def __init__(self, label: str, key: str) -> None:
        super().__init__(label)
        self.key = key
        self.setObjectName("FilterChip")
        self.setCheckable(True)
        self.setCursor(self.cursor())

