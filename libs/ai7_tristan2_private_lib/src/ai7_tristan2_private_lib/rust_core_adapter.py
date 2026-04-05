from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class RustCoreAdapter:
    library_name: str = "ai7_core_rs"

    def call(self, function_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "backend": "rust",
            "library": self.library_name,
            "function": function_name,
            "payload": payload,
            "status": "stub",
        }
