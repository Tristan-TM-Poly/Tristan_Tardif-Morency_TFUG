from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class CppLDKAdapter:
    library_name: str = "ldk_kernels_cpp"

    def call(self, kernel_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "backend": "cpp",
            "library": self.library_name,
            "kernel": kernel_name,
            "payload": payload,
            "status": "stub",
        }
