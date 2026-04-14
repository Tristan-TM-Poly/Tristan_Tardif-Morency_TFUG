from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/automation_bundle_report_resilient_2026-04-14.json"
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/auto_improvement_queue_generated_2026-04-14.md"


def build_queue() -> str:
    payload = json.loads(REPORT_PATH.read_text(encoding="utf-8")) if REPORT_PATH.exists() else {"results": []}
    failed = [r["script"] for r in payload.get("results", []) if not r.get("ok", False)]
    lines = [
        "# AUTO_IMPROVEMENT_QUEUE — Generated Snapshot (2026-04-14)",
        "",
        "## Priority rules",
        "1. Fix failing automation scripts first.",
        "2. Tighten the deepest frontier before widening breadth.",
        "3. Prefer improvements that increase reviewability and artifact legibility.",
        "",
        "## Current queue",
    ]
    if failed:
        lines.extend(f"- repair: {name}" for name in failed)
    else:
        lines += [
            "- improve: attach stronger Raman dataset-family instance",
            "- improve: strengthen bounded LDK executable evidence",
            "- improve: connect generated outputs to a more unified frontier digest",
        ]
    lines += [
        "",
        "## Law",
        "The improvement queue is generated so the system can prioritize its own next repairs and upgrades from automation evidence instead of intuition alone.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_queue())
