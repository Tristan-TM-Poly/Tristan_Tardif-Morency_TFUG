from __future__ import annotations

from typing import Any


def build_merge_plan(zip_entries: list[dict[str, Any]], conflicts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_zips": len(zip_entries),
        "conflicts": conflicts,
        "actions": [
            {"action": "extract", "path": e["path"]}
            for e in zip_entries
        ],
        "status": "planned"
    }
