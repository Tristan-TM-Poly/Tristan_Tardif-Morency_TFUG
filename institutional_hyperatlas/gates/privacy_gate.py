#!/usr/bin/env python3
"""Minimal privacy gate for AI-7 Institutional HyperAtlas records.

This gate is intentionally conservative. It rejects records that look like
people-level data unless they have been explicitly marked for manual review.
"""
import json
import re
import sys
from pathlib import Path

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){2}\d{4}")
PERSON_KEYS = {"person", "employee", "staff", "email", "phone", "linkedin", "contact_name"}


def scan_record(record):
    text = json.dumps(record, ensure_ascii=False).lower()
    flags = []
    if EMAIL_RE.search(text):
        flags.append("email_detected")
    if PHONE_RE.search(text):
        flags.append("phone_detected")
    if any(k in text for k in PERSON_KEYS):
        flags.append("person_level_keyword")
    privacy_level = record.get("privacy_level", "")
    if privacy_level == "contains_personal_data_reject_or_minimize":
        flags.append("explicit_personal_data_level")
    return flags


def main():
    if len(sys.argv) < 2:
        print("Usage: privacy_gate.py <records.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    records = json.loads(path.read_text(encoding="utf-8"))
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
