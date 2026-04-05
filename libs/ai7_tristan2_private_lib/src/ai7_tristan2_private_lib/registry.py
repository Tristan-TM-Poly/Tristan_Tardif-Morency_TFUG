from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class BranchStatus(str, Enum):
    STABLE = "stable"
    CRYSTALLIZABLE = "crystallizable"
    EXPLORATORY = "exploratory"
    QUARANTINE = "quarantine"


@dataclass
class ArtifactRecord:
    artifact_id: str
    title: str
    owner: str
    source_of_truth: str
    branch_status: BranchStatus
    tags: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class RegistryState:
    artifacts: Dict[str, ArtifactRecord] = field(default_factory=dict)

    def register(self, artifact: ArtifactRecord) -> None:
        self.artifacts[artifact.artifact_id] = artifact

    def get(self, artifact_id: str) -> ArtifactRecord | None:
        return self.artifacts.get(artifact_id)
