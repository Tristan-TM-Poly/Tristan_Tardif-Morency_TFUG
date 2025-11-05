"""
batch_preprocess.py — Raman AI Batch Preprocessing & Fractal Database Builder (Optech)
-------------------------------------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Automate preprocessing (Blocs 1–9) and create compact HDF5 database.

Pipeline:
    1. Load all spectra (.csv, .txt, .npy)
    2. Run RamanPreprocessPipeline
    3. Apply SpectrumCompressor
    4. Save results in FractalDB.h5
    5. Export global QC summary
"""

import os
import numpy as np
import pandas as pd
import h5py
from pathlib import Path
from tqdm import tqdm

# Modules internes
from raman_preprocess_pipeline import RamanPreprocessPipeline
from compress_spectrum import SpectrumCompressor


# -------------------------------------------------------------------------
# 🔹 1. Chargement automatique des fichiers
# -------------------------------------------------------------------------
def load_spectrum(file_path):
    """
    Load a Raman spectrum from .csv, .txt, or .npy.
    Must contain two columns: Raman shift (cm⁻¹) and Intensity.
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".npy":
        data = np.load(file_path)
        x, y = data[:, 0], data[:, 1]
    else:
        df = pd.read_csv(file_path, sep=None, engine="python", header=None)
        if df.shape[1] < 2:
            raise ValueError(f"Invalid file format: {file_path}")
        x, y = df.iloc[:, 0].values, df.iloc[:, 1].values
    return x, y


# -------------------------------------------------------------------------
# 🔹 2. Fonction principale de traitement de dossier
# -------------------------------------------------------------------------
def process_batch(
    input_dir="spectra_raw",
    output_file="FractalDB.h5",
    qc_dir="qc_reports",
    config=None,
    compression=True
):
    """
    Process all Raman spectra in folder and build fractal database.

    Parameters
    ----------
    input_dir : str
        Folder containing raw spectra (.csv, .txt, .npy)
    output_file : str
        HDF5 output file
    qc_dir : str
        Folder for QC reports
    config : dict
        Pipeline configuration
    compression : bool
        Apply physical fractal compression
    """
    # Initialisation
    input_dir = Path(input_dir)
    spectra_files = sorted(input_dir.glob("*.csv")) + sorted(input_dir.glob("*.txt")) + sorted(input_dir.glob("*.npy"))
    if len(spectra_files) == 0:
        raise FileNotFoundError(f"Aucun fichier détecté dans {input_dir}")

    pipeline = RamanPreprocessPipeline(config)
    compressor = SpectrumCompressor() if compression else None

    # Création base de données
    h5_path = Path(output_file)
    if h5_path.exists():
        h5_path.unlink()  # Écrase l’ancienne version
    h5 = h5py.File(h5_path, "w")

    # Groupes HDF5
    g_raw = h5.create_group("raw")
    g_proc = h5.create_group("processed")
    g_comp = h5.create_group("compressed")
    g_qc = h5.create_group("qc")

    qc_summary = []

    # Boucle principale
    for file in tqdm(spectra_files, desc="Traitement des spectres Raman"):
        sample_id = Path(file).stem
        try:
            x, y = load_spectrum(file)
            results = pipeline.run(sample_id, x, y)

            # Sauvegarde brute et prétraitée
            g_raw.create_dataset(sample_id, data=np.column_stack((x, y)))
            g_proc.create_dataset(sample_id, data=np.column_stack((results["x_proc"], results["y_proc"])))

            # Compression fractale
            if compression:
                comp_data = compressor.compress(results["x_proc"], results["y_proc"])
                g_comp.create_dataset(sample_id, data=np.string_(str(comp_data)))

            # QC
            g_qc.create_dataset(sample_id, data=np.string_(str(results["qc_metrics"])))
            qc_summary.append({"sample": sample_id, **results["qc_metrics"]})

        except Exception as e:
            print(f"[Erreur] {sample_id} : {e}")
            continue

    # Résumé global QC
    df_qc = pd.DataFrame(qc_summary)
    df_qc.to_excel(Path(qc_dir) / "QC_summary.xlsx", index=False)

    h5.close()
    print(f"✅ FractalDB générée : {output_file}")
    print(f"✅ Résumé QC : {qc_dir}/QC_summary.xlsx")

    return output_file
