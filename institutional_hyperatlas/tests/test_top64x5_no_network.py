#!/usr/bin/env python3
"""No-network validation tests for the AI-7 QC-CA Top 64^5 tensor.

These checks are intentionally local-only:
- validate axis sizes,
- validate tensor counts,
- validate generator output on a tiny limit,
- assert governance phrases are present,
- avoid scraping, cloud, secrets, or outreach.
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


def test_axes_have_64_entries():
    axes4 = json.loads(AXES4.read_text(encoding="utf-8"))
    axis5 = json.loads(AXIS5.read_text(encoding="utf-8"))
    assert len(axes4["A_institutions_sources"]) == 64
    assert len(axes4["B_challenges_sectors"]) == 64
    assert len(axes4["C_ai7_capabilities"]) == 64
    assert len(axes4["D_actions_governance"]) == 64
    assert len(axis5["E_dct_proof_prototype_maturity_gates"]) == 64


def test_tensor_counts_are_exact():
    axes4 = json.loads(AXES4.read_text(encoding="utf-8"))
    axis5 = json.loads(AXIS5.read_text(encoding="utf-8"))
    assert axes4["total_combinations"] == 64**4
    assert axis5["total_tensor_size_with_existing_axes"] == 64**5


def test_report_contains_governance_rule():
    text = REPORT5.read_text(encoding="utf-8")
    assert "PrivacyOK" in text
    assert "LicenseOK" in text
    assert "HumanReviewOK" in text
    assert "DCTReady" in text
    assert "Do not materialize" in text


def test_streaming_generator_small_topk():
    if TMP_OUT.exists():
        TMP_OUT.unlink()
    cmd = [
        sys.executable,
        str(GEN5),
        "--axes4",
        str(AXES4),
        "--axis5",
        str(AXIS5),
        "--limit",
        "5",
        "--out",
        str(TMP_OUT),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    rows = json.loads(TMP_OUT.read_text(encoding="utf-8"))
    assert len(rows) == 5
    for row in rows:
        assert set(row) == {"rank", "score", "institution_source", "challenge_sector", "ai7_capability", "action", "dct_gate"}
        assert 0 <= row["score"] <= 1
