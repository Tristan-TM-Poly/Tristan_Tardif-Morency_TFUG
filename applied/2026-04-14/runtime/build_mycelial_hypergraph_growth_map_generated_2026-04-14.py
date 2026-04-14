from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/mycelial_hypergraph_growth_map_generated_2026-04-14.md"


def build_map() -> str:
    lines = [
        "# MYCELIAL_HYPERGRAPH_GROWTH_MAP — Generated Snapshot (2026-04-14)",
        "",
        "## Growth layers",
        "- node seeds: TFUGA objects, pilots, packets, pages, demos",
        "- branch links: local concept and module couplings",
        "- mycelial links: transversal multi-branch recouplings",
        "- hyperedges: many-to-many structured relations across scales and languages",
        "- public surfaces: pages, demos, NPC routes, collaboration corridors",
        "",
        "## Growth law",
        "Growth is valid only if new nodes and links increase transportability, reviewability, and multi-scale legibility instead of raw graph mass.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_map())
