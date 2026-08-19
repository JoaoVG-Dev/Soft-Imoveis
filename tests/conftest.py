from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("SOFTIMOVEIS_SUPPRESS_ERROR_DIALOG", "1")


def pytest_configure() -> None:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

