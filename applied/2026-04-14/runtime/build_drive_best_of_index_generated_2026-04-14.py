from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/drive_best_of_index_generated_2026-04-14.md"


def build_index() -> str:
    lines = [
        "# DRIVE_BEST_OF_INDEX — Generated Snapshot (2026-04-14)",
        "",
        "## Best-of active families",
        "- sovereign trunk doctrine and active runtime governance",
        "- Fractal-Loop pilot closure artifacts",
        "- bounded LDK analytic companion artifacts",
        "- Raman frontier governance and reporting artifacts",
        "- automation, improvement, writing, and publication-prep layers",
        "",
        "## Promotion rule",
        "Only the best Drive artifacts that are trunk-facing, reusable, reviewable, benchmarkable, or publication-prep-relevant should be concentrated into GitHub.",
        "",
        "## Law",
        "The generated best-of index exists to prevent the GitHub layer from becoming archive bulk while still concentrating the strongest current Drive assets into executable memory.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_index())
