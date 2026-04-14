from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/auto_generator_catalog_generated_2026-04-14.md"


def build_catalog() -> str:
    lines = [
        "# AUTO_GENERATOR_CATALOG — Generated Snapshot (2026-04-14)",
        "",
        "## Generator families",
        "- homepage copy generators",
        "- landing section generators",
        "- interactive demo card generators",
        "- collaboration CTA generators",
        "- navigation generators",
        "- visualizer generators",
        "- trinity public coupling generators",
        "",
        "## Generator law",
        "Each generator family should remain small, composable, and visibly coupled to governed packets, review paths, and public progression.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_catalog())
