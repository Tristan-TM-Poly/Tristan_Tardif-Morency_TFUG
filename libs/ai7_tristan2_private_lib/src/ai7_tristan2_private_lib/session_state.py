from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SessionState:
    session_id: str
    actor_id: str
    active_campaign: str = ""
    active_pilot: str = ""
    focus_modules: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)

    def set_campaign(self, campaign_name: str) -> None:
        self.active_campaign = campaign_name

    def set_pilot(self, pilot_name: str) -> None:
        self.active_pilot = pilot_name
