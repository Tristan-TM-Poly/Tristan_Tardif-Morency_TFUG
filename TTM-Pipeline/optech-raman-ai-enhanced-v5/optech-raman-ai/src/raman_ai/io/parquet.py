
import os, glob
import numpy as np
import pandas as pd

def _guess_is_raw(folder: str) -> bool:
    return len(glob.glob(os.path.join(folder, "*.csv"))) + len(glob.glob(os.path.join(folder, "*.txt"))) > 0

def _read_raw_to_df(folder: str) -> pd.DataFrame:
    rows = []
    for p in glob.glob(os.path.join(folder, "*.csv")) + glob.glob(os.path.join(folder, "*.txt")):
        try:
            df = pd.read_csv(p)
        except Exception:
            df = pd.read_csv(p, sep="\t")
        if "x" not in df.columns or "y" not in df.columns:
            cols = df.columns.tolist()
            if len(cols) >= 2:
                df = df.rename(columns={cols[0]: "x", cols[1]: "y"})
        x = df["x"].astype("float32").to_numpy()
        y = df["y"].astype("float32").to_numpy()
        rows.append({
            "sample_id": os.path.splitext(os.path.basename(p))[0],
            "instrument_id": "unknown",
            "laser_nm": np.int16(532),
            "power_mw": np.float32(1.0),
            "integration_s": np.float32(1.0),
            "temp_C": np.float32(25.0),
            "datetime": pd.Timestamp.now().value // 10**6,
            "x_cm_1": x,
            "y": y,
            "label_material": None,
            "y_targets": None,
            "split": None,
        })
    return pd.DataFrame(rows)

def ensure_parquet(in_folder: str, out_folder: str):
    os.makedirs(out_folder, exist_ok=True)
    if _guess_is_raw(in_folder):
        df = _read_raw_to_df(in_folder)
        for _, row in df.iterrows():
            pdf = pd.DataFrame({"x_cm_1": [row["x_cm_1"]], "y": [row["y"]]})
            for k in ["sample_id","instrument_id","laser_nm","power_mw","integration_s","temp_C","datetime","label_material","y_targets","split"]:
                pdf[k] = [row[k]]
            pdf.to_parquet(os.path.join(out_folder, f"{row['sample_id']}.parquet"), index=False)
    else:
        pass
