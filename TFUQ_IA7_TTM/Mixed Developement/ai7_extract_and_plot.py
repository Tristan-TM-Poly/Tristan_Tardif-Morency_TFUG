#!/usr/bin/env python3
"""
ai7_extract_and_plot.py
- Parse SPICE .log files to extract .meas results into JSON/CSV.
- Parse hp_v4_timeseries.csv to generate KPI plots (PNG).
Usage:
    python ai7_extract_and_plot.py --logs ./logs --csv ./hp_v4_timeseries.csv --out ./out
Notes:
    - Expects LTspice/Micro-Cap style .log containing lines like:
        Measurement: GAIN_50kHZ
        mag(v(vout)) = 1.234
    - Also supports generic "name = value" lines.
"""
import argparse, re, json, csv
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def parse_spice_log(log_path: Path):
    text = log_path.read_text(errors='ignore')
    results = {}
    # Common patterns: "name = value" or two-line blocks after 'Measurement:'
    # 1) Single-line name = number
    for m in re.finditer(r'^\s*([A-Za-z0-9_]+)\s*=\s*([-+Ee0-9\.\*\/\(\)]+)', text, flags=re.M):
        name, val = m.group(1), m.group(2)
        # Try to eval; fallback to float conversion stripping units if present
        try:
            v = float(eval(val, {"__builtins__": {}}, {"pi": 3.141592653589793}))
        except Exception:
            try:
                v = float(re.findall(r'[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?', val)[0])
            except Exception:
                continue
        results[name] = v
    # 2) LTspice "Measurement: NAME" then next line contains value
    for mm in re.finditer(r'Measurement:\s*([A-Za-z0-9_]+)\s*\n([^\n\r]+)', text):
        name = mm.group(1)
        val_line = mm.group(2)
        try:
            v = float(re.findall(r'[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?', val_line)[0])
            results[name] = v
        except Exception:
            pass
    return results

def parse_many_logs(log_dir: Path):
    summary = {}
    log_dir = Path(log_dir)
    for p in sorted(log_dir.glob("*.log")):
        summary[p.name] = parse_spice_log(p)
    return summary

def plots_from_csv(csv_path: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(csv_path)
    # Plot 1: Vin vs time
    plt.figure()
    plt.plot(df["t_us"], df["Vin"])
    plt.xlabel("t (µs)")
    plt.ylabel("V_in (norm)")
    plt.title("AI-7 HP-v4: V_in vs time")
    plt.tight_layout()
    plt.savefig(out_dir / "plot_vin_vs_time.png", dpi=200)
    plt.close()

    # Plot 2: SNR vs time
    plt.figure()
    plt.plot(df["t_us"], df["SNR_dB"])
    plt.xlabel("t (µs)")
    plt.ylabel("SNR (dB)")
    plt.title("AI-7 HP-v4: SNR vs time")
    plt.tight_layout()
    plt.savefig(out_dir / "plot_snr_vs_time.png", dpi=200)
    plt.close()

    # Plot 3: Energy per MAC vs time
    plt.figure()
    plt.plot(df["t_us"], df["E_per_MAC_pJ"])
    plt.xlabel("t (µs)")
    plt.ylabel("Energy per MAC (pJ)")
    plt.title("AI-7 HP-v4: Energy/MAC vs time")
    plt.tight_layout()
    plt.savefig(out_dir / "plot_energy_vs_time.png", dpi=200)
    plt.close()
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", type=str, default=None, help="Directory with SPICE .log files")
    ap.add_argument("--csv", type=str, default=None, help="hp_v4_timeseries.csv")
    ap.add_argument("--out", type=str, default="./out", help="Output directory")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.logs:
        summary = parse_many_logs(Path(args.logs))
        (out_dir / "spice_meas_summary.json").write_text(json.dumps(summary, indent=2))
        # Also write a flattened CSV of key fields if present
        keys = set()
        for v in summary.values():
            keys.update(v.keys())
        keys = sorted(keys)
        rows = []
        for fname, d in summary.items():
            row = {"file": fname}
            for k in keys:
                row[k] = d.get(k, "")
            rows.append(row)
        # Save CSV
        import csv
        with open(out_dir / "spice_meas_summary.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["file"] + keys)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)

    if args.csv:
        df = plots_from_csv(Path(args.csv), out_dir)
        # Save a version of df for inspection
        df.to_csv(out_dir / "hp_v4_timeseries_clean.csv", index=False)

if __name__ == "__main__":
    main()
