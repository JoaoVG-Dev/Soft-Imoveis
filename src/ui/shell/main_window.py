"""Main application window."""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.app.state import AppState
from src.application.services import DEFAULT_ROUTE, NAVIGATION, DemoDataStore
from src.core.config import AppConfig
from src.core.constants import APP_TITLE, DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH
from src.core.paths import asset_path
from src.ui.pages import DashboardPage, RecordsPage, ReportsPage, SettingsPage
from src.ui.shell.sidebar import Sidebar
from src.ui.styles.tokens import Colors

LOGGER = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig, state: AppState, data_store: DemoDataStore) -> None:
        super().__init__()
        self.config = config
        self.state = state
        self.data_store = data_store
        self._pages: dict[str, QWidget] = {}

        self.setWindowTitle(APP_TITLE)
        self.setWindowIcon(QIcon(str(asset_path("icons", "softimoveis.svg"))))
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(1180, 690)

        root = QWidget()
        root.setObjectName("AppRoot")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._header())

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        self.sidebar = Sidebar()
        self.sidebar.navigate_requested.connect(self.navigate)
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)
        root_layout.addLayout(body, 1)

        self.setCentralWidget(root)
        self._build_pages()
        self.statusBar().showMessage(
            f"Soft-Imóveis | {config.environment} | v{config.app_version} | Dados demonstrativos"
        )
        self.navigate(DEFAULT_ROUTE)

    def navigate(self, key: str) -> None:
        if key not in self._pages:
            LOGGER.warning("Attempted navigation to unknown route: %s", key)
            return
        self.stack.setCurrentWidget(self._pages[key])
        self.sidebar.set_active(key)
        self.state.current_route = key
        LOGGER.info("Navigation: %s", key)

    def smoke_navigation(self) -> tuple[str, ...]:
        visited: list[str] = []
        for item in NAVIGATION:
            self.navigate(item.key)
            visited.append(item.key)
        return tuple(visited)

    def _build_pages(self) -> None:
        self._add_page("dashboard", DashboardPage(self.data_store))
        for key in (
            "landlords",
            "tenants",
            "properties",
            "contracts",
            "charges",
            "boletos",
            "delinquency",
            "finance",
            "transfers",
        ):
            self._add_page(key, RecordsPage(self.data_store.page(key), self.data_store))
        self._add_page("reports", ReportsPage())
        self._add_page("settings", SettingsPage(self.config))

    def _add_page(self, key: str, page: QWidget) -> None:
        self._pages[key] = page
        self.stack.addWidget(page)

    def _header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("TopHeader")
        header.setFixedHeight(62)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(12)

        layout.addWidget(BrandLockup())

        descriptor = QLabel("Gestão Imobiliária")
        descriptor.setObjectName("HeaderMeta")
        layout.addWidget(descriptor)
        layout.addStretch(1)

        user = QLabel(self.state.session.user_name)
        user.setObjectName("HeaderMeta")
        user.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(user)
        return header


class BrandLockup(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addWidget(SkylineMark())

        text = QWidget()
        text_layout = QVBoxLayout(text)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)

        word = QWidget()
        word_layout = QHBoxLayout(word)
        word_layout.setContentsMargins(0, 0, 0, 0)
        word_layout.setSpacing(0)
        soft = QLabel("soft")
        soft.setObjectName("BrandTitle")
        imoveis = QLabel("imóveis")
        imoveis.setObjectName("BrandAccent")
        word_layout.addWidget(soft)
        word_layout.addWidget(imoveis)

        subline = QLabel("INFORMÁTICA")
        subline.setObjectName("BrandSubline")
        text_layout.addWidget(word)
        text_layout.addWidget(subline)
        layout.addWidget(text)


class SkylineMark(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(40, 40)

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(Colors.ACCENT))
        painter.drawEllipse(0, 0, 40, 40)

        bars = ((11, 19, 4, 10, Colors.BACKGROUND), (17, 13, 4, 16, Colors.BACKGROUND), (23, 22, 4, 7, Colors.ATTENTION), (29, 16, 4, 13, Colors.BACKGROUND))
        for x, y, width, height, color in bars:
            painter.setBrush(QColor(color))
            painter.drawRect(x, y, width, height)
