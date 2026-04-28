#!/usr/bin/env python3
"""Optional MAST hooks for JWST AI-7 analysis.

No network calls happen unless this function is explicitly called and astroquery
is installed. Keep this module outside no-network CI.
"""
from __future__ import annotations


def query_mast_observations(**criteria):
    try:
        from astroquery.mast import Observations
    except Exception as exc:
        raise RuntimeError("astroquery is required for MAST queries: pip install astroquery") from exc
    return Observations.query_criteria(obs_collection="JWST", **criteria)
