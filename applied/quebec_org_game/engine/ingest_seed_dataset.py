from __future__ import annotations

import json
from pathlib import Path


def load_seed(path: str):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))


def ingest(seed_path: str):
    data = load_seed(seed_path)
    print(f"Loaded seed with {len(data.get('organizations', []))} organizations")


if __name__ == "__main__":
    ingest("applied/quebec_org_game/data/seed_dataset.json")
