
import click
from pathlib import Path
import sys, json

try:
    from .data.convert_csv_to_parquet import convert_folder as convert_csv_folder
except Exception:
    convert_csv_folder = None

try:
    from .utils.deduplicate import deduplicate_folder
except Exception:
    deduplicate_folder = None

from .features.fwt_tfug import TFUGFWTEmbedder, TFUGFWTConfig

import pandas as pd
import numpy as np
from scipy.signal import find_peaks

@click.group()
def main():
    """Optech Raman AI — CLI."""

@main.command("convert-csv")
@click.option("--input", "input_dir", type=click.Path(path_type=Path), required=True)
@click.option("--output", "output_dir", type=click.Path(path_type=Path), required=True)
def convert_csv(input_dir: Path, output_dir: Path):
    """Convertir tous les CSV d'un dossier en Parquet (schéma auto minimal)."""
    if convert_csv_folder is None:
        raise click.ClickException("convert_csv_folder indisponible dans ce build.")
    convert_csv_folder(input_dir, output_dir)

@main.command("dedup")
@click.option("--input", "input_dir", type=click.Path(path_type=Path), required=True)
@click.option("--hash", "algo", type=click.Choice(["sha1","md5","size_mtime"], case_sensitive=False), default="sha1")
def dedup(input_dir: Path, algo: str):
    """Dé-duplication simple d'un dossier (parquet/...) via hash ou taille+mtime."""
    if deduplicate_folder is None:
        raise click.ClickException("deduplicate_folder indisponible dans ce build.")
    deduplicate_folder(input_dir, algo=algo)

def extract_features_physics(df: pd.DataFrame, prominence: float, distance: int, topk: int) -> dict:
    x = df["wavenumber_cm1"].to_numpy()
    y = df["intensity"].to_numpy()
    peaks, props = find_peaks(y, prominence=prominence, distance=distance)
    prom = props.get("prominences", np.zeros_like(peaks))
    order = np.argsort(prom)[::-1]
    peaks = peaks[order][:topk]
    feats = {
        "n_peaks": int(len(peaks)),
        "y_mean": float(np.mean(y)),
        "y_std": float(np.std(y)),
        "area": float(np.trapz(y, x)),
    }
    for i, p in enumerate(peaks):
        feats[f"peak_{i+1}_pos"] = float(x[p])
        feats[f"peak_{i+1}_height"] = float(y[p])
    return feats

def run_features_dir(input_dir: Path, output_path: Path, method: str, prominence: float, distance: int, topk: int, downsample: int):
    rows = []
    emb_dim = None
    for p in sorted(input_dir.glob("*.parquet")):
        df = pd.read_parquet(p)
        if method == "physics":
            feats = extract_features_physics(df, prominence=prominence, distance=distance, topk=topk)
        elif method == "tfug":
            emb = TFUGFWTEmbedder(TFUGFWTConfig(downsample=downsample)).transform(df)
            if emb_dim is None:
                emb_dim = len(emb)
            feats = {f"emb_{i}": float(v) for i, v in enumerate(emb)}
        else:
            raise ValueError("Unknown method")
        feats["file"] = p.name
        rows.append(feats)
    out_df = pd.DataFrame(rows)
    if output_path.suffix.lower() == ".csv":
        out_df.to_csv(output_path, index=False)
    else:
        out_df.to_parquet(output_path, index=False)
    return out_df

@main.command("features")
@click.option("--input", "input_dir", type=click.Path(path_type=Path), required=True, help="Dossier contenant des .parquet (wavenumber_cm1,intensity,...)")
@click.option("--output", "output_path", type=click.Path(path_type=Path), required=True, help="Fichier de sortie (.parquet ou .csv)")
@click.option("--method", type=click.Choice(["physics","tfug"], case_sensitive=False), default="physics")
@click.option("--prominence", type=float, default=0.01, help="Prominence minimale (physics)")
@click.option("--distance", type=int, default=5, help="Distance minimale entre pics (physics)")
@click.option("--topk", type=int, default=5, help="Nombre max de pics à reporter (physics)")
@click.option("--downsample", type=int, default=64, help="Taille cible de l'embedding (tfug)")
def features_cmd(input_dir: Path, output_path: Path, method: str, prominence: float, distance: int, topk: int, downsample: int):
    """Extraire des features d'un dossier de .parquet (méthodes: physics|tfug)."""
    try:
        df = run_features_dir(input_dir, output_path, method.lower(), prominence, distance, topk, downsample)
        click.echo(f"[OK] Features écrites -> {output_path} ({len(df)} lignes)")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == "__main__":
    main()
