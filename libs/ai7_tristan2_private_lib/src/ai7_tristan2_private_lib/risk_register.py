from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskItem:
    risk_id: str
    title: str
    severity: RiskSeverity
    early_warning: str
    containment: str
    downgrade_trigger: str
