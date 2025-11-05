
import os, json
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def run(feats_folder: str, model: str="conv1d_bayes", cv: int=5, seed: int=42):
    fp = os.path.join(feats_folder, "features.parquet")
    df = pd.read_parquet(fp)
    y = df.get("peak_max", pd.Series(np.random.randn(len(df))))
    X = df.drop(columns=[c for c in df.columns if c in ("sample_id","peak_max")], errors="ignore").fillna(0.0).to_numpy()
    kf = KFold(n_splits=max(2, min(cv, max(2, len(df)//2))), shuffle=True, random_state=seed)
    rmses = []
    for tr, va in kf.split(X):
        m = RandomForestRegressor(random_state=seed)
        m.fit(X[tr], y.iloc[tr])
        p = m.predict(X[va])
        rmses.append(float(np.sqrt(mean_squared_error(y.iloc[va], p))))
    os.makedirs("models", exist_ok=True)
    metrics = {"cv_rmse_mean": float(np.mean(rmses)), "cv_rmse_std": float(np.std(rmses))}
    with open("models/last_metrics.json","w") as f:
        json.dump(metrics, f, indent=2)
    model_art = {"feature_means": df.mean(numeric_only=True).to_dict()}
    with open("models/last.pkl","w") as f:
        json.dump(model_art, f)


# ---- Added: Bayesian multi-output option ----
def train_bayesian_multioutput(X_train, Y_train, X_val=None, Y_val=None, alpha=1.0, beta=25.0, out_dir='models/bayes_multi'):
    from .heads.bayes_multi import BayesianLinearMultiOutput, BayesLinConfig
    import numpy as np, os, json
    os.makedirs(out_dir, exist_ok=True)
    model = BayesianLinearMultiOutput(BayesLinConfig(alpha=alpha, beta=beta)).fit(np.asarray(X_train), np.asarray(Y_train))
    # Save posterior mean and S_N
    np.save(os.path.join(out_dir, 'm_N.npy'), model.m_N)
    np.save(os.path.join(out_dir, 'S_N.npy'), model.S_N)
    with open(os.path.join(out_dir, 'meta.json'), 'w') as fh:
        json.dump({'alpha': alpha, 'beta': beta, 'D': model.D, 'K': model.K}, fh)
    metrics = {}
    if X_val is not None and Y_val is not None:
        mu, std = model.predict(np.asarray(X_val), return_std=True)
        mae = float(np.mean(np.abs(mu - Y_val)))
        metrics.update({'val_mae': mae})
        with open(os.path.join(out_dir, 'val_pred.json'), 'w') as fh:
            json.dump({'mu': mu.tolist(), 'std': std.tolist()}, fh)
    with open(os.path.join(out_dir, 'metrics.json'), 'w') as fh:
        json.dump(metrics, fh)
    return out_dir
