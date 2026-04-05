from __future__ import annotations

from .planner import CampaignPlan, PlanStep


def bounded_raman_review_campaign() -> CampaignPlan:
    return CampaignPlan(
        campaign_name="bounded-raman-review",
        steps=[
            PlanStep("identify-source", "clarify source of truth for pilot inputs", "source.identify"),
            PlanStep("attach-drive", "attach Drive documents to artifact records", "drive.attach"),
            PlanStep("score-artifact", "compute first score row", "score.compute"),
            PlanStep("review-pilot", "perform bounded review and closure decision", "review.close"),
        ],
    )


def fractal_loop_closure_campaign() -> CampaignPlan:
    return CampaignPlan(
        campaign_name="fractal-loop-closure",
        steps=[
            PlanStep("packet-family", "generate packet family skeleton", "packet.generate"),
            PlanStep("synergy-row", "compute synergy row", "synergy.compute"),
            PlanStep("reality-tag", "tag reality levels", "reality.tag"),
            PlanStep("promote-or-quarantine", "make governance decision", "governance.decide"),
        ],
    )
