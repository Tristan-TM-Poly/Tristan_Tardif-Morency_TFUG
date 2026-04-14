from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / 'applied/2026-04-14/runtime/artifacts/platform_stack_map_generated_2026-04-14.md'


def build_map() -> str:
    lines = [
        '# PLATFORM_STACK_MAP — Generated Snapshot (2026-04-14)',
        '',
        '## Shared stack',
        '- unified account identity layer',
        '- role and membership layer',
        '- packet and progression layer',
        '- review, audit, and rollback layer',
        '- subscription and donation layer',
        '',
        '## Surfaces',
        '- website: public and member portal',
        '- desktop app: heavier workbench and sovereign shell',
        '- Android app: mobile dashboard, demos, guidance, membership access',
        '',
        '## Law',
        'The platform stack is valid only if desktop, Android, and web remain one governed ecosystem rather than divergent products.',
    ]
    text = '\n'.join(lines) + '\n'
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(text, encoding='utf-8')
    return text


if __name__ == '__main__':
    print(build_map())
