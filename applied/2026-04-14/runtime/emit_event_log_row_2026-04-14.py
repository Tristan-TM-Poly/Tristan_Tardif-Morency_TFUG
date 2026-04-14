from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/event_log_row_generated_2026-04-14.json"


def build_event_row() -> dict:
    row = {
        "event_type": "promotion_decision_checked",
        "object_name": "Fractal-Loop first bounded pilot",
        "artifact_pointer": "runtime/artifacts/fractal_loop_reviewable_summary_2026-04-14.md",
        "verdict": "keep_bounded",
        "review_pointer": "review/REVIEW_SUMMARY_2026-04-14.md",
        "promotion_pointer": "governance/PROMOTION_DECISION_ROW_2026-04-14.md",
        "owner": "governance",
        "timestamp_placeholder": "2026-04-14T00:00:00Z",
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(row, indent=2), encoding="utf-8")
    return row


if __name__ == "__main__":
    print(json.dumps(build_event_row(), indent=2))
