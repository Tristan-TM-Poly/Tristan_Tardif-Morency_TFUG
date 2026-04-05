from __future__ import annotations

from dataclasses import dataclass

from .parallel_governance import AutonomousGovernanceDecision, GovernanceMode, ParallelGroup


@dataclass
class AutonomyGovernor:
    require_review_for_parallel: bool = True
    require_nonempty_tasks: bool = True

    def evaluate_group(self, group: ParallelGroup) -> AutonomousGovernanceDecision:
        if self.require_nonempty_tasks and not group.tasks:
            return AutonomousGovernanceDecision(
                group_id=group.group_id,
                approved=False,
                reason="empty task group",
                next_mode=GovernanceMode.QUARANTINE,
            )
        if self.require_review_for_parallel and group.governance_mode == GovernanceMode.COUPLED_PARALLEL and group.dependencies:
            return AutonomousGovernanceDecision(
                group_id=group.group_id,
                approved=False,
                reason="parallel group has unresolved dependencies",
                next_mode=GovernanceMode.SAFE_SEQUENTIAL,
            )
        return AutonomousGovernanceDecision(
            group_id=group.group_id,
            approved=True,
            reason="group approved",
            next_mode=group.governance_mode,
        )
