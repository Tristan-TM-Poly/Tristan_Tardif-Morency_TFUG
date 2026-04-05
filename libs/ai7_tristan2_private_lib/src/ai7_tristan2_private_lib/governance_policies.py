from __future__ import annotations

from dataclasses import dataclass

from .parallel_governance import GovernanceMode, ParallelGroup


@dataclass(frozen=True)
class GovernancePolicy:
    name: str
    allow_parallel: bool = True
    allow_quarantine: bool = True
    require_dependency_clearance: bool = True

    def recommend_mode(self, group: ParallelGroup) -> GovernanceMode:
        if self.require_dependency_clearance and group.dependencies:
            return GovernanceMode.SAFE_SEQUENTIAL
        if self.allow_parallel:
            return GovernanceMode.COUPLED_PARALLEL
        if self.allow_quarantine:
            return GovernanceMode.QUARANTINE
        return GovernanceMode.SAFE_SEQUENTIAL
