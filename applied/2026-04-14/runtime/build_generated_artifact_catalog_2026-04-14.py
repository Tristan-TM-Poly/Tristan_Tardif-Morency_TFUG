from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "applied/2026-04-14/runtime/artifacts"
OUTPUT_PATH = ARTIFACTS / "generated_artifact_catalog_2026-04-14.md"


def build_catalog() -> str:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    entries = sorted(p.name for p in ARTIFACTS.iterdir() if p.is_file())
    lines = [
        "# GENERATED_ARTIFACT_CATALOG — Generated Snapshot (2026-04-14)",
        "",
        f"- artifact_count: {len(entries)}",
        "",
        "## Files",
    ]
    lines.extend(f"- {name}" for name in entries)
    lines += [
        "",
        "## Law",
        "The generated artifact catalog exists to keep the automation layer inspectable as output volume grows.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_catalog())
