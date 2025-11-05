"""
TFUG/FWT quaternionic placeholder module.

This module defines a stable interface that can be swapped with a
production-grade implementation without breaking downstream code.
"""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass
class TFUGFWTConfig:
    level: int = 4
    basis: str = "q-fwt-v1"
    downsample: int = 64

class TFUGFWTEmbedder:
    def __init__(self, config: TFUGFWTConfig | None = None):
        self.config = config or TFUGFWTConfig()

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Return an embedding for a single spectrum dataframe
        with columns ['wavenumber_cm1', 'intensity'].
        """
        x = df["wavenumber_cm1"].to_numpy()
        y = df["intensity"].to_numpy()
        # Placeholder: deterministic downsampling + stats (mean, std).
        stride = max(1, len(y)//self.config.downsample)
        core = y[::stride][: self.config.downsample]
        emb = np.concatenate([core, np.array([y.mean(), y.std()], dtype=float)])
        return emb

def batch_transform(dfs: list[pd.DataFrame], config: TFUGFWTConfig | None = None) -> np.ndarray:
    emb = TFUGFWTEmbedder(config)
    return np.vstack([emb.transform(df) for df in dfs])
