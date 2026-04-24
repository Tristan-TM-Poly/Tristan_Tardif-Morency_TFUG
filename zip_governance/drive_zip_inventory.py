from __future__ import annotations

from pathlib import Path
from typing import Any


def scan_for_zips(root: str) -> list[dict[str, Any]]:
    base = Path(root)
    results = []
    if not base.exists():
        return results
    for path in base.rglob("*.zip"):
        results.append({
            "name": path.name,
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "parent": str(path.parent),
        })
    return results
