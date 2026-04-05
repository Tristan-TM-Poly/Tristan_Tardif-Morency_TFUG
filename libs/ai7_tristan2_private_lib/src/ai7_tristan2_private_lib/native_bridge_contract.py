from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class NativeBackend(str, Enum):
    RUST = "rust"
    CPP = "cpp"
    GO = "go"
    TYPESCRIPT = "typescript"
    PYTHON = "python"


@dataclass(frozen=True)
class NativeFunctionContract:
    function_name: str
    backend: NativeBackend
    input_schema: Dict[str, str]
    output_schema: Dict[str, str]
    invariants: List[str] = field(default_factory=list)
    benchmark_target: str = ""


@dataclass
class NativeBridgeRegistry:
    contracts: Dict[str, NativeFunctionContract] = field(default_factory=dict)

    def register(self, contract: NativeFunctionContract) -> None:
        self.contracts[contract.function_name] = contract

    def get(self, function_name: str) -> NativeFunctionContract | None:
        return self.contracts.get(function_name)
