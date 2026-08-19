"""Minimal application state."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SessionState:
    user_name: str = "Usuário desenvolvimento"
    company_name: str = "Soft-Imóveis"
    permissions: tuple[str, ...] = ("visualizar", "cadastrar", "editar", "emitir_boleto")


@dataclass
class AppState:
    session: SessionState
    current_route: str = "dashboard"

