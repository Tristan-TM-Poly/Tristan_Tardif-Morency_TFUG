
import argparse, os, json, numpy as np, importlib

from .models.train import train_bayesian_multioutput
from .report.gen_latex import inject_figures
from .io.standards import load_reference_spectra_mode
from .eval.calibration import interval_coverage, ece_regression, isotonic_sigma_mapping
from .report.calib_table import write_calibration_table

PROJ_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..')

def _synth_data(seed=7, N=256, D=24, K=4):
    np.random.seed(seed)
    X = np.random.randn(N, D)
    W = np.random.randn(D, K)
    Y = X @ W + 0.12*np.random.randn(N, K)
    return X, Y

def _load_val_true(seed=7):
    X, Y = _synth_data(seed=seed)
    return Y[200:]

def _call_if_exists(modpath, fn_names=('main','run','pipeline')):
    try:
        mod = importlib.import_module(modpath)
    except Exception as e:
        print(f"[warn] Cannot import {modpath}: {e}")
        return False
    for fn in fn_names:
        if hasattr(mod, fn) and callable(getattr(mod, fn)):
            try:
                getattr(mod, fn)()
                return True
            except TypeError:
                try:
                    getattr(mod, fn)(PROJ_ROOT)
                    return True
                except Exception as e:
                    print(f"[warn] {modpath}.{fn} failed: {e}")
                    continue
    print(f"[warn] No callable {fn_names} found in {modpath}")
    return False

def cmd_preprocess(args):
    ok = _call_if_exists('raman_ai.preprocess.pipeline')
    if not ok:
        print("preprocess: stub executed (wire raman_ai.preprocess.pipeline.{main|run|pipeline} to enable).")

def cmd_features(args):
    os.environ['RAMAN_STANDARDS_MODE'] = args.standards
    ok = _call_if_exists('raman_ai.features.pipeline')
    if not ok:
        print("features: stub executed (wire raman_ai.features.pipeline.{main|run|pipeline} to enable).")

def _split_xy_from_features(path):
    import pandas as pd, numpy as np
    df = pd.read_parquet(path)
    # Heuristics: targets are columns starting with 'target_'
    ycols = [c for c in df.columns if c.startswith('target_')]
    if ycols:
        Y = df[ycols].values.astype(float)
        X = df.drop(columns=ycols).select_dtypes(include=[float,int]).values.astype(float)
        return X, Y
    # else, synthesize Y via a random linear map for demo reproducibility
    X = df.select_dtypes(include=[float,int]).values.astype(float)
    if X.size == 0:
        raise ValueError('No numeric columns found in features parquet')
    rng = np.random.default_rng(7)
    K = min(4, max(1, X.shape[1]//8))
    W = rng.normal(size=(X.shape[1], K))
    Y = X @ W + 0.12*rng.normal(size=(X.shape[0], K))
    return X, Y

def cmd_train(args):
    if args.features:
        X, Y = _split_xy_from_features(args.features)
        n = X.shape[0]
        i = max(1, int(n*0.78))
        out = train_bayesian_multioutput(X[:i], Y[:i], X_val=X[i:], Y_val=Y[i:], alpha=args.alpha, beta=args.beta)
    else:
        X, Y = _synth_data()
        out = train_bayesian_multioutput(X[:200], Y[:200], X_val=X[200:], Y_val=Y[200:], alpha=args.alpha, beta=args.beta)
    print(out)

def cmd_calibrate(args):
    pred_path = os.path.join(PROJ_ROOT, 'models', 'bayes_multi', 'val_pred.json')
    with open(pred_path, 'r') as fh:
        pred = json.load(fh)
    mu = np.array(pred['mu']); std = np.array(pred['std'])
    Y_val = _load_val_true()

    if args.method == "isotonic":
        f = isotonic_sigma_mapping(Y_val, mu, std, n_quantiles=args.quantiles)
        std_cal = f(std)
    else:
        targets = (0.5,0.8,0.9,0.95)
        def coverage_loss(scale):
            mu_f = mu.flatten(); std_f = (std*scale).flatten(); y_f = Y_val.flatten()
            covs = [interval_coverage(y_f, mu_f, std_f, conf=t).empirical for t in targets]
            return float(np.mean((np.array(covs) - np.array(targets))**2))
        grid = np.linspace(0.3, 3.0, 108)
        losses = [coverage_loss(s) for s in grid]
        best = grid[int(np.argmin(losses))]
        std_cal = std * best

    nominals = [0.5,0.8,0.9,0.95]
    covers = [interval_coverage(Y_val.flatten(), mu.flatten(), std_cal.flatten(), conf=t).empirical for t in nominals]
    ece = ece_regression(Y_val.flatten(), mu.flatten(), std_cal.flatten(), n_bins=12)

    metrics_path = os.path.join(PROJ_ROOT, 'metrics', 'summary.json')
    os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
    blob = {"calibration": {"method": args.method, "nominal": nominals, "empirical": covers, "ece": float(ece)}}
    if os.path.isfile(metrics_path):
        with open(metrics_path, 'r') as fh:
            cur = json.load(fh)
    else:
        cur = {}
    cur.update(blob)
    with open(metrics_path, 'w') as fh:
        json.dump(cur, fh, indent=2)

    calib_table_tex = os.path.join(PROJ_ROOT, 'plots', 'calibration_table.tex')
    write_calibration_table(metrics_path, calib_table_tex)
    print(blob)

def cmd_evaluate(args):
    metrics_path = os.path.join(PROJ_ROOT, 'metrics', 'summary.json')
    print(metrics_path)

def cmd_report(args):
    plot_dir = os.path.join(PROJ_ROOT, 'plots')
    print(inject_figures(fig_dir=plot_dir))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--standards", choices=["synthetic","real"], default="synthetic", help="Choix des étalons")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("preprocess")
    sp.set_defaults(func=cmd_preprocess)

    sf = sub.add_parser("features")
    sf.set_defaults(func=cmd_features)

    st = sub.add_parser("train")
    st.add_argument("--alpha", type=float, default=1.0)
    st.add_argument("--beta", type=float, default=25.0)
    st.add_argument("--features", type=str, default=None, help="Path to features.parquet (optional)")
    st.set_defaults(func=cmd_train)

    sc = sub.add_parser("calibrate")
    sc.add_argument("--method", choices=["temp","isotonic"], default="isotonic")
    sc.add_argument("--quantiles", type=int, default=15)
    sc.set_defaults(func=cmd_calibrate)

    se = sub.add_parser("evaluate")
    se.set_defaults(func=cmd_evaluate)

    sr = sub.add_parser("report")
    sr.set_defaults(func=cmd_report)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
