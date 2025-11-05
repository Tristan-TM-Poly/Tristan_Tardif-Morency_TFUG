"""
validate_tfu_experiment.py — Validation expérimentale du modèle Raman/TFU
--------------------------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Optech / TFU Validation
Purpose: Compare measured spectra with TFU-analytical model,
         extract invariants, and generate a PDF + Excel report.
"""

import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress
from fpdf import FPDF

# blocs précédents
from raman_preprocess_pipeline import RamanPreprocessPipeline
from raman_invariants import extract_invariants
from raman_materials_full import generate_full_spectrum


# -------------------------------------------------------------------------
# 🔹 1. Fonctions auxiliaires
# -------------------------------------------------------------------------
def r2_score(y_exp, y_mod):
    ss_res = np.sum((y_exp - y_mod) ** 2)
    ss_tot = np.sum((y_exp - np.mean(y_exp)) ** 2)
    return 1 - ss_res / ss_tot

def rms_error(y_exp, y_mod):
    return np.sqrt(np.mean((y_exp - y_mod) ** 2))


# -------------------------------------------------------------------------
# 🔹 2. Fonction principale de validation
# -------------------------------------------------------------------------
def validate_experiment(
    material: str,
    measured_file: str,
    T: float = 300,
    Df_guess: float = 1.0,
    lam: float = 1.0,
    out_dir: str = "validation_reports",
):
    """
    Compare un spectre mesuré au modèle TFU-Raman.
    """
    out_dir = Path(out_dir); out_dir.mkdir(exist_ok=True)

    # 1️⃣ Charger spectre mesuré
    df = pd.read_csv(measured_file, sep=None, engine="python", header=None)
    nu, I_exp = df.iloc[:, 0].values, df.iloc[:, 1].values

    # 2️⃣ Générer modèle analytique
    I_mod = generate_full_spectrum(material, nu, Df=Df_guess, lam=lam, T=T)

    # 3️⃣ Normalisation
    I_exp /= np.max(I_exp); I_mod /= np.max(I_mod)

    # 4️⃣ Calcul métriques
    R2 = r2_score(I_exp, I_mod)
    RMS = rms_error(I_exp, I_mod)
    slope, intercept, r, p, se = linregress(I_mod, I_exp)

    # 5️⃣ Extraction invariants et estimation Df réel
    df_inv = extract_invariants(nu, I_exp, T=T)
    Df_mean = np.mean(df_inv["Df_est"]) if len(df_inv) else np.nan

    # 6️⃣ Figure comparative
    plt.figure(figsize=(10,5))
    plt.plot(nu, I_exp, label="Mesuré")
    plt.plot(nu, I_mod, label=f"Modèle TFU (Df={Df_guess:.2f})", linewidth=1.8)
    plt.xlabel("Raman shift (cm⁻¹)"); plt.ylabel("Intensité (normalisée)")
    plt.legend(); plt.tight_layout()
    fig_path = out_dir / f"{material}_TFU_validation_{int(T)}K.png"
    plt.savefig(fig_path, dpi=300); plt.close()

    # 7️⃣ Génération PDF simple
    pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Validation TFU – {material} @ {T} K", ln=True)
    pdf.multi_cell(0, 8,
        f"R² = {R2:.4f}\nRMS = {RMS:.5f}\n"
        f"Slope = {slope:.3f}, Intercept = {intercept:.3f}\n"
        f"Df (moyen estimé) = {Df_mean:.3f}\n"
        f"Fichier mesuré : {Path(measured_file).name}")
    pdf.image(str(fig_path), w=180)
    pdf_path = out_dir / f"{material}_TFU_validation_{int(T)}K.pdf"
    pdf.output(str(pdf_path))

    # 8️⃣ Export Excel
    df_inv.to_excel(out_dir / f"{material}_invariants_{int(T)}K.xlsx", index=False)

    print("✅ Validation TFU complétée :")
    print(f"R² = {R2:.4f}  |  RMS = {RMS:.5f}  |  Df ≈ {Df_mean:.3f}")
    print("Rapports :")
    print("  →", pdf_path)
    print("  →", fig_path)

    return {
        "R2": R2, "RMS": RMS, "Df_mean": Df_mean,
        "pdf": str(pdf_path), "figure": str(fig_path)
    }
