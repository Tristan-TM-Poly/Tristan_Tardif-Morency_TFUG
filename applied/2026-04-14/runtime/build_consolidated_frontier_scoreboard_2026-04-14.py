from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/consolidated_frontier_scoreboard_2026-04-14.md"


def build_scoreboard() -> str:
    lines = [
        "# CONSOLIDATED_FRONTIER_SCOREBOARD — Generated Snapshot (2026-04-14)",
        "",
        "| Pilot | Consolidated reading | Rank |",
        "|---|---|---|",
        "| Fractal-Loop | strongest governed frontier with executable placeholder, emitter, and reviewable chain | 1 |",
        "| bounded LDK pilot | strongest analytic companion frontier with placeholder and reviewable builder | 2 |",
        "| Raman pilot | strongest next scientific frontier with bounded data/observable scaffolds | 3 |",
        "| TFUGA-Mol controlled branch | controlled non-competing frontier | 4 |",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_scoreboard())
