"""Banking integration extension points."""

from __future__ import annotations

from typing import Protocol

from src.domain.entities import Boleto, Charge


class BankingProvider(Protocol):
    provider_name: str


class BoletoIssuer(Protocol):
    def issue(self, charge: Charge) -> Boleto:
        ...


class RemittanceService(Protocol):
    def generate_remittance(self, boletos: list[Boleto]) -> bytes:
        ...


class ReturnFileService(Protocol):
    def import_return_file(self, content: bytes) -> list[str]:
        ...

