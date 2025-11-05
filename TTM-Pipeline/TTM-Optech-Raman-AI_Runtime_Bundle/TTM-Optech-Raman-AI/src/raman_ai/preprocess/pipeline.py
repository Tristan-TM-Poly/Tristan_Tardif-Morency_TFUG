
import os, glob
import numpy as np
import pandas as pd
from . import spikes, baseline, norm, smooth, align as alignm

def run(parquet_folder: str, align: bool=True, baseline: str="asls", norm: str="snv", smooth: str="sg"):
    files = glob.glob(os.path.join(parquet_folder, "*.parquet"))
    for fp in files:
        df = pd.read_parquet(fp)
        x = df.loc[0, "x_cm_1"]
        y = df.loc[0, "y"]
        y1 = spikes.remove_spikes(y)
        y2 = baseline.correct(x, y1, method=baseline)
        y3 = norm.apply(y2, method=norm)
        y4 = smooth.apply(x, y3, method=smooth)
        if align:
            x_ref, y4 = alignm.align_to_ref(x, y4, ref_peak=520.7, max_shift=1.0)
            x = x_ref
        df.loc[0, "y_pp"] = [np.asarray(y4, dtype="float32")]
        df.loc[0, "x_cm_1"] = [np.asarray(x, dtype="float32")]
        df.to_parquet(fp, index=False)
