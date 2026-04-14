from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/drive_to_github_migration_queue_generated_2026-04-14.md"


def build_queue() -> str:
    lines = [
        "# DRIVE_TO_GITHUB_MIGRATION_QUEUE — Generated Snapshot (2026-04-14)",
        "",
        "## Priority queue",
        "1. sovereign trunk governance docs and runtime-facing canon",
        "2. active pilot governance artifacts for Fractal-Loop",
        "3. bounded LDK analytic companion artifacts",
        "4. Raman frontier artifacts that are already review/benchmark/data-facing",
        "5. automation, improvement, writing, and publication-prep outputs",
        "",
        "## Deferred",
        "- archive-heavy historical bundles",
        "- broad exploratory masses without current closure value",
        "- objects that are memory-rich but not yet trunk-facing or code-facing",
        "",
        "## Law",
        "The migration queue exists so Drive-to-GitHub promotion follows closure depth and reuse value rather than archive mass.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_queue())
