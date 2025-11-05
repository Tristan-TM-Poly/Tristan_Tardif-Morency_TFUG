
import os, glob
import numpy as np
import pandas as pd
from . import peaks, ratios, fwt, df_estim

def run(parquet_folder: str, out_folder: str, fwt: bool=True, df: bool=True, peaks: str="voigt", ratios: str="default"):
    os.makedirs(out_folder, exist_ok=True)
    feats = []
    files = glob.glob(os.path.join(parquet_folder, "*.parquet"))
    for fp in files:
        df = pd.read_parquet(fp)
        x = df.loc[0, "x_cm_1"]
        y = df.loc[0, "y_pp"] if df.loc[0, "y_pp"] is not None else df.loc[0, "y"]
        f = {}
        f.update(peaks.extract(x, y, mode=peaks))
        f.update(ratios.extract(x, y, mode=ratios))
        if fwt:
            f.update(fwt.extract(y))
        if df:
            f.update(df_estim.extract(y))
        f["sample_id"] = df.loc[0, "sample_id"]
        feats.append(f)
    pd.DataFrame(feats).to_parquet(os.path.join(out_folder, "features.parquet"), index=False)
