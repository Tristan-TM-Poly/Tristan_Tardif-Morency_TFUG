from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATASET_POINTER = ROOT / "applied/2026-04-14/pilots/RAMAN_DATASET_POINTER_ARTIFACT_2026-04-14.md"
OBSERVABLE_PACKET = ROOT / "applied/2026-04-14/packets/RAMAN_OBSERVABLE_PACKET_2026-04-14.md"
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/raman_reviewable_summary_2026-04-14.md"


def build_summary() -> str:
    lines = [
        "# RAMAN_REVIEWABLE_SUMMARY — Generated Snapshot (2026-04-14)",
        "",
        f"- dataset_pointer_artifact: {DATASET_POINTER.name}",
        f"- observable_packet: {OBSERVABLE_PACKET.name}",
        "- current_state: staged",
        "",
        "## Interpretation",
        "This generated summary exists to keep the Raman frontier review-readable while its bounded dataset family and observable vocabulary are still being tightened.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_summary())
