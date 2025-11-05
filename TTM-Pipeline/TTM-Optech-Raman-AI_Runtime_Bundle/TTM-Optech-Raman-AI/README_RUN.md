# Runtime Quickstart (2025-11-04T17:17:02.365100Z)

## Local (venv)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Notebooks (prétraitement → featurisation → modélisation → report)
jupyter lab notebooks/

# Entraînement sur features réels
python -m raman_ai.cli train --features ./data/features.parquet --alpha 1.3 --beta 25.0

# Calibration + table LaTeX
python -m raman_ai.cli calibrate --method isotonic --quantiles 15

# Injection figures/tables dans le PDF IEEE
python -m raman_ai.cli report
```

## Docker (CPU)
```bash
docker build -t optech-raman-ai:cpu .

# Exemple: train + calibrate + report
docker run --rm -v $PWD:/app optech-raman-ai:cpu python -m raman_ai.cli train --features ./data/features.parquet --alpha 1.3 --beta 25.0
docker run --rm -v $PWD:/app optech-raman-ai:cpu python -m raman_ai.cli calibrate --method isotonic --quantiles 15
docker run --rm -v $PWD:/app optech-raman-ai:cpu python -m raman_ai.cli report
```

### Notes
- `data/standards/real_templates/` peut contenir vos étalons réels (`*.csv` + `*.meta.json` optionnel).
- Les notebooks 01→04 documentent et valident chaque étape.
- `dvc.yaml` et `Makefile` orchestrent le pipeline de bout en bout.
