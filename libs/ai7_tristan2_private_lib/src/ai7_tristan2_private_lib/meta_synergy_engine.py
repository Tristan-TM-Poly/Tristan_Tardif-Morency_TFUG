from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .synergy import KMetaSynergyReport, ModuleSynergy, SynergyLevel


@dataclass
class MetaSynergyEngine:
    reports: Dict[str, KMetaSynergyReport] = field(default_factory=dict)

    def register_synergy(
        self,
        module_name: str,
        source_module: str,
        target_module: str,
        description: str,
        gain_score: float,
        level: SynergyLevel = SynergyLevel.K_META_SYNERGY,
    ) -> None:
        report = self.reports.setdefault(module_name, KMetaSynergyReport(module_name=module_name))
        report.synergies.append(
            ModuleSynergy(
                source_module=source_module,
                target_module=target_module,
                level=level,
                description=description,
                gain_score=gain_score,
            )
        )

    def total_gain(self, module_name: str) -> float:
        report = self.reports.get(module_name)
        if report is None:
            return 0.0
        return report.total_gain()

    def ranked_modules(self) -> List[str]:
        return sorted(self.reports.keys(), key=lambda name: self.total_gain(name), reverse=True)
