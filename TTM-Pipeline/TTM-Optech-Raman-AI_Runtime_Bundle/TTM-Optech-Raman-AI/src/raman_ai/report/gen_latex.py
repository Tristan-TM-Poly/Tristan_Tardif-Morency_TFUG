import datetime, json

import os, json, shutil, subprocess, tempfile
from jinja2 import Environment, FileSystemLoader

def run(metrics_path: str, latex_template: str, out_pdf: str):
    here = os.path.dirname(__file__)
    tpl_dir = os.path.join(here, "templates", "ieee")
    env = Environment(loader=FileSystemLoader(tpl_dir))
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    tpl = env.get_template("main.tex")
    tex = tpl.render(metrics=metrics)
    tmp = tempfile.mkdtemp()
    tex_path = os.path.join(tmp, "paper.tex")
    with open(tex_path, "w") as f:
        f.write(tex)
    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "paper.tex"], cwd=tmp, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
        shutil.copy(os.path.join(tmp, "paper.pdf"), out_pdf)
    except Exception:
        os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
        shutil.copy(tex_path, out_pdf.replace(".pdf",".tex"))

# --- Auto-injected metadata footer (git SHA + params) ---
def _try_git_sha():
    import subprocess
    try:
        sha = subprocess.check_output(["git","rev-parse","--short","HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        return sha
    except Exception:
        return "unknown"

def append_metadata_to_tex(tex_path, params_path="params.yaml"):
    try:
        import yaml
        with open(tex_path, "a", encoding="utf-8") as f:
            f.write("\n% Metadata injected\n")
            f.write(f"% Git SHA: {_try_git_sha()}\n")
            f.write(f"% Build UTC: {datetime.datetime.utcnow().isoformat()}Z\n")
            try:
                with open(params_path, "r", encoding="utf-8") as pf:
                    prms = yaml.safe_load(pf) or {{}}
                f.write("% Params: " + json.dumps(prms) + "\n")
            except Exception:
                pass
    except Exception:
        pass


# ---- Added: auto-inject figures if present ----
def inject_figures(fig_dir='plots'):
    figs = []
    if os.path.isdir(fig_dir):
        for fn in sorted(os.listdir(fig_dir)):
            if fn.lower().endswith('.png'):
                figs.append(os.path.join(fig_dir, fn))
    # Write a LaTeX include snippet
    snippet = os.path.join(fig_dir, 'figures.tex')
    with open(snippet, 'w') as fh:
        for path in figs:
            fh.write('\\begin{figure}[h]\n')
            fh.write('  \\centering\n')
            fh.write(f'  \\includegraphics[width=0.95\\linewidth]{{{path}}}\n')
            fh.write('  \\caption{Auto-included figure from pipeline.}\n')
            fh.write('\\end{figure}\n\n')
    return snippet
