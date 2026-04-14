from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/frontier_governance_digest_generated_2026-04-14.md"


def build_digest() -> str:
    lines = [
        "# FRONTIER_GOVERNANCE_DIGEST — Generated Snapshot (2026-04-14)",
        "",
        "## Current generated reading",
        "- Fractal-Loop remains the deepest governed frontier.",
        "- bounded LDK remains the strongest analytic companion frontier.",
        "- Raman remains the strongest next scientific frontier.",
        "- TFUGA-Mol remains controlled to preserve anti-diffusion discipline.",
        "",
        "## Generated law",
        "This digest is generated so the frontier hierarchy can be re-read from the automation layer without replacing the deeper score, review, benchmark, and packet structures.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_digest())
