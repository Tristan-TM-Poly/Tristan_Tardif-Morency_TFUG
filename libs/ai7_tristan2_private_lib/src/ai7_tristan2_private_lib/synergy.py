from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class SynergyLevel(str, Enum):
    LOCAL = "local"
    K_SYNERGY = "k_synergy"
    K_META_SYNERGY = "k_meta_synergy"


@dataclass
class ModuleSynergy:
    source_module: str
    target_module: str
    level: SynergyLevel
    description: str
    gain_score: float = 0.0


@dataclass
class KMetaSynergyReport:
    module_name: str
    synergies: List[ModuleSynergy] = field(default_factory=list)

    def total_gain(self) -> float:
        return sum(item.gain_score for item in self.synergies)
