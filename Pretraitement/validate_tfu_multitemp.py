"""
validate_tfu_multitemp.py — Multi-temperature TFU–Raman validation
-------------------------------------------------------------------
Author : Tristan Tardif-Morency
Purpose: Run TFU validation for several measured spectra (300–1500 K),
         compute Df(T), R²(T), RMS(T), and generate summary plots.
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from validate_tfu_experiment import validate_experiment

def validate_multitemp(
    material: str,
    spectra_dir: str = "spectres_mesures",
    temps: list = None,
    Df_guess: float = 1.0,
    lam: float = 0.8,
    out_dir: str = "validation_reports"
):
    """
    Run validation for all available temperature files.
    Expected filenames: <material>_<T>K.csv
    """
    temps = temps or [300, 600, 900, 1200, 1500]
    results = []

    for T in temps:
        file = Path(spectra_dir) / f"{material}_{T}K.csv"
        if not file.exists():
            print(f"[⚠️] Fichier manquant : {file.name}")
            continue

        print(f"--- Validation {material} @ {T} K ---")
        res = validate_experiment(
            material=material,
            measured_file=str(file),
            T=T,
            Df_guess=Df_guess,
            lam=lam,
            out_dir=out_dir
        )
        res["T"] = T
        results.append(res)

    if not results:
        print("Aucune donnée traitée.")
        return None

    df_summary = pd.DataFrame(results)
    csv_path = Path(out_dir) / f"{material}_TFU_summary.csv"
    df_summary.to_csv(csv_path, index=False)

    # --- Graphiques synthèse ---
    plt.figure(figsize=(9,5))
    plt.subplot(3,1,1)
    plt.plot(df_summary["T"], df_summary["R2"], "o-", label="R²")
    plt.ylabel("R²"); plt.grid(True)

    plt.subplot(3,1,2)
    plt.plot(df_summary["T"], df_summary["RMS"], "o-", label="RMS", color="orange")
    plt.ylabel("RMS"); plt.grid(True)

    plt.subplot(3,1,3)
    plt.plot(df_summary["T"], df_summary["Df_mean"], "o-", label="Df moyen", color="green")
    plt.xlabel("Température (K)")
    plt.ylabel("Df moyen"); plt.grid(True)

    plt.tight_layout()
    fig_path = Path(out_dir) / f"{material}_TFU_summary.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()

    print(f"✅ Validation multi-températures terminée.")
    print(f"→ Résumé : {csv_path}")
    print(f"→ Graphique : {fig_path}")
    return df_summary
