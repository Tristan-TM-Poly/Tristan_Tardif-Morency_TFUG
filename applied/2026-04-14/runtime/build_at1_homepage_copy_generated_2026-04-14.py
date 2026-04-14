from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/at1_homepage_copy_generated_2026-04-14.md"


def build_copy() -> str:
    lines = [
        "# AT1_HOMEPAGE_COPY — Generated Snapshot (2026-04-14)",
        "",
        "## Hero",
        "Axiom-Tristan (AT-1) builds governed research, scientific AI, and instrumented system architectures that connect deep theory, orchestration, and applied deployment.",
        "",
        "## Sub-hero",
        "AT-1 brings together TFUGA, IA-7, and public collaboration pathways to turn structured scientific depth into demonstrable systems, bounded interactive experiences, and credible technical programs.",
        "",
        "## Primary calls to action",
        "- Explore theory and systems",
        "- See public artifacts and demos",
        "- Start a collaboration",
        "- Request technical framing",
        "",
        "## Credibility line",
        "Public surfaces should show governed maturity, bounded demonstrations, and readable entrypoints rather than uncontrolled amplitude.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_copy())
