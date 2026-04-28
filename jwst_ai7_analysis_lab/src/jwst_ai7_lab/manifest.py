#!/usr/bin/env python3
"""JWST AI-7 manifest helpers."""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class JWSTProduct:
    product_uri: str
    filename: str
    instrument: str | None = None
    detector: str | None = None
    filter_or_grating: str | None = None
    product_type: str | None = None
    stage: str | None = None
    cal_ver: str | None = None
    crds_ctx: str | None = None
    program_id: str | None = None
    target_name: str | None = None
    public: bool = True
    provenance_url: str | None = None

    def as_dict(self):
        return asdict(self)


def load_manifest(path: str | Path) -> list[JWSTProduct]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [JWSTProduct(**item) for item in data]


def stage_from_filename(filename: str) -> str | None:
    suffixes = {
        "uncal.fits": "Stage 0",
        "rate.fits": "Stage 1",
        "rateints.fits": "Stage 1",
        "cal.fits": "Stage 2",
        "calints.fits": "Stage 2",
        "i2d.fits": "Stage 3 image",
        "s3d.fits": "Stage 3 cube",
        "x1d.fits": "Stage 3 spectrum",
        "x1dints.fits": "Stage 3 time-series spectrum",
    }
    for suffix, stage in suffixes.items():
        if filename.endswith(suffix):
            return stage
    return None


def manifest_summary(path: str | Path) -> list[dict]:
    out = []
    for p in load_manifest(path):
        out.append({
            "filename": p.filename,
            "stage": p.stage or stage_from_filename(p.filename),
            "instrument": p.instrument,
            "target_name": p.target_name,
            "cal_ver": p.cal_ver,
            "crds_ctx": p.crds_ctx,
            "public": p.public,
        })
    return out
