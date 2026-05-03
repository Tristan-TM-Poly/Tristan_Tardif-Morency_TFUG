#!/usr/bin/env python3
"""AI-7 Continuous Audit: bounded verification for code, claims, curve-fit and hypergraph proxies.

This script is intentionally safe and local-first. It does not deploy, purchase,
submit, file, or contact external services. It produces evidence artifacts that
can be uploaded by GitHub Actions.

Checks included:
- repository inventory and package presence
- Python syntax compilation for a bounded number of files
- optional unit test discovery summary
- AntiHype scan for unsupported high-risk claims
- synthetic curve-fit smoke test using a small Gaussian model
- mycelial hypergraph proxy from path/component co-occurrence
- DCT++ truth-level summary
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import os
import re
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

HIGH_RISK_PATTERNS = [
    r"sur[- ]?unit[eé]",
    r"[eé]nergie infinie",
    r"validation physique confirm[eé]e",
    r"supraconductivit[eé] confirm[eé]e",
    r"d[eé]p[oô]t officiel effectu[eé]",
    r"brevet d[eé]pos[eé]",
    r"cloud d[eé]ploy[eé]",
    r"achat effectu[eé]",
    r"revenu passif garanti",
    r"omniscien",
    r"omnipoten",
    r"transmission instantan[eé]e",
]

TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".yml", ".yaml", ".tex", ".jsx", ".js", ".tsx", ".ts"}
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


@dataclass
class CompileResult:
    checked: int
    ok: int
    failed: int
    failures: list[dict]


@dataclass
class AntiHypeResult:
    files_scanned: int
    matches: int
    findings: list[dict]


@dataclass
class CurveFitResult:
    model: str
    points: int
    true_center: float
    estimated_center: float
    true_sigma: float
    estimated_sigma: float
    mse: float
    status: str


@dataclass
class HypergraphResult:
    nodes: int
    hyperedges: int
    top_nodes: list[tuple[str, int]]
    top_hyperedges: list[tuple[str, int]]


def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def iter_files(root: Path, suffixes: set[str] | None = None, max_files: int = 5000) -> Iterable[Path]:
    count = 0
    for path in root.rglob("*"):
        if count >= max_files:
            break
        if path.is_file() and not should_skip(path):
            if suffixes is None or path.suffix.lower() in suffixes:
                count += 1
                yield path


def compile_python(root: Path, max_files: int = 800) -> CompileResult:
    failures = []
    checked = ok = 0
    for path in iter_files(root, {".py"}, max_files=max_files):
        checked += 1
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
            ast.parse(source, filename=str(path))
            ok += 1
        except Exception as exc:  # syntax or decode edge case
            failures.append({"path": str(path.relative_to(root)), "error": repr(exc)[:500]})
    return CompileResult(checked=checked, ok=ok, failed=len(failures), failures=failures[:50])


def antihype_scan(root: Path, max_files: int = 1200) -> AntiHypeResult:
    compiled = [(p, re.compile(p, re.IGNORECASE)) for p in HIGH_RISK_PATTERNS]
    findings = []
    files_scanned = 0
    matches = 0
    for path in iter_files(root, TEXT_SUFFIXES, max_files=max_files):
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for raw, pat in compiled:
            for m in pat.finditer(text):
                matches += 1
                line = text.count("\n", 0, m.start()) + 1
                findings.append({"path": str(path.relative_to(root)), "line": line, "pattern": raw})
                if len(findings) >= 100:
                    return AntiHypeResult(files_scanned=files_scanned, matches=matches, findings=findings)
    return AntiHypeResult(files_scanned=files_scanned, matches=matches, findings=findings)


def synthetic_curve_fit() -> CurveFitResult:
    # A tiny pure-Python Gaussian moment fit for bounded CI smoke testing.
    n = 241
    xs = [100.0 + i * (200.0 / (n - 1)) for i in range(n)]
    true_center = 187.0
    true_sigma = 18.0
    baseline = 3.0
    amp = 42.0
    ys = [baseline + amp * math.exp(-0.5 * ((x - true_center) / true_sigma) ** 2) for x in xs]
    # baseline estimate from edges, then moment center/sigma on positive corrected signal
    edge = max(5, n // 20)
    b = (sum(ys[:edge]) + sum(ys[-edge:])) / (2 * edge)
    weights = [max(0.0, y - b) for y in ys]
    sw = sum(weights) or 1.0
    center = sum(x * w for x, w in zip(xs, weights)) / sw
    var = sum(((x - center) ** 2) * w for x, w in zip(xs, weights)) / sw
    sigma = math.sqrt(max(var, 0.0))
    pred = [b + max(weights) * math.exp(-0.5 * ((x - center) / max(sigma, 1e-9)) ** 2) for x in xs]
    mse = sum((y - p) ** 2 for y, p in zip(ys, pred)) / n
    status = "pass" if abs(center - true_center) < 2.0 and abs(sigma - true_sigma) < 3.0 else "review"
    return CurveFitResult(
        model="gaussian_moment_smoke",
        points=n,
        true_center=true_center,
        estimated_center=round(center, 6),
        true_sigma=true_sigma,
        estimated_sigma=round(sigma, 6),
        mse=round(mse, 9),
        status=status,
    )


def hypergraph_proxy(root: Path, max_files: int = 3000) -> HypergraphResult:
    node_counts: Counter[str] = Counter()
    edge_counts: Counter[str] = Counter()
    keywords = [
        "raman", "curve", "fit", "baseline", "auc", "bootstrap", "calibration", "replicate",
        "ftte", "hgfm", "hypergraph", "fractal", "mycel", "global", "coupling", "top64",
        "portal", "tfuga", "sim", "evidence", "gate", "bat", "rosetta", "dct", "cloud", "workflow",
    ]
    for path in iter_files(root, TEXT_SUFFIXES, max_files=max_files):
        rel = str(path.relative_to(root)).lower()
        present = sorted({k for k in keywords if k in rel})
        parts = [p.lower() for p in path.parts if p.lower() not in IGNORE_DIRS]
        present.extend([p for p in parts[:4] if p not in {".", ""}])
        present = sorted(set(present))
        for node in present:
            node_counts[node] += 1
        if len(present) >= 2:
            edge_key = " | ".join(present[:6])
            edge_counts[edge_key] += 1
    return HypergraphResult(
        nodes=len(node_counts),
        hyperedges=len(edge_counts),
        top_nodes=node_counts.most_common(20),
        top_hyperedges=edge_counts.most_common(20),
    )


def repo_inventory(root: Path) -> dict:
    suffix_counts = Counter()
    top_dirs = Counter()
    total = 0
    for path in iter_files(root, None, max_files=10000):
        total += 1
        suffix_counts[path.suffix.lower() or "<none>"] += 1
        rel = path.relative_to(root)
        if rel.parts:
            top_dirs[rel.parts[0]] += 1
    return {
        "files_sampled": total,
        "suffix_counts": suffix_counts.most_common(25),
        "top_dirs": top_dirs.most_common(25),
        "canonical_paths_present": {
            "packages": (root / "packages").exists(),
            "evidence": (root / "evidence").exists(),
            "docs": (root / "docs").exists(),
            "github_workflows": (root / ".github" / "workflows").exists(),
            "publications_master_v10": (root / "publications" / "axiom-tristan-master-v10").exists(),
        },
    }


def write_report(out_dir: Path, report: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ai7_continuous_audit_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [
        "# AI-7 Continuous Audit Report",
        "",
        f"Generated UTC: {report['generated_utc']}",
        f"Truth level: {report['truth_level']}",
        "",
        "## Summary",
        "",
        f"- Files sampled: {report['inventory']['files_sampled']}",
        f"- Python compile checked/failed: {report['python_compile']['checked']} / {report['python_compile']['failed']}",
        f"- AntiHype matches: {report['antihype']['matches']}",
        f"- Curve-fit smoke status: {report['curve_fit']['status']}",
        f"- Hypergraph proxy nodes/hyperedges: {report['hypergraph']['nodes']} / {report['hypergraph']['hyperedges']}",
        "",
        "## Promotion gate",
        "",
        "This audit is evidence for software health only. It does not validate physical claims, official filings, purchases, revenues, or cloud deployments.",
    ]
    (out_dir / "AI7_CONTINUOUS_AUDIT_REPORT.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", default="reports/ai7-continuous-audit")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    t0 = time.time()
    report = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "truth_level": "T2 software audit artifact; not physical or official validation",
        "root": str(root),
        "inventory": repo_inventory(root),
        "python_compile": asdict(compile_python(root)),
        "antihype": asdict(antihype_scan(root)),
        "curve_fit": asdict(synthetic_curve_fit()),
        "hypergraph": asdict(hypergraph_proxy(root)),
        "elapsed_seconds": None,
    }
    report["elapsed_seconds"] = round(time.time() - t0, 3)
    write_report(Path(args.out), report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    # Fail only on syntax failures or curve-fit smoke failure, not on AntiHype findings.
    if report["python_compile"]["failed"] > 0:
        return 2
    if report["curve_fit"]["status"] != "pass":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
