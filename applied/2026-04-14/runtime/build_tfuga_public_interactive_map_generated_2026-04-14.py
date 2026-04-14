from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/tfuga_public_interactive_map_generated_2026-04-14.md"


def build_map() -> str:
    lines = [
        "# TFUGA_PUBLIC_INTERACTIVE_MAP — Generated Snapshot (2026-04-14)",
        "",
        "## Public modules",
        "- TFUGA Trinity Hub",
        "- Fractal-Loop Explorer",
        "- bounded LDK Visualizer",
        "- Raman Observability Preview",
        "- AT-1 Collaboration Gateway",
        "",
        "## Coupling rule",
        "Each module should expose one TFUGA object, one AI-7 interaction loop, one TRISTAN2 review/score/gate layer, and one public conversion path.",
        "",
        "## Law",
        "The public-interactive map is valid only if it preserves internal sovereignty while increasing external readability and engagement.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_map())
