from __future__ import annotations

import zipfile
from typing import Any


def analyze_zip_contents(path: str, max_files: int = 50) -> dict[str, Any]:
    summary = {
        'path': path,
        'file_count': 0,
        'sample_files': [],
        'types': set()
    }

    try:
        with zipfile.ZipFile(path, 'r') as z:
            names = z.namelist()
            summary['file_count'] = len(names)

            for name in names[:max_files]:
                summary['sample_files'].append(name)
                if '.' in name:
                    ext = name.split('.')[-1].lower()
                    summary['types'].add(ext)

    except Exception as e:
        return {
            'path': path,
            'status': 'error',
            'error': str(e)
        }

    summary['types'] = list(summary['types'])
    summary['status'] = 'analyzed'
    return summary


def analyze_many(zip_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [analyze_zip_contents(e['path']) for e in zip_entries]
