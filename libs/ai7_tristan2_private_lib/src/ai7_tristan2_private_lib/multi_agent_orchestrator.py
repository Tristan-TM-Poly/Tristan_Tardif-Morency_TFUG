from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .actors import ActorProfile, is_actor_allowed
from .parallel_governance import ParallelGroup
from .task_queue import TaskQueue


@dataclass
class MultiAgentOrchestrator:
    actors: Dict[str, ActorProfile] = field(default_factory=dict)
    queue: TaskQueue = field(default_factory=TaskQueue)
    groups: Dict[str, ParallelGroup] = field(default_factory=dict)

    def register_actor(self, actor: ActorProfile) -> bool:
        if not is_actor_allowed(actor):
            return False
        self.actors[actor.actor_id] = actor
        return True

    def register_group(self, group: ParallelGroup) -> None:
        self.groups[group.group_id] = group
        for task in group.tasks:
            self.queue.enqueue(task)

    def actor_ids(self) -> List[str]:
        return sorted(self.actors.keys())

    def group_ids(self) -> List[str]:
        return sorted(self.groups.keys())
