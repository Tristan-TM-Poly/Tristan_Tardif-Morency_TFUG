from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/collaboration_cta_packet_generated_2026-04-14.md"


def build_packet() -> str:
    lines = [
        "# COLLABORATION_CTA_PACKET — Generated Snapshot (2026-04-14)",
        "",
        "## Primary CTAs",
        "- Start a research collaboration",
        "- Propose an applied pilot",
        "- Request a technical framing session",
        "- Explore public notes and demo entrypoints",
        "",
        "## CTA law",
        "Calls to action should turn public clarity into bounded next steps rather than generic contact noise.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_packet())
