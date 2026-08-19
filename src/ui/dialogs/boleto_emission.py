"""Mock boleto emission dialog."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.formatters import format_brl
from src.domain.services import ChargeCalculationInput, DemoChargeCalculationService
from src.ui.widgets import FormField


class BoletoEmissionDialog(QDialog):
    def __init__(self, source_row: dict[str, object], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Emissão de boleto - demonstração")
        self.resize(900, 720)
        self._calculator = DemoChargeCalculationService()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("EMISSÃO DE BOLETO")
        title.setObjectName("PageTitle")
        subtitle = QLabel(
            "DEMO DATA: interface operacional sem integração bancária, CNAB, carteira, convênio ou fórmula financeira real."
        )
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        self.tenant = FormField("Locatário", _display_value(source_row.get("locatario", source_row.get("tenant", ""))), read_only=True)
        self.property_ref = FormField("Imóvel", _display_value(source_row.get("imovel", source_row.get("property_ref", ""))), read_only=True)
        self.landlord = FormField("Locador", _display_value(source_row.get("locador", "")), "A confirmar pelo vínculo real.", read_only=True)
        self.competence = FormField("Competência", _display_value(source_row.get("competencia", "")))
        self.issue_date = FormField("Data de emissão", "18/08/2026")
        self.due_date = FormField("Data de vencimento", str(source_row.get("vencimento", "")))
        self.base_value = FormField("Valor base", str(source_row.get("valor", "R$ 0,00")))
        self.fine = FormField("Multa", "R$ 0,00", "Sem fórmula real configurada.")
        self.interest = FormField("Juros", "R$ 0,00", "Sem fórmula real configurada.")
        self.correction = FormField("Correção", "R$ 0,00", "Sem índice real configurado.")
        self.other_items = FormField("Outros lançamentos", "R$ 0,00")
        self.total = FormField("Valor total", "R$ 0,00", read_only=True)

        content_layout.addWidget(
            _section("IDENTIFICAÇÃO", (self.tenant, self.property_ref, self.landlord), columns=3)
        )
        content_layout.addWidget(
            _section("COMPETÊNCIA E DATAS", (self.competence, self.issue_date, self.due_date), columns=3)
        )
        content_layout.addWidget(
            _section(
                "VALORES E ENCARGOS",
                (self.base_value, self.other_items, self.fine, self.interest, self.correction, self.total),
                columns=3,
            )
        )

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        buttons = QDialogButtonBox()
        calculate = buttons.addButton("Recalcular", QDialogButtonBox.ButtonRole.ActionRole)
        calculate.setObjectName("ActionButton")
        calculate.clicked.connect(self._recalculate)
        self.emit_button = buttons.addButton("Registrar mock", QDialogButtonBox.ButtonRole.AcceptRole)
        self.emit_button.setObjectName("PrimaryButton")
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self._accept_mock)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._recalculate()

    def _recalculate(self) -> None:
        result = self._calculator.calculate(
            ChargeCalculationInput(
                base_value=_parse_brl(self.base_value.text()),
                fine=_parse_brl(self.fine.text()),
                interest=_parse_brl(self.interest.text()),
                correction=_parse_brl(self.correction.text()),
                other_items=_parse_brl(self.other_items.text()),
            )
        )
        self.total.set_text(format_brl(result.total))

    def _accept_mock(self) -> None:
        QMessageBox.information(
            self,
            "Boleto não emitido",
            "Registro mock concluído. Nenhuma integração bancária real foi executada.",
        )
        self.accept()


def _parse_brl(value: str) -> Decimal:
    clean = value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return Decimal(clean or "0")
    except InvalidOperation:
        return Decimal("0.00")


def _display_value(value: object) -> str:
    text = str(value).strip()
    return text if text else "A confirmar"


def _section(title: str, fields: tuple[FormField, ...], columns: int) -> QFrame:
    section = QFrame()
    section.setObjectName("FormSection")
    section.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    layout = QVBoxLayout(section)
    layout.setContentsMargins(14, 10, 14, 12)
    layout.setSpacing(8)

    title_label = QLabel(title)
    title_label.setObjectName("SectionTitle")
    layout.addWidget(title_label)

    grid = QGridLayout()
    grid.setHorizontalSpacing(12)
    grid.setVerticalSpacing(8)
    for index, field in enumerate(fields):
        grid.addWidget(field, index // columns, index % columns)
    for column in range(columns):
        grid.setColumnStretch(column, 1)
    layout.addLayout(grid)
    return section
