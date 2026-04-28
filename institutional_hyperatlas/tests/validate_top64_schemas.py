#!/usr/bin/env python3
"""Dependency-free schema-style validation for AI-7 Top 64 axes.

This is intentionally stricter than a loose smoke test and does not require jsonschema.
It validates the shape, exact counts, uniqueness, and tensor cardinalities.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AXES4 = ROOT / "institutional_hyperatlas/top_64x64x64x64/axes/top_64_axes.json"
AXIS5 = ROOT / "institutional_hyperatlas/top_64x64x64x64x64/axes/top_64_e_dct_axis.json"
SCHEMA4 = ROOT / "institutional_hyperatlas/schemas/top64_axes_schema.json"
SCHEMA5 = ROOT / "institutional_hyperatlas/schemas/top64_e_axis_schema.json"

AXES4_KEYS = [
    "A_institutions_sources",
    "B_challenges_sectors",
    "C_ai7_capabilities",
    "D_actions_governance",
]
AXIS5_KEY = "E_dct_proof_prototype_maturity_gates"


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def validate_axis(values, name):
    check(isinstance(values, list), f"{name} must be a list")
    check(len(values) == 64, f"{name} must contain exactly 64 entries")
    check(len(set(values)) == 64, f"{name} entries must be unique")
    for index, value in enumerate(values):
        check(isinstance(value, str), f"{name}[{index}] must be a string")
        check(value.strip(), f"{name}[{index}] must be non-empty")


def main():
    axes4 = json.loads(AXES4.read_text(encoding="utf-8"))
    axis5 = json.loads(AXIS5.read_text(encoding="utf-8"))
    schema4 = json.loads(SCHEMA4.read_text(encoding="utf-8"))
    schema5 = json.loads(SCHEMA5.read_text(encoding="utf-8"))

    for key in AXES4_KEYS:
        check(key in axes4, f"Missing key in 64^4 axes: {key}")
        validate_axis(axes4[key], key)
    check(axes4.get("count_per_axis") == 64, "count_per_axis must be 64")
    check(axes4.get("total_combinations") == 64**4, "64^4 total mismatch")

    check(AXIS5_KEY in axis5, f"Missing key in E-axis: {AXIS5_KEY}")
    validate_axis(axis5[AXIS5_KEY], AXIS5_KEY)
    check(axis5.get("count") == 64, "E-axis count must be 64")
    check(axis5.get("axis_name") == "E", "axis_name must be E")
    check(axis5.get("total_tensor_size_with_existing_axes") == 64**5, "64^5 total mismatch")

    check(schema4["properties"]["count_per_axis"]["const"] == 64, "schema4 count const mismatch")
    check(schema4["properties"]["total_combinations"]["const"] == 64**4, "schema4 total const mismatch")
    check(schema5["properties"]["count"]["const"] == 64, "schema5 count const mismatch")
    check(schema5["properties"]["total_tensor_size_with_existing_axes"]["const"] == 64**5, "schema5 total const mismatch")

    print("AI-7 Top64 schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
