# Calibration_Raman_Waterkit (FR)
Généré le 2025-11-04

Contenu:
- `data_templates/`: modèles CSV (étalons aqueux et solides) + exemples synthétiques.
- `notebooks/Calibration_Raman_Waterkit.ipynb`: pipeline de calibration prêt à exécuter (NumPy pur).
- `scripts/raman_cal_helpers.py`: fonctions utilitaires (lissage, baseline poly, intégration de bandes, centroïde, FWHM).
- `figures/`: résultats/exports.

Usage rapide:
1. Duplique les CSV `*_template.csv` et remplis-les avec tes données (colonne `concentration_mM` si applicable).
2. Ouvre le notebook, choisis les fenêtres de bandes et exécute les cellules.
3. Le notebook calcule aires, centroïdes, FWHM et ajuste une droite (aire vs concentration).
