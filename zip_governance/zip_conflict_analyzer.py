from __future__ import annotations

from typing import Any


def analyze_conflicts(zip_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {}
    conflicts = []

    for entry in zip_entries:
        name = entry["name"]
        if name in seen:
            conflicts.append({
                "file": name,
                "paths": [seen[name], entry["path"]],
                "type": "duplicate_name"
            })
        else:
            seen[name] = entry["path"]

    return conflicts
