from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .planner import CampaignPlan
from .task_queue import TaskQueue


@dataclass
class CampaignRunner:
    queue: TaskQueue = field(default_factory=TaskQueue)

    def load_plan(self, plan: CampaignPlan) -> None:
        for task in plan.to_tasks():
            self.queue.enqueue(task)

    def pending_commands(self) -> List[str]:
        return [task.command for task in self.queue.tasks if task.status.value == "pending"]
