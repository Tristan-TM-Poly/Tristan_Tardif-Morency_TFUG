from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / 'applied/2026-04-14/runtime/artifacts/front_auto_improvement_loop_generated_2026-04-14.md'


def build_loop() -> str:
    lines = [
        '# FRONT_AUTO_IMPROVEMENT_LOOP — Generated Snapshot (2026-04-14)',
        '',
        '## Loop',
        '1. absorb front routes, pages, packets, and generated modules',
        '2. canonize the strongest current front path and identify weak zones',
        '3. generate bounded improvements and generated module candidates',
        '4. propagate changes across release, membership, AI-BOTS, Yggdrasil, and demos',
        '5. test navigability and route coherence',
        '6. cleanup duplication and weak surfaces',
        '7. reindex preferred front paths and release candidate state',
        '',
        '## Law',
        'The loop is valid only if generated front changes are routed through governed review and produce a denser public application layer.',
    ]
    text = '\n'.join(lines) + '\n'
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding='utf-8')
    return text


if __name__ == '__main__':
    print(build_loop())
