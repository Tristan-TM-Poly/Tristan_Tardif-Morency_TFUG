from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MEMORY_PATH = Path("out/tfuga/memory_log.jsonl")


def append_record(record: dict[str, Any], path: Path = DEFAULT_MEMORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    record = dict(record)
    record["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_all(path: Path = DEFAULT_MEMORY_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records
