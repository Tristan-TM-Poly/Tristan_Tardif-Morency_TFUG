#!/usr/bin/env python3
import json, sys, pathlib

def main(runs_dir="runs", out_tex="latex/metrics_table.tex"):
    runs = sorted(pathlib.Path(runs_dir).glob("*_metrics.json"))
    rows = []
    for r in runs:
        try:
            d = json.loads(r.read_text(encoding="utf-8"))
            rows.append(d)
        except Exception as e:
            print(f"[WARN] skip {r}: {e}")
    if not rows:
        print("[INFO] no metrics found")
        return
    # Build LaTeX table
    cols = sorted({k for row in rows for k in row.keys()})
    lines = []
    lines.append(r"\begin{tabular}{%s}" % ("l" * len(cols)))
    lines.append(r"\hline")
    lines.append(" & ".join(cols) + r" \\ \hline")
    for row in rows:
        vals = [str(row.get(c, "")) for c in cols]
        lines.append(" & ".join(vals) + r" \\")
    lines.append(r"\hline")
    lines.append(r"\end{tabular}")
    outp = pathlib.Path(out_tex)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] wrote {outp}")

if __name__ == "__main__":
    main(*sys.argv[1:])
