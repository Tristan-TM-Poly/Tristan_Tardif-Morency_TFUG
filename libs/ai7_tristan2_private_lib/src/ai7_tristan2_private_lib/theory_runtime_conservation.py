from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TheoryRuntimeConservation:
    object_name: str
    implementation_depth: float
    theory_amplitude: float

    def conservation_ratio(self) -> float:
        if self.theory_amplitude <= 0:
            return 0.0
        return self.implementation_depth / self.theory_amplitude

    def interpretation(self) -> str:
        ratio = self.conservation_ratio()
        if ratio >= 0.85:
            return "strong conservation"
        if ratio >= 0.60:
            return "usable pilot conservation"
        if ratio >= 0.35:
            return "inflation risk"
        return "severe theory-runtime divergence"
