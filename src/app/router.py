"""Small route registry used by the shell and tests."""

from __future__ import annotations

from collections.abc import Callable


class Router:
    def __init__(self, default_route: str) -> None:
        self._routes: dict[str, Callable[[], object]] = {}
        self.current_route = default_route

    def register(self, key: str, factory: Callable[[], object]) -> None:
        self._routes[key] = factory

    def keys(self) -> tuple[str, ...]:
        return tuple(self._routes.keys())

    def resolve(self, key: str) -> object:
        if key not in self._routes:
            raise KeyError(f"Unknown route: {key}")
        self.current_route = key
        return self._routes[key]()

