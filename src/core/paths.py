"""Path helpers that work in development and PyInstaller builds."""

from __future__ import annotations

import sys
from pathlib import Path


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def source_root() -> Path:
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS")) / "src"
    return Path(__file__).resolve().parents[1]


def project_root() -> Path:
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return source_root().parent


def asset_path(*parts: str) -> Path:
    return source_root() / "assets" / Path(*parts)


def logs_dir() -> Path:
    path = project_root() / "logs"
    path.mkdir(parents=True, exist_ok=True)
    return path

