
import pandas as pd, numpy as np
from pathlib import Path
from optech_raman_ai.cli import run_features_dir

def make_parquet_dir(tmp: Path, n=3):
    tmp.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        x = np.linspace(100, 2000, 512)
        y = np.sin(x/80.0) + 0.02*np.random.randn(512)
        df = pd.DataFrame({"sample_id":[f"s{i}"]*len(x),
                           "wavenumber_cm1":x,
                           "intensity":y})
        df.to_parquet(tmp/f"s{i}.parquet", index=False)
    return tmp

def test_features_physics(tmp_path):
    inp = make_parquet_dir(tmp_path/"in")
    out = tmp_path/"feats.parquet"
    df = run_features_dir(inp, out, method="physics", prominence=0.01, distance=5, topk=3, downsample=64)
    assert out.exists()
    assert {"n_peaks","y_mean","y_std","area","file"}.issubset(df.columns)

def test_features_tfug(tmp_path):
    inp = make_parquet_dir(tmp_path/"in2")
    out = tmp_path/"feats_tfug.parquet"
    df = run_features_dir(inp, out, method="tfug", prominence=0.01, distance=5, topk=3, downsample=32)
    assert out.exists()
    assert any(c.startswith("emb_") for c in df.columns)
