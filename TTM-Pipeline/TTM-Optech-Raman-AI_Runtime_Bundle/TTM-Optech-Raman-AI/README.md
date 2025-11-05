
# Optech Raman AI

Pipeline reproductible pour spectroscopie Raman :
- Format **Parquet** + schéma canonique
- Prétraitement vectorisé (spikes, baseline, normalisation, alignement, lissage)
- Featurisation hybride (pics, ratios, **FWT/TFUG** placeholder)
- Tête **bayésienne** multi-sorties (architecture extensible)
- **DVC** stages + **CLI** (`raman`)
- Rapport IEEE auto (LaTeX, TikZ/PGF)

> Généré le 2025-11-04T16:13:07.447338Z

## Installation (dev)

```
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -e .
```

## Commandes clés

```
raman prep   --in data/raw --out data/parquet --align --baseline asls --norm snv --smooth sg
raman feats  --in data/parquet --out data/features --fwt --df --peaks voigt --ratios default
raman train  --feats data/features --model conv1d_bayes --cv 5 --seed 42
raman eval   --feats data/features --model models/conv1d_bayes.pt --uncertainty
raman report --metrics reports/metrics.json --latex templates/ieee/main.tex --out reports/paper.pdf
```

## Arborescence

```
optech-raman-ai/
  src/raman_ai/...
  data/{{raw, parquet, features, models, reports}}
  dvc.yaml
  params.yaml
  tests/
```

## Notes
- Les modules **FWT/TFUG** sont fournis en *squelette* pour brancher vos implémentations (ou packages internes).
- **Torch** et **DVC** sont laissés en option pour éviter un lock d'environnement ici.


## Quickstart

```bash
pip install -e .[dev,test]
# 1) Convert to parquet
raman-ai to-parquet --params params.yaml
# 2) Preprocess
raman-ai preprocess --params params.yaml
# 3) Features
raman-ai features --params params.yaml
# 4) Train
raman-ai train --params params.yaml
# 5) Evaluate
raman-ai evaluate --params params.yaml
# 6) Report
raman-ai report --params params.yaml
```


## Added (auto)
- Standards library in `data/standards` with Si/PS/PTFE/Al2O3 placeholders.
- Bayesian multi-output head with predictive uncertainties: `raman_ai.models.heads.bayes_multi`.
- Uncertainty calibration utilities: `raman_ai.eval.calibration`.
- Plot utilities for spectra & calibration: `raman_ai.report.plots`.
- CLI commands: `train_bayes`, `inject_figs`, `list_standards`.
- Make targets: `make train_bayes`, `make figs`, `make standards`.
- LaTeX auto-include figures via `plots/figures.tex`.
- DVC stages: `features`, `train_bayes`, `evaluate` (appended).
(Generated on 2025-11-04T16:33:40.233004Z)


## Added (calibration & templates) — 2025-11-04T16:50:07.444496Z
- `data/standards/real_templates/` avec CSV vides et README explicatif.
- Calibration **isotonique** sans dépendances externes: `isotonic_sigma_mapping()`.
- CLI: `run_temp_scaling_demo`, `run_isotonic_calibration_demo` (démos non destructives).
- DVC stage `ablation` (exécute la démo de calibration pour CI).


## Added (stable CLI & contracts) — 2025-11-04T16:56:39.441466Z
- CLI stable: preprocess, features, train, calibrate, evaluate, report.
- Make targets: preprocess/features/train/calibrate/evaluate/report/paper.
- DVC stage `calibrate` (isotonic by défaut).
- Pydantic contracts optionnels pour `io/schema.py` (si pydantic dispo).
- Calibration table generator: `raman_ai.report.calib_table.write_calibration_table`.
