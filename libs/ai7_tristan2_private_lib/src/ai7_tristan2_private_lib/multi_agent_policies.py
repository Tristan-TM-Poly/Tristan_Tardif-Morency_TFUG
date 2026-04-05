from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AgentPolicy:
    actor_id: str
    max_parallel_groups: int = 4
    can_promote: bool = False
    can_quarantine: bool = True
    can_attach_drive: bool = True


@dataclass
class MultiAgentPolicies:
    policies: Dict[str, AgentPolicy]

    def get(self, actor_id: str) -> AgentPolicy | None:
        return self.policies.get(actor_id)
