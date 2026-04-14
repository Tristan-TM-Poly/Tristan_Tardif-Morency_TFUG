from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/automation_bundle_report_resilient_2026-04-14.json"
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/automation_digest_generated_2026-04-14.md"


def build_digest() -> str:
    payload = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    ok_count = payload.get("ok_count", 0)
    fail_count = payload.get("fail_count", 0)
    lines = [
        "# AUTOMATION_DIGEST — Generated Snapshot (2026-04-14)",
        "",
        f"- ok_count: {ok_count}",
        f"- fail_count: {fail_count}",
        "",
        "## Reading",
        "This generated digest compresses the current resilient automation run into a governance-facing summary without hiding failed steps.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_digest())
