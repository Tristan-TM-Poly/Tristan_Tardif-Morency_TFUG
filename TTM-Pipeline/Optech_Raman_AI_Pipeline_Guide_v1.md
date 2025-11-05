# Optech Raman AI — Pipeline Guide (v7, slim)  
_Date: 2025-11-04_

This document explains **in depth** how the Optech Raman AI pipeline is structured and how each component works — from raw data to a LaTeX‑ready PDF report. It covers **data model**, **algorithms**, **configuration**, **CLI**, **parallelization**, **QA**, **notebooks**, **testing**, **performance**, and **extensions** (TFUG FWT). Everything here is aligned with the **v7 slim** bundle you have.

---

## 1) Big‑Picture Overview

**Goal:** Turn raw/sanitized Raman spectra into **cleaned signals**, **features** (physics or TFUG embeddings), **visuals**, **QA summaries**, and an **auto‑compiled LaTeX PDF** — with a **single command**.

**Single command (zero‑flag by default):**
```bash
optech-raman-ai report
# reads pipeline/params.yaml and runs:
# preprocess → features → QA → plot → LaTeX tables+gallery → (optional) PDF compile
```
This defaults to the unified configuration in `pipeline/params.yaml`. You can override parallelism on the fly:
```bash
optech-raman-ai report --n-jobs 8
```

**Key stages:**
1. **Preprocess**: Savitzky–Golay smoothing → ALS baseline removal → area normalization.  
2. **Features**: 
   - **Physics**: peaks + statistics (n_peaks, area, y_mean, y_std, top‑K peaks positions/heights).  
   - **TFUG**: embedding via TFUG FWT (**stub** now; replace with the real implementation).
3. **QA**: SNR, area, peak‑count thresholds → `latex/qa_summary.csv` (+ boolean pass/fail per sample).
4. **Plot**: PNG figures with **peak markers** for each spectrum (gallery).
5. **Report**: auto‑generate LaTeX tables (`metrics_table.tex`, `fig_gallery.tex`) and **optional auto‑PDF** (`latex/main.pdf`).

---

## 2) Repository Layout (what matters)

```
Optech_Raman_AI_Bundle/
├── pipeline/
│   ├── params.yaml                  # unified config: preprocess, features, report
│   └── report_gen.py                # LaTeX table & gallery generation
├── src/optech_raman_ai/
│   ├── cli.py                       # CLI entrypoints (convert, dedup, preprocess, features, plot, report)
│   ├── pipelines/preprocess.py      # PreprocessParams, preprocess_df, load_params_yaml
│   ├── features/fwt_tfug.py         # TFUGFWTEmbedder (stub) + config
│   ├── features/physics.py          # features_physics (peaks + stats)
│   ├── plotting/plot_spectra.py     # plot_folder(), peak markers, PNG export
│   └── utils/
│       ├── schema.py                # validate_schema()
│       └── qa.py                    # qa_row(), snr_basic(), area_under_curve()
├── latex/
│   ├── main.tex                     # includes metrics_table.tex + fig_gallery.tex
│   ├── metrics_table.tex            # auto-generated
│   ├── fig_gallery.tex              # auto-generated
│   └── (main.pdf)                   # auto-compiled if enabled
├── notebooks/
│   ├── 00_Quickstart.ipynb
│   ├── 02_Preprocess.ipynb
│   ├── 03_Features.ipynb
│   └── 10_End_to_End_Report.ipynb   # end-to-end demo (imports from .py)
├── tests/                           # unit + e2e tests
├── Makefile                         # setup/report/test/pdf shortcuts
├── pyproject.toml                   # optional dependencies groups ([project.optional-dependencies])
└── requirements.txt                 # minimal run deps (pandas, numpy, scipy, pyarrow, click, joblib, matplotlib, pyyaml)
```

---

## 3) Data Model & Contracts

**Input Parquet schema** (validated early by `utils/schema.py`):
- `wavenumber_cm1: float`  — X‑axis (Raman shift).
- `intensity: float`       — Y‑axis (signal).
- `sample_id: string`      — optional, coerced to string if present.

Why **Parquet**? Columnar, fast IO, typed schema, compressed. All pipeline stages assume **one spectrum per file**.

---

## 4) Configuration (`pipeline/params.yaml`)

Example (v7 defaults):
```yaml
preprocess:
  savgol_window: 21        # must be odd; smoothing window
  savgol_poly: 3
  als_lambda: 1.0e5        # baseline ALS smoothness
  als_p: 0.01              # baseline asymmetry parameter
  area_norm: true          # area = ~1 post-normalization
  input_dir: data/processed
  output_dir: data/clean

features:
  method: physics          # physics | tfug
  prominence: 0.02         # peak detection (physics)
  distance: 5              # min distance between peaks (physics)
  topk: 5                  # number of peaks to log (physics)
  downsample: 64           # embedding size (tfug)
  input_dir: data/clean
  output_path: data/features/features.parquet

report:
  fig_dir: figures
  latex_dir: latex
  runs_dir: runs
  n_jobs: -1               # -1 = all cores
  auto_pdf: true           # latexmk/pdflatex at the end
  qa:
    snr_min: 5.0
    area_min: 0.1
    peaks_min: 1
```

You can keep this file as the **single source of truth**. The CLI reads it by default. Specific flags only override selectively (e.g., `--n-jobs 8`).

---

## 5) Algorithms & Math

### 5.1 Preprocess (`pipelines/preprocess.py`)
Pipeline: **Savitzky–Golay smoothing** → **ALS baseline removal** → **area normalization**.

- **Savitzky–Golay**: local polynomial regression; preserves peak shapes vs. simple moving average.  
  Parameters: `savgol_window` (odd), `savgol_poly`.

- **ALS baseline** (Asymmetric Least Squares):  
  Minimizes \( \sum w_i (y_i - z_i)^2 + \lambda \sum (D^2 z)^2 \),  
  with iterative reweighting via asymmetry parameter \(p\) for baseline suppression.  
  - `als_lambda` controls smoothness of the baseline.
  - `als_p` controls asymmetry (fraction treated as peaks vs. baseline).

- **Area normalization**:  
  After baseline correction, area \( A = \int y_c(x) dx \) is scaled to ~1 to make spectra comparable across acquisitions.

**Outputs:** a new Parquet per input in `preprocess.output_dir` with normalized, baseline‑free intensity.

### 5.2 Features
- **Physics (`features/physics.py`)**:  
  Uses `scipy.signal.find_peaks(y, prominence, distance)` to detect peaks; records:
  - `n_peaks`, `y_mean`, `y_std`, `area`
  - `peak_i_pos`, `peak_i_height` for `i = 1..topk` (sorted by prominence).

- **TFUG (`features/fwt_tfug.py`)** (stub):  
  Provides a deterministic embedding of length `downsample`. Replace the body with your **real quaternionic TFUG/FWT** implementation and keep the **same interface** (`TFUGFWTEmbedder(TFUGFWTConfig).transform(df)`).

### 5.3 QA (`utils/qa.py`)
- **SNR** (robust): \( \text{SNR} = (\max(y) - \text{median}(y)) / (1.4826 \cdot \text{MAD}) \).
- **Area**: \( A = \int y(x) dx \) (post‑norm should be \(\approx 1\)).
- **Peak count**: after preprocessing, enforce `peaks_min` with same `prominence`/`distance` used in features.

**Output:** `latex/qa_summary.csv` with per‑file thresholds and `ok` flag.

---

## 6) CLI — What each command does

- `optech-raman-ai preprocess`  
  Batch‑applies the preprocess to a folder (you can still run it standalone if needed).

- `optech-raman-ai features`  
  Extracts features from a folder of preprocessed Parquets (physics or tfug).

- `optech-raman-ai plot`  
  Produces **PNG** with **peak markers** for each file; used by the report for a visual gallery.

- `optech-raman-ai report`  **← recommended**
  1) Reads `pipeline/params.yaml`.  
  2) Preprocess (parallel).  
  3) Features (parallel).  
  4) QA CSV.  
  5) Plots with peaks.  
  6) LaTeX tables & gallery.  
  7) **Optional** auto‑compile `latex/main.tex` → `latex/main.pdf`.

**Parallelization:** controlled by `report.n_jobs` (default `-1` for all cores). Override quickly:
```bash
optech-raman-ai report --n-jobs 12
```

---

## 7) LaTeX Outputs

- `latex/metrics_table.tex`: table summarizing metrics (derived from `runs/*_metrics.json`).  
- `latex/fig_gallery.tex`: a figure grid referencing all PNGs in `figures/`.  
- `latex/main.tex`: includes both `.tex` files and compiles to `latex/main.pdf` when `auto_pdf=true`.

You can customize the LaTeX template and styling as needed (`latex/main.tex`).

---

## 8) Notebooks — 4 Essentials

1. **`00_Quickstart.ipynb`** — install + `optech-raman-ai report` demo.  
2. **`02_Preprocess.ipynb`** — imports from `pipelines/preprocess.py`, shows intermediate signals.  
3. **`03_Features.ipynb`** — physics vs TFUG (stub), imports from `features/`.  
4. **`10_End_to_End_Report.ipynb`** — full run with imports (no hidden state).

All notebooks **import from `.py` modules** (no duplicated logic). With **Jupytext**, you can keep synchronized `.py` pairs for clean diffs.

---

## 9) Tests & Quality

- **Unit tests** for preprocess, features, CLI core.  
- **E2E** test for report (synthetic spectra → features/figures/LaTeX).  
Run:
```bash
make test
# or
pytest -q
```

**Static checks** (optional): `flake8`, `black` via `.[dev]` extra in `pyproject.toml`.

---

## 10) Performance & Scaling

- **Joblib**‐based parallelism for preprocess/features/QA.  
- I/O is columnar (Parquet) to reduce load and increase throughput.  
- Use `report.n_jobs: -1` to saturate cores or override with `--n-jobs`.  
- Reduce `downsample` for TFUG if embedding is heavy; tune `prominence/distance/topk` for physics.  
- Consider chunking folders for extremely large datasets.

---

## 11) Extending with Real TFUG FWT

Replace the stub in `features/fwt_tfug.py`:
- Keep `TFUGFWTConfig` fields (`downsample`, possibly add `basis`, `level`, etc.).
- Implement energy‑preserving transforms (quaternionic FWT) and derive a fixed‑length embedding.  
- Add **profiling** and **validation** vs. physics baselines (latency, accuracy, robustness).  
- Update tests (`tests/`) with goldens and tolerance bands per material (Si, PMMA, PS, metals).

---

## 12) Reproducibility & Determinism

- Ensure any TFUG randomness is seeded.  
- Logs and metrics are stored in `runs/` and LaTeX includes a **run ID** / timestamp.  
- Pin versions in `requirements.txt` / `pyproject.toml` for stable builds.

---

## 13) Troubleshooting

- **Missing LaTeX tools**: set `report.auto_pdf: false` or install `latexmk`/`pdflatex`.  
- **Empty PNGs / no peaks**: adjust `preprocess` (ALS/Savitzky–Golay) and `features.prominence/distance`.  
- **Weird areas**: check `area_norm` or raw input integrity; ensure wavenumbers are monotonic and in cm⁻¹.  
- **Schema errors**: make sure Parquets include `wavenumber_cm1` and `intensity` as numeric columns.

---

## 14) Daily Dev Shortcuts (Makefile)

```bash
make setup     # venv + install .[dev,viz] + dvc
make report    # full pipeline per params.yaml
make test      # pytest -q
make pdf       # latexmk -pdf latex/main.tex
```

---

## 15) Security & Data Handling

- Parquet files may embed sensitive sample metadata; keep only what you need.  
- Version large inputs externally (DVC/Git‑LFS) if needed, or mount read‑only volumes in production.

---

## 16) What to do Next (recommended)

1. **Wire the real TFUG FWT** into `features/fwt_tfug.py`.  
2. Add **real goldens** and stricter tests with **physics tolerances**.  
3. Enable **adaptive peak policies** per spectral band and material.  
4. Add a **LaTeX QA color table** page (red/yellow/green + PASS/FAIL badge).

---

**You can now run the whole pipeline with one command and produce a ready‑to‑share PDF.**  
Tune `pipeline/params.yaml`, drop new `.parquet` spectra in `data/processed`, and execute:

```bash
optech-raman-ai report
```

