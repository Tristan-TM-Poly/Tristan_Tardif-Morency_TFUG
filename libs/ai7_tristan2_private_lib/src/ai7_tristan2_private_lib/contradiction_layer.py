from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ContradictionStatus(str, Enum):
    OPEN = "open"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    DOWNGRADE_REQUIRED = "downgrade_required"


@dataclass
class ContradictionRecord:
    contradiction_id: str
    artifact_id: str
    hypothesis: str
    observed_conflict: str
    status: ContradictionStatus = ContradictionStatus.OPEN
    actions: List[str] = field(default_factory=list)

    def add_action(self, action: str) -> None:
        self.actions.append(action)
