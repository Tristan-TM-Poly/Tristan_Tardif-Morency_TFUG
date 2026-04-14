from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/tfuga_interactive_gameplay_loop_generated_2026-04-14.md"


def build_loop() -> str:
    lines = [
        "# TFUGA_INTERACTIVE_GAMEPLAY_LOOP — Generated Snapshot (2026-04-14)",
        "",
        "## Core loop",
        "1. user explores a bounded TFUGA mechanic or object",
        "2. AI-7 adapts the interaction by surfacing next bounded actions or views",
        "3. TRISTAN2 scores, reviews, or gates what is shown next",
        "4. public layer offers one next move: learn, compare, collaborate, or inspect artifacts",
        "",
        "## Game-like rule",
        "The loop should feel progressive and interactive without becoming disconnected from governed evidence.",
        "",
        "## Law",
        "The gameplay loop is valid only if progression, curiosity, and conversion remain coupled to the TFUGA-AI7-TRISTAN2 trinity.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_loop())
