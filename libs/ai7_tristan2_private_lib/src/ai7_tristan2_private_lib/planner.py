from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .task_queue import TaskItem


@dataclass
class PlanStep:
    name: str
    description: str
    command: str


@dataclass
class CampaignPlan:
    campaign_name: str
    steps: List[PlanStep] = field(default_factory=list)

    def to_tasks(self) -> List[TaskItem]:
        tasks = []
        for idx, step in enumerate(self.steps):
            tasks.append(
                TaskItem(
                    task_id=f"{self.campaign_name}-{idx+1}",
                    command=step.command,
                    payload={"name": step.name, "description": step.description},
                    priority=max(1, len(self.steps) - idx),
                )
            )
        return tasks
