from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RealityLevel(str, Enum):
    R0 = "document_only"
    R1 = "partially_structured"
    R2 = "prototype_executable"
    R3 = "bounded_runtime_active"
    R4 = "reviewed_runtime"
    R5 = "branch_feedback_active"
    R6 = "canon_facing_measured"


@dataclass
class RealityTag:
    object_name: str
    doctrine_level: RealityLevel
    machine_level: RealityLevel
    runtime_level: RealityLevel
    review_level: RealityLevel

    def weakest_link(self) -> RealityLevel:
        ordered = [
            RealityLevel.R0,
            RealityLevel.R1,
            RealityLevel.R2,
            RealityLevel.R3,
            RealityLevel.R4,
            RealityLevel.R5,
            RealityLevel.R6,
        ]
        levels = [self.doctrine_level, self.machine_level, self.runtime_level, self.review_level]
        return min(levels, key=lambda x: ordered.index(x))
