from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/auto_generator_cards_generated_2026-04-14.md"


def build_cards() -> str:
    lines = [
        "# AUTO_GENERATOR_CARDS — Generated Snapshot (2026-04-14)",
        "",
        "## Cards",
        "- Homepage Copy Generator: produces bounded hero and CTA structures",
        "- Demo Card Generator: produces public demo cards tied to governed artifacts",
        "- Visualizer Generator: produces small visual module scaffolds",
        "- Navigation Generator: produces bounded public navigation fragments",
        "- Trinity Coupling Generator: produces modules explicitly tied to TFUGA x AI-7 x TRISTAN2",
        "",
        "## Card law",
        "Each auto-generator card should expose a readable promise, one bounded output family, and one next action.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_cards())
