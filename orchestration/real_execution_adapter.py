from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


@dataclass
class ExecutionRecord:
    agent_id: str
    task_id: str
    command: str
    status: str
    executed_at_utc: str
    notes: str = ""


def execute_supervised(agent_id: str, tasks: Iterable[dict[str, Any]]) -> list[ExecutionRecord]:
    records: list[ExecutionRecord] = []
    for task in tasks:
        task_id = str(task.get("task_id", "unknown_task"))
        command = str(task.get("command", "noop"))
        records.append(
            ExecutionRecord(
                agent_id=agent_id,
                task_id=task_id,
                command=command,
                status="proposed_execution",
                executed_at_utc=datetime.now(timezone.utc).isoformat(),
                notes="Supervised mode only. Human or approved CI step required before real execution.",
            )
        )
    return records
