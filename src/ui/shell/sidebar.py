"""Sidebar navigation."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout

from src.application.services import NAVIGATION, NavigationItem
from src.core.paths import asset_path
from src.ui.styles.tokens import Metrics


class Sidebar(QFrame):
    navigate_requested = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(Metrics.SIDEBAR_WIDTH)
        self._buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(0)

        current_group = None
        for item in NAVIGATION:
            if item.group != current_group:
                current_group = item.group
                group_label = QLabel(current_group)
                group_label.setObjectName("SidebarGroup")
                layout.addWidget(group_label)
            layout.addWidget(self._button_for(item))
        layout.addStretch(1)
        self.set_active("dashboard")

    def set_active(self, key: str) -> None:
        for button_key, button in self._buttons.items():
            button.setProperty("active", button_key == key)
            button.style().unpolish(button)
            button.style().polish(button)

    def _button_for(self, item: NavigationItem) -> QPushButton:
        button = QPushButton(item.label)
        button.setObjectName("NavButton")
        button.setIcon(QIcon(str(asset_path("icons", item.icon))))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda checked=False, key=item.key: self.navigate_requested.emit(key))
        self._buttons[item.key] = button
        return button
