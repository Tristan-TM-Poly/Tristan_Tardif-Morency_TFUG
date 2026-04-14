from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/pilot_frontier_scoreboard_state_generated_2026-04-14.md"


def build_scoreboard_state() -> str:
    lines = [
        "# PILOT_FRONTIER_SCOREBOARD_STATE — Generated Snapshot (2026-04-14)",
        "",
        "| Pilot | Runtime signal | Review signal | Frontier reading |",
        "|---|---|---|---|",
        "| Fractal-Loop | emitter and reviewable chain staged | review/falsification/summary staged | strongest governed frontier |",
        "| bounded LDK pilot | placeholder and emitter staged | benchmark and reviewable builder staged | strongest analytic companion frontier |",
        "| Raman pilot | no runtime yet | benchmark/review bridge staged | strongest next scientific frontier |",
        "| TFUGA-Mol controlled branch | partial | controlled | bounded non-competing branch |",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_scoreboard_state())
