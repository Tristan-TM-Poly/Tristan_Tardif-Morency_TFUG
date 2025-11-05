# Demo script to run the kernel on three materials.
import json, csv
from tfu_sc_analytic import SCInputs, compute_all, estimate_Df_from_Tc

materials = {
    "YBCO": {
        "inputs": dict(theta0=900.0, lambda0=1.0, mu_star=0.12,
                       vF0=2.0e5, mstar0=2.0*9.10938356e-31, ns0=8e27,
                       Df_ref=1.2, al=0.70, at=0.70, ans=-0.70, pf=0.2, beta=1.0),
        "Tc_target": 92.0,
    },
    "MgB2": {
        "inputs": dict(theta0=750.0, lambda0=0.9, mu_star=0.10,
                       vF0=3.0e5, mstar0=1.5*9.10938356e-31, ns0=7e27,
                       Df_ref=1.2, al=0.39, at=-0.27, ans=-0.70, pf=0.1, beta=1.0),
        "Tc_target": 39.0,
    },
    "H3S": {
        "inputs": dict(theta0=1500.0, lambda0=2.0, mu_star=0.10,
                       vF0=3.0e5, mstar0=1.0*9.10938356e-31, ns0=1e29,
                       Df_ref=1.2, al=0.45, at=0.41, ans=-0.70, pf=0.15, beta=1.0),
        "Tc_target": 203.0,
    },
}

out_rows = []
for name, cfg in materials.items():
    p = SCInputs(**cfg["inputs"])
    Df_star = estimate_Df_from_Tc(cfg["Tc_target"], p)
    obs = compute_all(Df_star, p)
    obs["material"] = name
    out_rows.append(obs)

with open("results_demo.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    for r in out_rows:
        w.writerow(r)

print("Wrote results_demo.csv with", len(out_rows), "rows.")
