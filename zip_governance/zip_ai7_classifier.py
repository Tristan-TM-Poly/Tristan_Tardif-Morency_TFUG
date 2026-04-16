from __future__ import annotations

from typing import Any


def classify_zip(entry: dict[str, Any]) -> dict[str, Any]:
    name = entry.get('name', '').lower()

    if 'data' in name:
        category = 'dataset'
    elif 'report' in name:
        category = 'report'
    elif 'image' in name or 'media' in name:
        category = 'media'
    else:
        category = 'unknown'

    score = 1.0 if category != 'unknown' else 0.3

    return {
        'path': entry.get('path'),
        'category': category,
        'confidence': score
    }


def classify_all(zip_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [classify_zip(e) for e in zip_entries]
