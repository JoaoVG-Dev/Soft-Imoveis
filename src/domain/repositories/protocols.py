"""Repository interfaces for future persistence implementations."""

from __future__ import annotations

from typing import Protocol, TypeVar

from src.domain.entities import (
    BankAccount,
    Boleto,
    Charge,
    Contract,
    Landlord,
    Payment,
    Property,
    Settlement,
    Tenant,
    Transfer,
)

T = TypeVar("T")


class ListRepository(Protocol[T]):
    def list(self) -> list[T]:
        ...

    def get(self, key: str) -> T | None:
        ...

    def search(self, query: str) -> list[T]:
        ...


class LandlordRepository(ListRepository[Landlord], Protocol):
    pass


class TenantRepository(ListRepository[Tenant], Protocol):
    pass


class PropertyRepository(ListRepository[Property], Protocol):
    pass


class ContractRepository(ListRepository[Contract], Protocol):
    pass


class ChargeRepository(ListRepository[Charge], Protocol):
    pass


class BoletoRepository(ListRepository[Boleto], Protocol):
    pass


class PaymentRepository(ListRepository[Payment], Protocol):
    pass


class SettlementRepository(ListRepository[Settlement], Protocol):
    pass


class BankAccountRepository(ListRepository[BankAccount], Protocol):
    pass


class TransferRepository(ListRepository[Transfer], Protocol):
    pass

