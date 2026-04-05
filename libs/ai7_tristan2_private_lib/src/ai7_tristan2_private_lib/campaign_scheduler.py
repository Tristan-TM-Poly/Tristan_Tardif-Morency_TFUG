from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .campaign_runner import CampaignRunner
from .planner import CampaignPlan


@dataclass
class CampaignScheduler:
    runners: Dict[str, CampaignRunner] = field(default_factory=dict)

    def add_plan(self, plan: CampaignPlan) -> None:
        runner = CampaignRunner()
        runner.load_plan(plan)
        self.runners[plan.campaign_name] = runner

    def pending_by_campaign(self) -> Dict[str, List[str]]:
        return {name: runner.pending_commands() for name, runner in self.runners.items()}

    def names(self) -> List[str]:
        return sorted(self.runners.keys())
