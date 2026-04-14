from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/generated_ledger_index_2026-04-14.md"


def build_generated_ledger_index() -> str:
    lines = [
        "# GENERATED_LEDGER_INDEX — Generated Snapshot (2026-04-14)",
        "",
        "| Entry kind | Pointer | State |",
        "|---|---|---|",
        "| event row | runtime/artifacts/event_log_row_generated_2026-04-14.json | staged |",
        "| Fractal-Loop reviewable summary | runtime/artifacts/fractal_loop_reviewable_summary_2026-04-14.md | staged |",
        "| bounded LDK reviewable summary | runtime/artifacts/ldk_reviewable_summary_2026-04-14.md | staged |",
        "| Raman reviewable summary | runtime/artifacts/raman_reviewable_summary_2026-04-14.md | staged |",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_generated_ledger_index())
