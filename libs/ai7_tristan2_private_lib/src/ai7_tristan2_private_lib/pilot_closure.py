from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class PilotStatus(str, Enum):
    DESIGNED = "designed"
    RUNNING = "running"
    REVIEW_REQUIRED = "review_required"
    CLOSED = "closed"
    QUARANTINED = "quarantined"


@dataclass
class PilotClosureRecord:
    pilot_id: str
    title: str
    status: PilotStatus
    success_criteria: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    closure_notes: str = ""

    def add_blocker(self, blocker: str) -> None:
        self.blockers.append(blocker)
