#!/usr/bin/env python3
"""DCT claim packets for JWST AI-7 analysis."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class DCTClaim:
    claim: str
    data_products: list[str]
    calibration_versions: dict[str, str]
    method: str
    equations: list[str]
    uncertainty: str
    tests: list[str]
    limitations: list[str]
    promotion_status: str = "candidate"

    def as_dict(self):
        return asdict(self)


def dct_claim_packet(
    claim: str,
    data_products: list[str],
    calibration_versions: dict[str, str] | None = None,
    method: str = "unspecified",
    equations: list[str] | None = None,
    uncertainty: str = "not yet quantified",
    tests: list[str] | None = None,
    limitations: list[str] | None = None,
) -> DCTClaim:
    return DCTClaim(
        claim=claim,
        data_products=data_products,
        calibration_versions=calibration_versions or {},
        method=method,
        equations=equations or [],
        uncertainty=uncertainty,
        tests=tests or [],
        limitations=limitations or [],
    )


def write_claim_packet(packet: DCTClaim, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
