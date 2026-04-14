from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "applied/2026-04-14/runtime/artifacts/abcd_synergy_everywhere_matrix_generated_2026-04-14.md"


def build_matrix() -> str:
    lines = [
        "# ABCD_SYNERGY_EVERYWHERE_MATRIX — Generated Snapshot (2026-04-14)",
        "",
        "| Family | Website | Demos | EduGame | AI-BOTS | Yggdrasil | AI-7/TRISTAN2 | Research/Publication |",
        "|---|---|---|---|---|---|---|---|",
        "| A^i synergies | visible modules | bounded pilots | challenge paths | guided hints | branch routes | direct corridors | pilot notes |",
        "| B^j meta-synergies | governance pages | anti-inflation surfaces | progression logic | orchestration doctrine | recoupling routes | packet/review/score | canon notes |",
        "| C^k generative-meta-synergies | workbenches | module generators | quest generators | adaptive planners | growth maps | runtime creation pipelines | thesis/publication packets |",
        "| D^l future generative-meta-synergies | roadmap surfaces | future demo tracks | long-horizon quest lines | future bot classes | future hypergraph expansions | staged future runtime programs | future labs and horizon notes |",
        "",
        "## Law",
        "The everywhere matrix is valid only if the four synergy families become cross-layer transport routes rather than isolated ranking buckets.",
    ]
    text = "\n".join(lines) + "\n"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(build_matrix())
