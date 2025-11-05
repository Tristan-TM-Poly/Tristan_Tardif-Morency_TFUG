import argparse, os, json, numpy as np
from .models.train import train_bayesian_multioutput
from .report.gen_latex import inject_figures
from .io.standards import load_reference_spectra, load_reference_spectra_mode
from .eval.calibration import interval_coverage, ece_regression, isotonic_sigma_mapping

def cmd_preprocess(args):
    # placeholder to keep interface stable; real logic wired in pipeline.py
    print("preprocess: stub (wire to preprocess/pipeline.py as needed)")

def cmd_features(args):
    # placeholder: in real flow, call features/pipeline.py to produce data/features.parquet
    print("features: stub (wire to features/pipeline.py)")

def _synth_data(seed=7, N=256, D=24, K=4):
    np.random.seed(seed)
    X = np.random.randn(N, D)
    W = np.random.randn(D, K)
    Y = X @ W + 0.12*np.random.randn(N, K)
    return X, Y

def cmd_train(args):
    # For demo: use synthetic data unless --features points to real parquet
    X, Y = _synth_data()
    out = train_bayesian_multioutput(X[:200], Y[:200], X_val=X[200:], Y_val=Y[200:], alpha=args.alpha, beta=args.beta)
    print(out)

def _load_val_true(seed=7):
    X, Y = _synth_data(seed=seed)
    return Y[200:]

def cmd_calibrate(args):
    # Load predictions from previous train
    pred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', 'models', 'bayes_multi', 'val_pred.json')
    with open(pred_path, 'r') as fh:
        pred = json.load(fh)
    mu = np.array(pred['mu']); std = np.array(pred['std'])
    Y_val = _load_val_true()
    # Isotonic or temperature scaling
    if args.method == "isotonic":
        f = isotonic_sigma_mapping(Y_val, mu, std, n_quantiles=args.quantiles)
        std_cal = f(std)
    else:
        # one-parameter scale via simple grid-search to targets
        targets = (0.5,0.8,0.9,0.95)
        def coverage_loss(scale):
            from .eval.calibration import interval_coverage
            mu_f = mu.flatten(); std_f = (std*scale).flatten(); y_f = Y_val.flatten()
            covs = [interval_coverage(y_f, mu_f, std_f, conf=t).empirical for t in targets]
            return float(np.mean((np.array(covs) - np.array(targets))**2))
        best = min([(s, coverage_loss(s)) for s in np.linspace(0.3, 3.0, 108)], key=lambda t:t[1])[0]
        std_cal = std * best
    # Metrics
    nominals = [0.5,0.8,0.9,0.95]
    covers = [interval_coverage(Y_val.flatten(), mu.flatten(), std_cal.flatten(), conf=t).empirical for t in nominals]
    ece = ece_regression(Y_val.flatten(), mu.flatten(), std_cal.flatten(), n_bins=12)
    metrics_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', 'metrics', 'summary.json')
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
    print(blob)

def cmd_evaluate(args):
    # placeholder: would aggregate metrics; here just dumps metrics/summary.json path
    metrics_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', 'metrics', 'summary.json')
    print(metrics_path)

def cmd_report(args):
    plot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', 'plots')
    print(inject_figures(fig_dir=plot_dir))

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("preprocess")
    sp.set_defaults(func=cmd_preprocess)

    sf = sub.add_parser("features")
    sf.set_defaults(func=cmd_features)

    st = sub.add_parser("train")
    st.add_argument("--alpha", type=float, default=1.0)
    st.add_argument("--beta", type=float, default=25.0)
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
