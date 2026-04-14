from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/interactive_experience_roadmap_generated_2026-04-14.md"


def build_roadmap() -> str:
    lines = [
        "# INTERACTIVE_EXPERIENCE_ROADMAP — Generated Snapshot (2026-04-14)",
        "",
        "## Experience tracks",
        "1. Fractal-Loop interactive explorer",
        "2. bounded LDK analytic visualizer",
        "3. Raman frontier observability demo",
        "4. public AT-1 cockpit-style demo hub",
        "",
        "## Principles",
        "- every demo should be bounded",
        "- every demo should point to a governed artifact family",
        "- every demo should increase clarity before spectacle",
        "- interactive layers should convert public interest into collaboration or technical dialogue",
        "",
        "## Law",
        "Interactive experiences are valid only when they make governed internal structure legible to external users without inflating maturity claims.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_roadmap())
