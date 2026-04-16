from __future__ import annotations

import concurrent.futures
from pathlib import Path
import zipfile
from typing import Any


def extract_one(path: str, output_dir: str) -> dict[str, Any]:
    p = Path(path)
    try:
        with zipfile.ZipFile(p, 'r') as z:
            z.extractall(Path(output_dir) / p.stem)
        return {'path': path, 'status': 'extracted'}
    except Exception as e:
        return {'path': path, 'status': 'error', 'error': str(e)}


def parallel_extract(zip_entries: list[dict[str, Any]], output_dir: str, max_workers: int = 4):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(extract_one, e['path'], output_dir) for e in zip_entries]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
    return results
