# Optech Raman AI — Suite pédagogique & pipeline

**Date:** 2025-11-04T17:48:02

Ce bundle contient :
- `notebooks/`: 10 notebooks pédagogiques (structure, données, prétraitement, features, modélisation bayésienne, CLI, tests, DVC, logging, profiling).
- `latex/`: modèle LaTeX minimal (Overleaf-ready) avec `main.tex` et `references.bib`.
- `pipeline/`: squelettes `dvc.yaml`, `params.yaml` et un script `report_gen.py` pour agréger des métriques JSON.
- `runs/`: dossier prévu pour stocker des `*_metrics.json`.
- `examples/`: petits jeux de données CSV synthétiques pour démarrer.

## Installation locale rapide
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
# Optionnel: DVC si désiré
pip install dvc
```

## Lancement notebooks
```bash
jupyter notebook
# puis ouvrir notebooks/*.ipynb
```

## Données & pipeline
- Place tes fichiers bruts dans `data/raw/` (ou `examples/` pour tester).
- Exécute la conversion CSV→Parquet via notebook `01` ou ta CLI.
- Le pipeline de prétraitement et features est documenté dans `02` & `03`.

## DVC (optionnel)
```bash
dvc init
dvc repro
```
Le graphe minimal est dans `pipeline/dvc.yaml`. Modifie `pipeline/params.yaml` pour ajuster les hyperparamètres (fenêtre Savitzky–Golay, lambda ALS, etc.).

## Reporting LaTeX
- Les métriques agrégées (`runs/*_metrics.json`) peuvent être converties en tableaux LaTeX via `pipeline/report_gen.py`.
- Compiler `latex/main.tex` localement (`latexmk`) ou sur Overleaf (charger le dossier `latex/`).

## Qualité & releases
- Tests: `pytest -q`
- Formatage: `black .` ; Lint: `flake8`
- Versioning sémantique: tags Git → changelog → wheel (à brancher sur CI).
