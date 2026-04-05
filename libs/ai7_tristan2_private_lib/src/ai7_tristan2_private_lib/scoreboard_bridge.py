from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class ScoreboardPointer:
    spreadsheet_id: str
    sheet_name: str
    description: str = ""


@dataclass
class ScoreRow:
    artifact_id: str
    score_total: float
    branch_status: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "score_total": self.score_total,
            "branch_status": self.branch_status,
            "metadata": self.metadata,
        }
