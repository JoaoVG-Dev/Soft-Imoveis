"""Initial domain model draft.

The model deliberately avoids undocumented financial rules. It preserves the
conceptual separation between charge, boleto, payment, settlement and transfer.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Landlord:
    code: str
    name: str
    document: str
    phone: str
    email: str
    property_count: int
    status: str


@dataclass(frozen=True)
class Tenant:
    code: str
    name: str
    document: str
    phone: str
    email: str
    contract: str
    status: str


@dataclass(frozen=True)
class Property:
    code: str
    address: str
    landlord: str
    current_tenant: str
    contract: str
    status: str


@dataclass(frozen=True)
class Contract:
    code: str
    property_ref: str
    landlord: str
    tenant: str
    start_date: date
    end_date: date
    base_value: Decimal
    status: str


@dataclass(frozen=True)
class Charge:
    code: str
    tenant: str
    property_ref: str
    competence: str
    due_date: date
    amount: Decimal
    boleto: str
    status: str


@dataclass(frozen=True)
class Boleto:
    id: str
    charge_code: str
    tenant: str
    property_ref: str
    issue_date: date | None
    due_date: date
    amount: Decimal
    status: str
    our_number: str | None = None
    digitable_line: str | None = None
    barcode: str | None = None
    bank: str | None = None
    wallet: str | None = None
    external_reference: str | None = None


@dataclass(frozen=True)
class Payment:
    code: str
    charge_code: str
    payer: str
    payment_date: date | None
    amount: Decimal
    status: str


@dataclass(frozen=True)
class Settlement:
    code: str
    payment_code: str
    settlement_date: date | None
    status: str
    notes: str = ""


@dataclass(frozen=True)
class BankAccount:
    code: str
    label: str
    bank_name: str | None
    agency: str | None
    account_number: str | None
    status: str


@dataclass(frozen=True)
class Transfer:
    code: str
    landlord: str
    contract: str
    reference: str
    due_date: date
    amount: Decimal
    status: str

