from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .registry import BranchStatus


class MaturityGate(str, Enum):
    G1 = "foundation"
    G2 = "self_governance_active"
    G3 = "pilot_feedback_to_canon"
    G4 = "measured_partial_autonomy"


@dataclass(frozen=True)
class GovernanceDecision:
    artifact_id: str
    target_status: BranchStatus
    reason: str
    maturity_gate: MaturityGate


def evaluate_promotion(score_total: float) -> BranchStatus:
    if score_total >= 8.0:
        return BranchStatus.STABLE
    if score_total >= 5.0:
        return BranchStatus.CRYSTALLIZABLE
    if score_total >= 2.0:
        return BranchStatus.EXPLORATORY
    return BranchStatus.QUARANTINE
