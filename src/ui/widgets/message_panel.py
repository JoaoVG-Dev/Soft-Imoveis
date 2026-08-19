"""Message panel for empty, loading and error states."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class MessagePanel(QWidget):
    def __init__(self, title: str, message: str, action_label: str = "") -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("EmptyTitle")
        title_label.setWordWrap(True)
        message_label = QLabel(message)
        message_label.setObjectName("MutedLabel")
        message_label.setWordWrap(True)

        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addWidget(message_label)
        if action_label:
            button = QPushButton(action_label)
            button.setObjectName("PrimaryButton")
            layout.addWidget(button)
        layout.addStretch(1)

