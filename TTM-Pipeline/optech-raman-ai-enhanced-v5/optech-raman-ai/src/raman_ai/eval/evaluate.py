
import os, json
import numpy as np
import pandas as pd

def run(feats_folder: str, model_path: str, out_path: str, uncertainty: bool=True):
    feats = pd.read_parquet(os.path.join(feats_folder, "features.parquet"))
    mp = model_path
    if mp.endswith(".pt"):
        mp = mp.replace(".pt",".pkl")
    with open(mp, "r") as f:
        model = json.load(f)
    mu = pd.Series(model.get("feature_means", {}))
    X = feats[mu.index].fillna(0.0)
    diffs = (X - mu).abs().mean().to_dict()
    metrics = {"mean_abs_feature_dev": diffs}
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2)
