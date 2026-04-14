from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/interactive_demo_spec_generated_2026-04-14.md"


def build_spec() -> str:
    lines = [
        "# INTERACTIVE_DEMO_SPEC — Generated Snapshot (2026-04-14)",
        "",
        "## First bounded demo concepts",
        "1. Fractal-Loop explorer with bounded state transitions and readable observables",
        "2. bounded LDK visualizer with analytic trace interpretation",
        "3. Raman observability preview tied to bounded observable families",
        "",
        "## Experience rules",
        "- every demo must point to governed artifacts",
        "- every demo must stay bounded and interpretable",
        "- every demo should convert curiosity into a next step: note, artifact, or collaboration",
        "",
        "## Public conversion target",
        "The demo layer should function as a proof-of-entry surface for AT-1 rather than as disconnected spectacle.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_spec())
