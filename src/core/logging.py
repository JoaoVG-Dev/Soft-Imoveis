"""Logging setup for the desktop application."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from src.core.config import AppConfig
from src.core.paths import logs_dir


def setup_logging(config: AppConfig) -> None:
    level = getattr(logging, config.log_level, logging.INFO)
    log_file = logs_dir() / "softimoveis.log"

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)
    root.addHandler(file_handler)
    root.addHandler(console_handler)

