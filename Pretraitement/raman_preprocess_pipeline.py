"""
raman_preprocess_pipeline.py — Raman AI Preprocessing Master Module (Optech)
----------------------------------------------------------------------------
Author : Tristan Tardif-Morency
Project: Raman AI – Fractal Calibration Pipeline (Optech 2025)
Purpose: Unified preprocessing pipeline integrating all Raman modules.

Pipeline steps:
1. NoiseFilter
2. BaselineCorrector
3. Calibrator
4. Normalizer
5. Resampler
6. Derivator
7. QCReporter
"""

import numpy as np
from pathlib import Path

# Importation des modules internes
from noise_filter import NoiseFilter
from baseline_correction import BaselineCorrector
from calibration import Calibrator
from normalize import Normalizer
from resample import Resampler
from derivative import Derivator
from qc_report import QCReporter


# -------------------------------------------------------------------------
# 🔹 Classe principale du pipeline
# -------------------------------------------------------------------------
class RamanPreprocessPipeline:
    """
    Complete Raman preprocessing pipeline for Optech Raman AI system.
    """

    def __init__(self, config=None):
        """
        Parameters
        ----------
        config : dict or None
            Optional configuration dictionary controlling parameters for all blocks.
        """
        cfg = config or {}

        # 1️⃣ Nettoyage
        self.noise = NoiseFilter(**cfg.get("noise", {}))

        # 2️⃣ Baseline
        self.baseline = BaselineCorrector(**cfg.get("baseline", {}))

        # 3️⃣ Calibration
        self.calib = Calibrator(**cfg.get("calib", {}))

        # 4️⃣ Normalisation
        self.norm = Normalizer(**cfg.get("norm", {}))

        # 5️⃣ Ré-échantillonnage
        self.resample = Resampler(**cfg.get("resample", {}))

        # 6️⃣ Dérivation
        self.deriv = Derivator(**cfg.get("deriv", {}))

        # 7️⃣ QC
        self.qc = QCReporter(**cfg.get("qc", {}))

        # Dossier de sortie QC
        self.out_dir = Path(cfg.get("out_dir", "qc_reports"))
        self.out_dir.mkdir(exist_ok=True)

    # ---------------------------------------------------------------
    def run(self, sample_id, x, y):
        """
        Execute full preprocessing pipeline on one spectrum.

        Parameters
        ----------
        sample_id : str
            Name or ID of the sample.
        x : np.ndarray
            Raman shift axis (cm⁻¹)
        y : np.ndarray
            Raw intensity vector.

        Returns
        -------
        results : dict
            Dictionary with processed data and QC metrics.
        """

        # Step 1 – Noise removal
        x1, y1 = self.noise.apply(x, y)

        # Step 2 – Baseline correction
        x2, y2, baseline = self.baseline.apply(x1, y1)

        # Step 3 – Calibration
        x3, y3, coeffs = self.calib.apply(x2, y2)

        # Step 4 – Normalization
        x4, y4 = self.norm.apply(x3, y3)

        # Step 5 – Resampling
        x5, y5 = self.resample.apply(x4, y4)

        # Step 6 – Derivative
        x6, y6 = self.deriv.apply(x5, y5)

        # Step 7 – Quality Control
        metrics = self.qc.evaluate(x5, y3, y5)
        pdf, xlsx = self.qc.generate_report(sample_id, x5, y3, y5, metrics)

        # Return structured results
        return {
            "sample_id": sample_id,
            "x_raw": x,
            "y_raw": y,
            "x_proc": x6,
            "y_proc": y6,
            "baseline": baseline,
            "calib_coeffs": coeffs,
            "qc_metrics": metrics,
            "qc_report_pdf": pdf,
            "qc_report_xlsx": xlsx
        }
