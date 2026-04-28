#!/usr/bin/env python3
"""Minimal licence gate for AI-7 Institutional HyperAtlas records."""
import json
import sys
from pathlib import Path

BAD = {"", "unknown", "unclear", "none", "n/a", "varies", "varies by dataset"}


def scan_record(record):
    flags = []
    sources = record.get("sources", [])
    if not sources:
        flags.append("missing_sources")
    for i, src in enumerate(sources):
        licence = str(src.get("license", "")).strip().lower()
        if licence in BAD:
            flags.append(f"source_{i}_unclear_license")
        if not src.get("url"):
            flags.append(f"source_{i}_missing_url")
        if not src.get("retrieved_at"):
            flags.append(f"source_{i}_missing_retrieved_at")
    return flags


def main():
    if len(sys.argv) < 2:
        print("Usage: license_gate.py <records.json>", file=sys.stderr)
        return 2
    records = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if isinstance(records, dict):
        records = [records]
    findings = []
    for idx, record in enumerate(records):
        flags = scan_record(record)
        if flags:
            findings.append({"index": idx, "id": record.get("id"), "flags": flags})
    result = {"passed": not findings, "findings": findings}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
