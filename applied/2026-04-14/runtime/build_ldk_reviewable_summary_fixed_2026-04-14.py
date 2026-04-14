from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/ldk_bounded_artifact_fixed_2026-04-14.json"
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/ldk_reviewable_summary_fixed_2026-04-14.md"


def build_summary() -> str:
    payload = json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))
    result = payload.get("result", {})
    trace = result.get("trace", [])
    admissible = result.get("admissible", False)

    lines = [
        "# LDK_REVIEWABLE_SUMMARY_FIXED — Generated Snapshot (2026-04-14)",
        "",
        f"- artifact_type: {payload.get('artifact_type', 'unknown')}",
        f"- source: {payload.get('source', 'unknown')}",
        f"- trace_length: {len(trace)}",
        f"- admissible: {admissible}",
        "",
        "## Interpretation",
        "This generated summary exists to make the fixed bounded LDK artifact readable by review-facing layers without mutating the bounded analytic object.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_summary())
