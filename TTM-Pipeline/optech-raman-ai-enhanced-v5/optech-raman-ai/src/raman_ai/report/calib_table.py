import os, json, numpy as np

def write_calibration_table(metrics_path, out_tex):
    if not os.path.isfile(metrics_path):
        raise FileNotFoundError(metrics_path)
    with open(metrics_path, 'r') as fh:
        m = json.load(fh)
    nom = m.get('calibration', {}).get('nominal', [])
    emp = m.get('calibration', {}).get('empirical', [])
    rows = []
    for n, e in zip(nom, emp):
        rows.append((n, e, e - n))
    with open(out_tex, 'w') as f:
        f.write('\\begin{table}[h]\n\\centering\\begin{tabular}{lrr}\n\\hline\n')
        f.write('Nominal & Empirical & Gap \\\\\n\\hline\n')
        for n,e,g in rows:
            f.write(f"{n:.2f} & {e:.4f} & {g:+.4f} \\\\\
")
        f.write('\\hline\n\\end{tabular}\n\\caption{Uncertainty calibration (post-scaling/isotonic).}\n\\end{table}\n')
