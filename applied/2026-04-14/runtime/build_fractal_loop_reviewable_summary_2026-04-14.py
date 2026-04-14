from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/fractal_loop_trace_artifact_2026-04-14.json"
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/fractal_loop_reviewable_summary_2026-04-14.md"


def build_summary() -> str:
    payload = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    result = payload["result"]
    trace = result.get("trace", [])
    bounded = result.get("bounded", False)
    stop_reason = result.get("stop_reason", "unknown")

    lines = [
        "# FRACTAL_LOOP_REVIEWABLE_SUMMARY — Generated Snapshot (2026-04-14)",
        "",
        f"- artifact_type: {payload.get('artifact_type', 'unknown')}",
        f"- source: {payload.get('source', 'unknown')}",
        f"- trace_length: {len(trace)}",
        f"- bounded: {bounded}",
        f"- stop_reason: {stop_reason}",
        "",
        "## Interpretation",
        "This generated summary exists to make the emitted trace readable by review-facing layers without changing the underlying bounded object.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_summary())
