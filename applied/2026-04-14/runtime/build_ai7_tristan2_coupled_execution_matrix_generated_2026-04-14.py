from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/ai7_tristan2_coupled_execution_matrix_generated_2026-04-14.md"


def build_matrix() -> str:
    lines = [
        "# AI7_TRISTAN2_COUPLED_EXECUTION_MATRIX — Generated Snapshot (2026-04-14)",
        "",
        "| Corridor | AI-7 role | TRISTAN2 role | Next governed step |",
        "|---|---|---|---|",
        "| centrale scoring corridor | emit score signals | interpret and gate via review/promote/hold | attach packet family and bounded pilot centrale config |",
        "| contradiction corridor | collect anomaly and contradiction intake | route contradiction/review/rollback/quarantine | emit contradiction packet and retry scope |",
        "| propagation corridor | produce bounded outputs | decide propagation or hold | attach propagation packet and sync stage |",
        "| monitoring corridor | Raman/process intake | preserve review and safety queues | attach monitoring packet and score row binding |",
        "",
        "## Law",
        "The coupled execution matrix is valid only when fast AI-7 metabolism and slow TRISTAN2 governance remain visibly distinct yet structurally linked.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_matrix())
