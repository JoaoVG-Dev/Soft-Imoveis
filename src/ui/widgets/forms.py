"""Form controls with visible labels."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QLineEdit, QSizePolicy, QVBoxLayout, QWidget


class FormField(QWidget):
    def __init__(
        self,
        label: str,
        value: str = "",
        helper: str = "",
        read_only: bool = False,
    ) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label_widget = QLabel(label)
        label_widget.setObjectName("FieldLabel")
        label_widget.setProperty("weight", "strong")

        self.input = QLineEdit(value)
        self.input.setReadOnly(read_only)

        layout.addWidget(label_widget)
        layout.addWidget(self.input)

        if helper:
            helper_label = QLabel(helper)
            helper_label.setObjectName("HelperText")
            helper_label.setWordWrap(True)
            layout.addWidget(helper_label)

    def text(self) -> str:
        return self.input.text()

    def set_text(self, value: str) -> None:
        self.input.setText(value)
