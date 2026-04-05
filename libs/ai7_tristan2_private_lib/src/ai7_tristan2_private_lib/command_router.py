from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class CommandResult:
    ok: bool
    message: str
    data: Dict[str, Any] | None = None


class CommandRouter:
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[[Dict[str, Any]], CommandResult]] = {}

    def register(self, command_name: str, handler: Callable[[Dict[str, Any]], CommandResult]) -> None:
        self._handlers[command_name] = handler

    def dispatch(self, command_name: str, payload: Dict[str, Any]) -> CommandResult:
        handler = self._handlers.get(command_name)
        if handler is None:
            return CommandResult(ok=False, message=f"Unknown command: {command_name}", data={"payload": payload})
        return handler(payload)
