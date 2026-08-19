from __future__ import annotations

from PySide6.QtWidgets import QApplication

from src.app.application import SoftImoveisApplication
from src.application.services import NAVIGATION


def test_application_initializes_and_smoke_navigates() -> None:
    qt_app = QApplication.instance() or QApplication([])
    app = SoftImoveisApplication(["--smoke-test"])
    visited = app.window.smoke_navigation()
    assert visited == tuple(item.key for item in NAVIGATION)
    assert app.state.current_route == NAVIGATION[-1].key
    qt_app.processEvents()

