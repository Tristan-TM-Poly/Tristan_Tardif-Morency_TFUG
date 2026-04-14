from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/monitoring_to_contradiction_chain_generated_2026-04-14.md"


def build_chain() -> str:
    lines = [
        "# MONITORING_TO_CONTRADICTION_CHAIN — Generated Snapshot (2026-04-14)",
        "",
        "## Chain",
        "1. AI-7 monitoring packet receives bounded Raman/process signal",
        "2. anomaly threshold is checked against bounded observable family",
        "3. contradiction packet is emitted when mismatch or breach appears",
        "4. contradiction packet is routed into TRISTAN2 review queue",
        "5. TRISTAN2 decides hold, retry, rollback, quarantine, or propagate",
        "",
        "## Law",
        "The chain is valid only if sensing increases local honesty and bounded correction instead of triggering uncontrolled autonomy or rhetorical escalation.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_chain())
