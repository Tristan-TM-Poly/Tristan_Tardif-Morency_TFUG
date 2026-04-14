from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/tfuga_edugame_loop_generated_2026-04-14.md"


def build_loop() -> str:
    lines = [
        "# TFUGA_EDUGAME_LOOP — Generated Snapshot (2026-04-14)",
        "",
        "## Core loop",
        "1. player enters a bounded TFUGA concept zone",
        "2. AI-BOT NPC proposes one admissible path, challenge, or hint",
        "3. player acts inside a bounded mechanic or system view",
        "4. TRISTAN2 scores, reviews, or gates what unlocks next",
        "5. AI-7 adapts the next activity, comparison, or artifact route",
        "6. player exits toward deeper theory, system practice, or collaboration",
        "",
        "## Learning law",
        "The loop is valid only if play increases theory understanding, system literacy, and governed experimentation rather than passive consumption.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_loop())
