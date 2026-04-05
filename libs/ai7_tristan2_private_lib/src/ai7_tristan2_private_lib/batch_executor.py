from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .parallel_governance import ParallelGroup
from .task_queue import TaskStatus


@dataclass
class BatchExecutionReport:
    batch_id: str
    executed_tasks: List[str] = field(default_factory=list)
    blocked_tasks: List[str] = field(default_factory=list)


def execute_parallel_group(group: ParallelGroup) -> BatchExecutionReport:
    report = BatchExecutionReport(batch_id=group.group_id)
    for task in group.tasks:
        if group.dependencies:
            task.status = TaskStatus.BLOCKED
            report.blocked_tasks.append(task.task_id)
        else:
            task.status = TaskStatus.DONE
            report.executed_tasks.append(task.task_id)
    return report
