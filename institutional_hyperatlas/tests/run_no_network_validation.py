#!/usr/bin/env python3
"""Standalone no-network validator for AI-7 Institutional HyperAtlas.

This script intentionally avoids pytest dependencies so it can run anywhere with Python.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AXES4 = ROOT / "institutional_hyperatlas/top_64x64x64x64/axes/top_64_axes.json"
AXIS5 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/axes/top_64_e_dct_axis.json"
GEN5 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/generator/generate_top64x5_tensor.py"
REPORT5 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/reports/top64x5_report.md"
TMP_OUT = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/reports/test_generated_top64x5.json"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    axes4 = json.loads(AXES4.read_text(encoding="utf-8"))
    axis5 = json.loads(AXIS5.read_text(encoding="utf-8"))
    check(len(axes4["A_institutions_sources"]) == 64, "A axis must have 64 entries")
    check(len(axes4["B_challenges_sectors"]) == 64, "B axis must have 64 entries")
    check(len(axes4["C_ai7_capabilities"]) == 64, "C axis must have 64 entries")
    check(len(axes4["D_actions_governance"]) == 64, "D axis must have 64 entries")
    check(len(axis5["E_dct_proof_prototype_maturity_gates"]) == 64, "E axis must have 64 entries")
    check(axes4["total_combinations"] == 64**4, "64^4 count mismatch")
    check(axis5["total_tensor_size_with_existing_axes"] == 64**5, "64^5 count mismatch")

    report = REPORT5.read_text(encoding="utf-8")
    for phrase in ["PrivacyOK", "LicenseOK", "HumanReviewOK", "DCTReady", "Do not materialize"]:
        check(phrase in report, f"Missing governance phrase: {phrase}")

    if TMP_OUT.exists():
        TMP_OUT.unlink()
    subprocess.run([
        sys.executable,
        str(GEN5),
        "--axes4", str(AXES4),
        "--axis5", str(AXIS5),
        "--limit", "5",
        "--out", str(TMP_OUT),
    ], check=True, cwd=ROOT)
    rows = json.loads(TMP_OUT.read_text(encoding="utf-8"))
    check(len(rows) == 5, "Generator must emit exactly 5 rows for --limit 5")
    for row in rows:
        check(0 <= row["score"] <= 1, "Score must be normalized to [0,1]")
        check("dct_gate" in row, "Generated row must include dct_gate")

    print("AI-7 no-network validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
