#!/usr/bin/env python3
"""Conservative quality gates for JWST AI-7 analysis."""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class QualityVector:
    bad_pixel_fraction: float = 0.0
    saturation_fraction: float = 0.0
    background_residual: float = 0.0
    wcs_rms_arcsec: float = 0.0
    psf_mismatch: float = 0.0
    artifact_score: float = 0.0
    calibration_known: bool = False

    def as_dict(self):
        return asdict(self)


def quality_score(q: QualityVector) -> float:
    """Return conservative governance quality score in [0, 1]."""
    penalties = (
        2.5 * q.bad_pixel_fraction
        + 3.0 * q.saturation_fraction
        + 0.5 * min(abs(q.background_residual), 1.0)
        + 0.25 * min(q.wcs_rms_arcsec, 4.0)
        + 0.8 * min(q.psf_mismatch, 1.0)
        + 0.8 * min(q.artifact_score, 1.0)
    )
    bonus = 0.08 if q.calibration_known else 0.0
    return max(0.0, min(1.0, 1.0 - penalties + bonus))


def quality_gate(q: QualityVector, threshold: float = 0.70):
    score = quality_score(q)
    return {
        "passed": score >= threshold,
        "score": round(score, 5),
        "threshold": threshold,
        "quality_vector": q.as_dict(),
    }
