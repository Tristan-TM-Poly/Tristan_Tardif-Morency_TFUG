from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def file_sha256(path: str, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    p = Path(path)
    with p.open('rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def deduplicate_zip_entries(zip_entries: list[dict[str, Any]]) -> dict[str, Any]:
    seen_hashes: dict[str, str] = {}
    unique_entries = []
    duplicates = []

    for entry in zip_entries:
        sha = file_sha256(entry['path'])
        enriched = dict(entry)
        enriched['sha256'] = sha
        if sha in seen_hashes:
            duplicates.append({
                'path': entry['path'],
                'duplicate_of': seen_hashes[sha],
                'sha256': sha,
            })
        else:
            seen_hashes[sha] = entry['path']
            unique_entries.append(enriched)

    return {
        'unique_entries': unique_entries,
        'duplicates': duplicates,
        'unique_count': len(unique_entries),
        'duplicate_count': len(duplicates),
    }
