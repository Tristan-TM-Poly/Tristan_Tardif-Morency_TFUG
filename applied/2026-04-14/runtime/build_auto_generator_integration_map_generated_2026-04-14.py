from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/auto_generator_integration_map_generated_2026-04-14.md"


def build_map() -> str:
    lines = [
        "# AUTO_GENERATOR_INTEGRATION_MAP — Generated Snapshot (2026-04-14)",
        "",
        "## Integration targets",
        "- AT1LandingPageGenerated.tsx",
        "- TFUGATrinityInteractivePageGenerated.tsx",
        "- FractalLoopVisualizerGenerated.tsx",
        "- BoundedLDKVisualizerGenerated.tsx",
        "- PublicInteractiveNavigationGenerated.tsx",
        "",
        "## Integration rule",
        "Generated modules should be inserted as bounded sections, cards, or panels that remain linked to TFUGA objects, AI-7 interaction logic, and TRISTAN2 governance constraints.",
        "",
        "## Law",
        "The integration map is valid only if module generation increases public richness without fragmenting the web layer into uncoupled parts.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_map())
