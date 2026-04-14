from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/interactive_demo_cards_generated_2026-04-14.md"


def build_cards() -> str:
    lines = [
        "# INTERACTIVE_DEMO_CARDS — Generated Snapshot (2026-04-14)",
        "",
        "## Cards",
        "- Fractal-Loop Explorer: bounded state transitions and readable observables",
        "- bounded LDK Visualizer: analytic trace interpretation and admissibility view",
        "- Raman Preview: bounded observable-family exploration",
        "- AT-1 Demo Hub: public cockpit-style gateway into demos and artifacts",
        "",
        "## Card law",
        "Each demo card should expose a bounded concept, a readable promise, and one next action.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_cards())
