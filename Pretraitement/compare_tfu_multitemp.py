"""
compare_tfu_multitemp.py — Superposition multi-T exp vs modèle TFU
-------------------------------------------------------------------
Author : Tristan Tardif-Morency
Purpose: Plot all measured spectra vs TFU-model spectra on one figure,
         showing how accuracy and Df evolve with temperature.
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from raman_materials_full import generate_full_spectrum
from raman_preprocess_pipeline import RamanPreprocessPipeline
from validate_tfu_experiment import r2_score, rms_error


def compare_tfu_multitemp(
    material: str,
    spectra_dir: str = "spectres_mesures",
    temps: list = None,
    Df_guess: float = 1.0,
    lam: float = 0.8,
    out_dir: str = "validation_reports"
):
    out_dir = Path(out_dir); out_dir.mkdir(exist_ok=True)
    temps = temps or [300, 600, 900, 1200, 1500]
    plt.figure(figsize=(10, 6))

    cmap = plt.get_cmap("plasma", len(temps))
    summary = []

    for i, T in enumerate(temps):
        file = Path(spectra_dir) / f"{material}_{T}K.csv"
        if not file.exists():
            print(f"[⚠️] Fichier manquant : {file.name}")
            continue

        # Charger et prétraiter
        df = pd.read_csv(file, sep=None, engine="python", header=None)
        nu, I_exp = df.iloc[:, 0].values, df.iloc[:, 1].values
        I_exp /= np.max(I_exp)

        # Modèle TFU
        I_mod = generate_full_spectrum(material, nu, Df=Df_guess, lam=lam, T=T)
        I_mod /= np.max(I_mod)

        # Métriques
        R2 = r2_score(I_exp, I_mod)
        RMS = np.sqrt(np.mean((I_exp - I_mod) ** 2))
        summary.append({"T": T, "R2": R2, "RMS": RMS})

        # Tracé superposé
        plt.plot(nu, I_exp + i*1.1, label=f"{T} K exp", color=cmap(i))
        plt.plot(nu, I_mod + i*1.1, "--", color=cmap(i))

    plt.xlabel("Raman shift (cm⁻¹)")
    plt.ylabel("Intensité (offset par T)")
    plt.title(f"{material} — Spectres expérimentaux vs modèle TFU")
    plt.legend(fontsize=7, ncol=2)
    plt.tight_layout()

    fig_path = out_dir / f"{material}_TFU_compare_multiT.png"
    plt.savefig(fig_path, dpi=350)
    plt.close()

    df_sum = pd.DataFrame(summary)
    csv_path = out_dir / f"{material}_TFU_compare_multiT.csv"
    df_sum.to_csv(csv_path, index=False)

    print(f"✅ Comparaison multi-T complétée → {fig_path}")
    return df_sum
