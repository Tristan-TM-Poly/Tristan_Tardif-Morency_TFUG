from __future__ import annotations

from .campaigns import bounded_raman_review_campaign, fractal_loop_closure_campaign
from .planner import CampaignPlan


def load_campaign(name: str) -> CampaignPlan:
    if name == "bounded-raman-review":
        return bounded_raman_review_campaign()
    if name == "fractal-loop-closure":
        return fractal_loop_closure_campaign()
    raise ValueError(f"Unknown campaign: {name}")


def main(argv: list[str] | None = None) -> int:
    argv = argv or []
    if len(argv) < 2 or argv[0] != "campaign":
        print("Usage: campaign <bounded-raman-review|fractal-loop-closure>")
        return 1

    plan = load_campaign(argv[1])
    for task in plan.to_tasks():
        print(f"{task.task_id}: {task.command} :: {task.payload}")
    return 0
