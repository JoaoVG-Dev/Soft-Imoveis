"""Settings page."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QGridLayout, QScrollArea, QTabWidget, QVBoxLayout, QWidget

from src.core.config import AppConfig
from src.ui.widgets import FormField, PageHeader


class SettingsPage(QWidget):
    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self.setObjectName("Page")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        layout.addWidget(
            PageHeader(
                "Configurações",
                "Pontos de extensão para aplicação, usuários, empresa, cobranças, integrações, banco de dados e logs.",
            )
        )

        tabs = QTabWidget()
        tabs.addTab(_application_tab(config), "APLICAÇÃO")
        tabs.addTab(_placeholder_tab("Usuários", "Login, sessão, role e permissões serão definidos após descoberta."), "USUÁRIOS")
        tabs.addTab(_placeholder_tab("Empresa", "Dados oficiais da empresa não foram carregados nesta fase."), "EMPRESA")
        tabs.addTab(_placeholder_tab("Cobranças", "Multa, juros, correção e baixas aguardam regra documentada."), "COBRANÇAS")
        tabs.addTab(_placeholder_tab("Integrações", "Banco, CNAB, remessa, retorno e API externa ainda não configurados."), "INTEGRAÇÕES")
        tabs.addTab(_placeholder_tab("Banco de Dados", "Persistência definitiva não foi implementada nesta etapa."), "BANCO DE DADOS")
        tabs.addTab(_placeholder_tab("Logs", "Logs locais são gravados em desenvolvimento sem dados sensíveis."), "LOGS")
        tabs.addTab(_placeholder_tab("Sobre", "Soft-Imóveis 0.2.0 - refinamento visual da fundação desktop."), "SOBRE")
        layout.addWidget(tabs, 1)


def _application_tab(config: AppConfig) -> QWidget:
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.setContentsMargins(14, 14, 14, 14)
    layout.setSpacing(12)

    grid_container = QWidget()
    grid = QGridLayout(grid_container)
    grid.setContentsMargins(14, 14, 14, 14)
    grid.setHorizontalSpacing(14)
    grid.setVerticalSpacing(12)
    fields = (
        FormField("Ambiente", config.environment, read_only=True),
        FormField("Nome da aplicação", config.app_name, read_only=True),
        FormField("Versão", config.app_version, read_only=True),
        FormField("API URL", config.api_url or "Não configurada", "Preparado para API futura.", read_only=True),
        FormField("Nível de log", config.log_level, read_only=True),
    )
    for index, field in enumerate(fields):
        grid.addWidget(field, index // 2, index % 2)
    grid.setColumnStretch(0, 1)
    grid.setColumnStretch(1, 1)
    layout.addWidget(grid_container)
    layout.addStretch(1)
    return tab


def _placeholder_tab(title: str, message: str) -> QWidget:
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setContentsMargins(16, 16, 16, 16)
    layout.setSpacing(8)
    heading = QLabel(title.upper())
    heading.setObjectName("PageTitle")
    label = QLabel(message)
    label.setObjectName("PageSubtitle")
    label.setWordWrap(True)
    layout.addWidget(heading)
    layout.addWidget(label)
    layout.addStretch(1)
    scroll.setWidget(content)
    return scroll
