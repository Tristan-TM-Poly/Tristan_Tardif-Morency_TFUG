
import os, pandas as pd, numpy as np
from raman_ai.io.parquet import ensure_parquet
from raman_ai.preprocess.pipeline import run as run_prep

def test_prep_tmp(tmp_path):
    raw = tmp_path/"raw"; raw.mkdir()
    p = raw/"s1.csv"
    p.write_text("x,y\n500,0\n520,10\n540,1\n")
    out = tmp_path/"parquet"; out.mkdir()
    ensure_parquet(str(raw), str(out))
    run_prep(str(out), align=True, baseline="asls", norm="snv", smooth="sg")
    files = list(out.glob("*.parquet"))
    assert len(files)==1
    df = pd.read_parquet(files[0])
    assert df.loc[0,"y_pp"] is not None
