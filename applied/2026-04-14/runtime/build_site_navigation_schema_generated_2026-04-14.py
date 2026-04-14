from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/site_navigation_schema_generated_2026-04-14.md"


def build_schema() -> str:
    lines = [
        "# SITE_NAVIGATION_SCHEMA — Generated Snapshot (2026-04-14)",
        "",
        "## Primary navigation",
        "- Home",
        "- Theory and Systems",
        "- Demos",
        "- Programs",
        "- Notes",
        "- Contact",
        "",
        "## Secondary navigation",
        "- TFUGA",
        "- IA-7",
        "- AT-1",
        "- Collaborations",
        "- Public artifacts",
        "",
        "## Law",
        "Navigation should mirror public maturity and collaboration pathways rather than internal archive depth.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_schema())
