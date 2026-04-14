from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / 'applied/2026-04-14/runtime/artifacts/front_deployment_target_map_generated_2026-04-14.md'


def build_map() -> str:
    lines = [
        '# FRONT_DEPLOYMENT_TARGET_MAP — Generated Snapshot (2026-04-14)',
        '',
        '## Candidate targets',
        '- local preview via Vite',
        '- bounded staging deployment target',
        '- public release candidate host',
        '- broader public production host',
        '',
        '## Deployment corridors',
        '- release candidate front -> staging',
        '- staging -> public release candidate',
        '- public release candidate -> broader public deployment',
        '',
        '## Law',
        'A deployment target map is valid only if each target preserves rollback and maturity distinctions while increasing real public reach.',
    ]
    text = '\n'.join(lines) + '\n'
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding='utf-8')
    return text


if __name__ == '__main__':
    print(build_map())
