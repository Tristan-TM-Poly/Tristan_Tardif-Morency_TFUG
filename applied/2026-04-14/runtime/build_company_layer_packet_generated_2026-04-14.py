from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/company_layer_packet_generated_2026-04-14.md"


def build_packet() -> str:
    lines = [
        "# COMPANY_LAYER_PACKET — Generated Snapshot (2026-04-14)",
        "",
        "## Public identity",
        "- master public entity: Axiom-Tristan (AT-1)",
        "- three-pillar framing: TFUGA / IA-7 / AT-1",
        "- public role: convert deep structures into programs, tools, collaborations, demonstrations, and applications",
        "",
        "## Company-facing surfaces",
        "- public website",
        "- collaboration programs",
        "- public notes and artifacts",
        "- interactive demo layer",
        "",
        "## Company law",
        "The company layer should appear as ambitious, structured, credible, readable, and immediately actionable.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_packet())
