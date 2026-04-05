from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class LedgerAction(str, Enum):
    PROMOTE = "promote"
    DOWNGRADE = "downgrade"
    QUARANTINE = "quarantine"
    RESTORE = "restore"


@dataclass
class LedgerEntry:
    artifact_id: str
    action: LedgerAction
    from_state: str
    to_state: str
    reason: str


@dataclass
class PromotionDowngradeLedger:
    entries: List[LedgerEntry] = field(default_factory=list)

    def record(self, entry: LedgerEntry) -> None:
        self.entries.append(entry)
