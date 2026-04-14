from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/public_site_map_generated_2026-04-14.md"


def build_map() -> str:
    lines = [
        "# PUBLIC_SITE_MAP — Generated Snapshot (2026-04-14)",
        "",
        "## Recommended pages",
        "- Home",
        "- About",
        "- Theory and Systems",
        "- IA-7 and Governed Orchestration",
        "- Programs and Collaborations",
        "- Public Notes and Artifacts",
        "- Contact",
        "",
        "## Entry wedge",
        "- Governed orchestration for research, scientific AI, and instrumented complex systems",
        "",
        "## Calls to action",
        "- Explore research and engineering axes",
        "- Propose a problem or collaboration",
        "- Consult public artifacts and notes",
        "- Request technical or strategic framing",
        "",
        "## Law",
        "The site map is valid only if it creates a clear public entrypoint without flattening the project's maturity hierarchy.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_map())
