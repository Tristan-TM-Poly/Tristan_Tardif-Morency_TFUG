from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    BLOCKED = "blocked"
    DONE = "done"
    QUARANTINED = "quarantined"


@dataclass
class TaskItem:
    task_id: str
    command: str
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class TaskQueue:
    tasks: List[TaskItem] = field(default_factory=list)

    def enqueue(self, task: TaskItem) -> None:
        self.tasks.append(task)
        self.tasks.sort(key=lambda t: t.priority, reverse=True)

    def next_task(self) -> TaskItem | None:
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None
