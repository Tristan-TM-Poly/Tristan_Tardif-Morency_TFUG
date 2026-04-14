from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/company_collaboration_packet_generated_2026-04-14.md"


def build_packet() -> str:
    lines = [
        "# COMPANY_COLLABORATION_PACKET — Generated Snapshot (2026-04-14)",
        "",
        "## Collaboration modes",
        "- research collaborations",
        "- applied technical pilots",
        "- scientific AI and instrumentation programs",
        "- public demonstration and educational partnerships",
        "",
        "## Entry conditions",
        "- bounded problem statement",
        "- visible success criterion",
        "- governed artifact or note family",
        "- clear next collaboration step",
        "",
        "## Company-facing promise",
        "AT-1 should appear as a structured and credible interface between deep theory, orchestrated engineering, and bounded public demonstrations.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_packet())
