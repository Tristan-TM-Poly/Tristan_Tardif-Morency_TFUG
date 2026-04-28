#!/usr/bin/env python3
"""No-network validation for the AI-7 Top 64^8 MetaCanon tensor."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AXES4 = ROOT / "institutional_hyperatlas/top_64x64x64x64/axes/top_64_axes.json"
AXIS5 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/axes/top_64_e_dct_axis.json"
AXIS6 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64x64/axes/top_64_f_impactops_axis.json"
AXIS7 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64x64x64x64/axes/top_64_g_scale_context_axis.json"
AXIS8 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64x64x64x64/axes/top_64_h_metacanon_axis.json"
GEN8 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64x64x64x64/generator/generate_top64x8_beam.py"
TMP_OUT = ROOT / "institutional_hyperatlas/top_64x64x64x64x64x64x64x64/reports/test_generated_top64x8_beam.json"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    axes4 = json.loads(AXES4.read_text(encoding="utf-8"))
    axis5 = json.loads(AXIS5.read_text(encoding="utf-8"))
    axis6 = json.loads(AXIS6.read_text(encoding="utf-8"))
    axis7 = json.loads(AXIS7.read_text(encoding="utf-8"))
    axis8 = json.loads(AXIS8.read_text(encoding="utf-8"))

    for key in ["A_institutions_sources", "B_challenges_sectors", "C_ai7_capabilities", "D_actions_governance"]:
        check(len(axes4[key]) == 64, f"{key} must have 64 entries")
    check(len(axis5["E_dct_proof_prototype_maturity_gates"]) == 64, "E axis must have 64 entries")
    check(len(axis6["F_impactops_field_feedback_rollback_adoption"]) == 64, "F axis must have 64 entries")
    check(len(axis7["G_scale_territory_time_partner_context"]) == 64, "G axis must have 64 entries")
    check(len(axis8["H_metacanon_learning_transfer_reproduction"]) == 64, "H axis must have 64 entries")

    check(axis7["total_tensor_size_with_existing_axes"] == 64**7, "64^7 count mismatch")
    check(axis8["total_tensor_size_with_existing_axes"] == 64**8, "64^8 count mismatch")

    if TMP_OUT.exists():
        TMP_OUT.unlink()
    subprocess.run([
        sys.executable,
        str(GEN8),
        "--axes4", str(AXES4),
        "--axis5", str(AXIS5),
        "--axis6", str(AXIS6),
        "--axis7", str(AXIS7),
        "--axis8", str(AXIS8),
        "--beam-width", "16",
        "--limit", "5",
        "--out", str(TMP_OUT),
    ], check=True, cwd=ROOT)
    rows = json.loads(TMP_OUT.read_text(encoding="utf-8"))
    check(len(rows) == 5, "beam generator must emit exactly 5 rows")
    for row in rows:
        check(0 <= row["score"] <= 1, "score must be normalized")
        check("scale_context" in row, "row must include scale_context")
        check("metacanon_gate" in row, "row must include metacanon_gate")

    print("AI-7 Top64^8 beam validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
