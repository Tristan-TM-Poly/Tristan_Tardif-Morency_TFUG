
import pandas as pd, numpy as np, os
from raman_ai.features.tfuq import extract

def test_tfuq_extract_shapes():
    y = np.sin(np.linspace(0, 20, 1024)) + 0.1*np.random.randn(1024)
    f = extract(y)
    assert "tfuq_q0" in f and "tfuq_q_norm2" in f and "tfuq_psd_slope" in f
    assert any(k.startswith("tfuq_ms_energy_L") for k in f.keys())
