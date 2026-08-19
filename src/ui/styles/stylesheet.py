"""QSS stylesheet generated from centralized tokens."""

from __future__ import annotations

from src.ui.styles.tokens import Colors, Fonts


def build_stylesheet(font_family: str | None = None) -> str:
    c = Colors
    font = f'"{font_family or Fonts.FALLBACK}"'
    return f"""
* {{
    font-family: {font};
    color: {c.TEXT};
    font-size: {Fonts.BODY_SIZE}pt;
    outline: none;
}}

QMainWindow, QWidget#AppRoot {{
    background: {c.BACKGROUND};
}}

QWidget#TopHeader {{
    background: {c.BACKGROUND};
    border-bottom: 2px solid {c.TEXT};
}}

QLabel#BrandTitle {{
    font-size: 15pt;
    font-weight: 700;
    color: {c.TEXT};
}}

QLabel#BrandAccent {{
    font-size: 15pt;
    font-weight: 700;
    color: {c.ACCENT};
}}

QLabel#BrandSubline {{
    font-size: 6.8pt;
    font-weight: 500;
    letter-spacing: 3px;
    color: {c.NEUTRAL_600};
}}

QLabel#HeaderMeta, QLabel#MutedLabel, QLabel#HelperText {{
    color: {c.NEUTRAL_700};
}}

QFrame#Sidebar {{
    background: {c.SURFACE};
    border-right: 2px solid {c.TEXT};
}}

QLabel#SidebarGroup {{
    color: {c.NEUTRAL_700};
    font-size: {Fonts.KICKER_SIZE}pt;
    font-weight: 700;
    padding: 10px 12px 4px 14px;
    letter-spacing: 1px;
    border-top: 1px solid {c.NEUTRAL_300};
}}

QPushButton#NavButton {{
    background: transparent;
    border: 0;
    border-left: 4px solid transparent;
    padding: 6px 10px;
    text-align: left;
    font-weight: 500;
    min-height: 24px;
}}

QPushButton#NavButton:hover {{
    background: {c.ACCENT_LIGHT};
}}

QPushButton#NavButton[active="true"] {{
    background: {c.ACCENT_LIGHT};
    border-left: 4px solid {c.ACCENT};
    color: {c.ACCENT_TEXT};
    font-weight: 600;
}}

QWidget#Page {{
    background: {c.BACKGROUND};
}}

QLabel#PageTitle {{
    font-size: {Fonts.TITLE_SIZE}pt;
    font-weight: 800;
    color: {c.TEXT};
}}

QLabel#PageSubtitle {{
    color: {c.NEUTRAL_700};
}}

QFrame#SectionFrame {{
    background: {c.BACKGROUND};
    border: 2px solid {c.TEXT};
}}

QFrame#MetricBand {{
    background: {c.BACKGROUND};
    border: 2px solid {c.TEXT};
}}

QFrame#MetricCell {{
    background: {c.BACKGROUND};
    border: 0;
    border-right: 1px solid {c.NEUTRAL_300};
    border-bottom: 1px solid {c.NEUTRAL_300};
}}

QLabel#MetricLabel {{
    color: {c.NEUTRAL_700};
    font-size: {Fonts.KICKER_SIZE}pt;
    font-weight: 700;
    letter-spacing: 1px;
}}

QLabel#MetricValue {{
    font-size: {Fonts.METRIC_SIZE}pt;
    font-weight: 800;
    color: {c.TEXT};
}}

QLabel#MetricValue[tone="attention"] {{
    color: {c.ATTENTION_DARK};
}}

QLabel#MetricValue[tone="muted"] {{
    color: {c.NEUTRAL_700};
    font-size: 13pt;
}}

QLineEdit, QTextEdit, QComboBox {{
    background: {c.BACKGROUND};
    border: 2px solid {c.TEXT};
    padding: 9px 10px;
    min-height: 24px;
    selection-background-color: {c.ACCENT};
    selection-color: {c.BACKGROUND};
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 2px solid {c.ACCENT};
}}

QLineEdit:disabled, QTextEdit:disabled, QComboBox:disabled {{
    background: {c.NEUTRAL_200};
    color: {c.NEUTRAL_600};
}}

QPushButton {{
    border: 2px solid {c.TEXT};
    background: {c.BACKGROUND};
    padding: 8px 12px;
    font-weight: 600;
    min-height: 24px;
}}

QPushButton:hover {{
    background: {c.ACCENT_LIGHT};
}}

QPushButton:pressed {{
    background: {c.NEUTRAL_300};
}}

QPushButton:disabled {{
    background: {c.NEUTRAL_200};
    color: {c.NEUTRAL_600};
    border-color: {c.NEUTRAL_400};
}}

QPushButton#PrimaryButton {{
    background: {c.ACCENT};
    border-color: {c.ACCENT};
    color: {c.BACKGROUND};
}}

QPushButton#PrimaryButton:hover {{
    background: {c.ACCENT_HOVER};
    border-color: {c.ACCENT_HOVER};
}}

QPushButton#DangerButton {{
    color: {c.ATTENTION_DARK};
    border-color: {c.ATTENTION_DARK};
}}

QPushButton#ActionButton {{
    padding: 7px 10px;
    font-size: 9pt;
    font-weight: 600;
    border-color: {c.NEUTRAL_700};
}}

QPushButton#ActionButton:hover {{
    background: {c.ACCENT_LIGHT};
    color: {c.ACCENT_TEXT};
    border-color: {c.TEXT};
}}

QPushButton#PrimaryActionButton {{
    padding: 7px 12px;
    font-size: 9pt;
    font-weight: 700;
    background: {c.ACCENT};
    border-color: {c.ACCENT};
    color: {c.BACKGROUND};
}}

QPushButton#PrimaryActionButton:hover {{
    background: {c.ACCENT_HOVER};
    border-color: {c.ACCENT_HOVER};
}}

QPushButton#FilterChip {{
    padding: 5px 10px;
    border: 2px solid {c.TEXT};
    background: {c.BACKGROUND};
    font-weight: 700;
}}

QPushButton#FilterChip:checked {{
    background: {c.ACCENT};
    border-color: {c.ACCENT};
    color: {c.BACKGROUND};
}}

QTableView {{
    background: {c.BACKGROUND};
    gridline-color: transparent;
    border: 2px solid {c.TEXT};
    selection-background-color: {c.ACCENT_LIGHT};
    selection-color: {c.TEXT};
    alternate-background-color: {c.SURFACE};
}}

QHeaderView::section {{
    background: {c.BACKGROUND};
    border: 0;
    border-bottom: 2px solid {c.TEXT};
    padding: 8px 8px;
    font-weight: 800;
}}

QTableView::item {{
    padding: 7px 8px;
    border-bottom: 1px solid {c.NEUTRAL_300};
}}

QTableView::item:hover {{
    background: {c.ACCENT_LIGHT};
}}

QLabel#StatusBadge {{
    padding: 3px 7px;
    border: 1px solid {c.TEXT};
    font-weight: 700;
}}

QLabel#StatusBadge[tone="attention"] {{
    color: {c.ATTENTION_DARK};
    border-color: {c.ATTENTION_DARK};
}}

QLabel#StatusBadge[tone="ok"] {{
    color: {c.ACCENT_TEXT};
    border-color: {c.ACCENT};
}}

QLabel#EmptyTitle {{
    font-size: 14pt;
    font-weight: 800;
}}

QTabWidget::pane {{
    border: 2px solid {c.TEXT};
    top: -1px;
}}

QTabBar::tab {{
    background: {c.SURFACE};
    border: 1px solid {c.NEUTRAL_400};
    padding: 8px 13px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QTabBar::tab:selected {{
    background: {c.BACKGROUND};
    border-bottom: 2px solid {c.BACKGROUND};
    color: {c.ACCENT_TEXT};
}}

QStatusBar {{
    background: {c.SURFACE};
    border-top: 1px solid {c.NEUTRAL_300};
    color: {c.NEUTRAL_700};
}}

QScrollArea {{
    border: 0;
    background: {c.BACKGROUND};
}}

QScrollBar:vertical, QScrollBar:horizontal {{
    background: {c.SURFACE};
    border: 1px solid {c.NEUTRAL_300};
    width: 12px;
    height: 12px;
}}

QScrollBar::handle {{
    background: {c.NEUTRAL_500};
}}

QFrame#FormSection {{
    background: {c.BACKGROUND};
    border: 2px solid {c.TEXT};
}}

QLabel#SectionTitle {{
    font-size: 9pt;
    font-weight: 800;
    color: {c.ACCENT_TEXT};
    letter-spacing: 1px;
}}
"""
