"""Centralized runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from src.core.constants import APP_NAME, APP_VERSION


@dataclass(frozen=True)
class AppConfig:
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    environment: str = "development"
    api_url: str = ""
    log_level: str = "INFO"


def load_config() -> AppConfig:
    """Load configuration from environment variables.

    Secrets are intentionally not loaded from source files. Future builds can
    add a .env loader if the deployment process calls for it.
    """

    return AppConfig(
        environment=os.getenv("SOFTIMOVEIS_ENV", "development"),
        api_url=os.getenv("SOFTIMOVEIS_API_URL", ""),
        log_level=os.getenv("SOFTIMOVEIS_LOG_LEVEL", "INFO").upper(),
    )

