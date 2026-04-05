from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .task_queue import TaskItem


class GovernanceMode(str, Enum):
    COUPLED_PARALLEL = "coupled_parallel"
    SAFE_SEQUENTIAL = "safe_sequential"
    QUARANTINE = "quarantine"


@dataclass
class ParallelGroup:
    group_id: str
    tasks: List[TaskItem] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    governance_mode: GovernanceMode = GovernanceMode.COUPLED_PARALLEL

    def add_task(self, task: TaskItem) -> None:
        self.tasks.append(task)


@dataclass
class AutonomousGovernanceDecision:
    group_id: str
    approved: bool
    reason: str
    next_mode: GovernanceMode
