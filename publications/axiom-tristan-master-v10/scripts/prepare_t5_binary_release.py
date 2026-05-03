#!/usr/bin/env python3
"""Prepare a T5 binary release package for Axiom-Tristan Master v10.

This script is intentionally local-first. It does not upload anything by itself.
It computes SHA-256, tests ZIP integrity, writes a BAT record draft, and emits
next commands for GitHub Release or another binary artifact channel.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import subprocess
from pathlib import Path


DEFAULT_NAME = "axiom_tristan_master_zip_v10_2026_05_01.zip"
ISSUE_URL = "https://github.com/Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG/issues/29"
WORKFLOW = ".github/workflows/verify-axiom-tristan-master-v10-binary.yml"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def unzip_test(path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        ["unzip", "-t", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode == 0, proc.stdout


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Axiom-Tristan Master v10 T5 binary release evidence.")
    parser.add_argument("zip_path", nargs="?", default=DEFAULT_NAME, help="Path to the master ZIP")
    parser.add_argument("--asset-url", default="PENDING_EXTERNAL_BINARY_ASSET_URL", help="External URL after upload")
    parser.add_argument("--out-dir", default="t5_release_evidence", help="Output evidence directory")
    args = parser.parse_args()

    zip_path = Path(args.zip_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not zip_path.exists():
        raise SystemExit(f"Missing ZIP: {zip_path}")

    digest = sha256_file(zip_path)
    ok, unzip_log = unzip_test(zip_path)
    now = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    write_text(out_dir / "sha256.txt", f"{digest}  {zip_path.name}\n")
    write_text(out_dir / "unzip_test.log", unzip_log)

    truth_level = "T5-candidate" if ok and args.asset_url != "PENDING_EXTERNAL_BINARY_ASSET_URL" else "T2-local-binary-verified"

    bat = {
        "artifact_name": zip_path.name,
        "version": "v10",
        "generated_utc": now,
        "truth_level": truth_level,
        "sha256": digest,
        "asset_url": args.asset_url,
        "local_unzip_test_passed": ok,
        "verification_workflow": WORKFLOW,
        "gate_issue": ISSUE_URL,
        "rollback": [
            "delete or unpublish incorrect external binary asset",
            "leave issue #29 open if external verification fails",
            "keep text indexes and downgrade binary status to T2 if needed",
        ],
        "non_claims": [
            "no cloud deployment",
            "no official filing",
            "no experimental validation",
            "no purchase",
            "no revenue action",
        ],
    }
    write_text(out_dir / "BAT_T5_BINARY_RECORD_DRAFT.json", json.dumps(bat, indent=2, ensure_ascii=False) + "\n")

    receipt = f"""# Axiom-Tristan Master v10 T5 Binary Release Evidence Draft

Generated: {now}

Artifact: `{zip_path.name}`

SHA-256:

```text
{digest}  {zip_path.name}
```

Local ZIP integrity:

```text
{'PASS' if ok else 'FAIL'}
```

External asset URL:

```text
{args.asset_url}
```

## Promotion state

- If asset URL is still pending: binary remains T2.
- If asset URL is real and GitHub Actions verification passes: binary can be promoted to T5.

## Run external verification workflow

Use GitHub Actions workflow:

```text
{WORKFLOW}
```

Inputs:

```text
asset_url={args.asset_url}
expected_sha256={digest}
```

## GitHub CLI release example

```bash
gh release create axiom-tristan-master-v10 {zip_path.name} \\
  --repo Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG \\
  --title "Axiom-Tristan Master v10" \\
  --notes "Master v10 binary archive. Verify with SHA-256: {digest}"
```

## Rollback

If verification fails, delete or unpublish the external asset and keep issue #29 open.
"""
    write_text(out_dir / "T5_BINARY_RELEASE_EVIDENCE_DRAFT.md", receipt)

    print(receipt)
    print(f"Wrote evidence directory: {out_dir}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
