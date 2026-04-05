from __future__ import annotations

from dataclasses import dataclass

from .task_queue import TaskItem


@dataclass(frozen=True)
class PriorityWeights:
    urgency: float = 1.0
    synergy_gain: float = 1.5
    canon_impact: float = 1.3
    risk_penalty: float = 1.2


def compute_priority(
    base_priority: int,
    synergy_gain: float,
    canon_impact: float,
    risk_penalty: float,
    weights: PriorityWeights | None = None,
) -> float:
    weights = weights or PriorityWeights()
    return (
        base_priority * weights.urgency
        + synergy_gain * weights.synergy_gain
        + canon_impact * weights.canon_impact
        - risk_penalty * weights.risk_penalty
    )


def reprioritize_task(
    task: TaskItem,
    synergy_gain: float,
    canon_impact: float,
    risk_penalty: float,
    weights: PriorityWeights | None = None,
) -> TaskItem:
    task.priority = int(compute_priority(task.priority, synergy_gain, canon_impact, risk_penalty, weights))
    return task
