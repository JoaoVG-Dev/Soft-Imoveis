"""Qt application bootstrap."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QMessageBox

from src.app.state import AppState, SessionState
from src.application.services import DemoDataStore
from src.core.config import AppConfig, load_config
from src.core.logging import setup_logging
from src.core.paths import asset_path
from src.ui.shell import MainWindow
from src.ui.styles import build_stylesheet

LOGGER = logging.getLogger(__name__)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Soft-Imoveis desktop")
    parser.add_argument("--smoke-test", action="store_true", help="Create the window, navigate pages and exit.")
    parser.add_argument("--screenshot-dir", default="", help="Capture smoke screenshots into this directory.")
    return parser.parse_args(argv)


class SoftImoveisApplication:
    def __init__(self, argv: list[str] | None = None) -> None:
        self.argv = list(argv if argv is not None else sys.argv[1:])
        self.args = parse_args(self.argv)
        self.config = load_config()
        setup_logging(self.config)
        LOGGER.info("Starting Soft-Imoveis desktop")

        self.qt_app = QApplication.instance() or QApplication([sys.argv[0], *self.argv])
        self.qt_app.setApplicationName(self.config.app_name)
        self.qt_app.setApplicationVersion(self.config.app_version)
        font_family = self._load_fonts()
        self.qt_app.setFont(QFont(font_family, 10))
        self.qt_app.setStyleSheet(build_stylesheet(font_family))
        self._install_exception_hook()

        self.state = AppState(session=SessionState())
        self.data_store = DemoDataStore()
        self.window = MainWindow(self.config, self.state, self.data_store)

    def run(self) -> int:
        if self.args.smoke_test:
            self.window.resize(1366, 768)
            self.window.show()
            self.qt_app.processEvents()
            visited = self.window.smoke_navigation()
            LOGGER.info("Smoke navigation completed: %s", ", ".join(visited))
            if self.args.screenshot_dir:
                self._capture_screenshots(Path(self.args.screenshot_dir))
            QTimer.singleShot(100, self.qt_app.quit)
            return self.qt_app.exec()

        self.window.show()
        return self.qt_app.exec()

    def _capture_screenshots(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        for width, height in ((1366, 768), (1920, 1080)):
            self.window.resize(width, height)
            self.qt_app.processEvents()
            pixmap = self.window.grab()
            target = directory / f"softimoveis-{width}x{height}.png"
            pixmap.save(str(target))
            LOGGER.info("Saved screenshot: %s", target)

    def _load_fonts(self) -> str:
        fonts_dir = asset_path("fonts")
        loaded_families: list[str] = []

        if fonts_dir.exists():
            for font_path in fonts_dir.glob("*.ttf"):
                loaded_families.extend(_load_font_file(font_path))
        else:
            LOGGER.info("No bundled fonts directory found; using system fallback.")

        if "Archivo" in loaded_families:
            return "Archivo"

        windir = Path(os.getenv("WINDIR", r"C:\Windows"))
        for fallback in (windir / "Fonts" / "segoeui.ttf", windir / "Fonts" / "arial.ttf"):
            if fallback.exists():
                loaded_families.extend(_load_font_file(fallback))
                if loaded_families:
                    return loaded_families[-1]
        return "Segoe UI"

    def _install_exception_hook(self) -> None:
        def handle_exception(exc_type, exc_value, exc_traceback) -> None:
            LOGGER.exception("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))
            if os.getenv("SOFTIMOVEIS_SUPPRESS_ERROR_DIALOG") == "1":
                return
            QMessageBox.critical(
                None,
                "Não foi possível concluir a operação",
                "O erro foi registrado para diagnóstico. Nenhuma alteração foi salva.",
            )

        sys.excepthook = handle_exception


def _load_font_file(font_path: Path) -> list[str]:
    result = QFontDatabase.addApplicationFont(str(font_path))
    if result == -1:
        LOGGER.warning("Could not load font: %s", font_path)
        return []
    return list(QFontDatabase.applicationFontFamilies(result))


def run(argv: list[str] | None = None) -> int:
    app = SoftImoveisApplication(argv)
    return app.run()
