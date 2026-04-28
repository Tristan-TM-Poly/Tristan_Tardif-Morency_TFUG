import argparse, hashlib, itertools, json, heapq
from pathlib import Path

def stable_hash_score(items):
    s = "|".join(items).encode("utf-8")
    h = hashlib.sha256(s).hexdigest()
    return int(h[:8], 16) / 0xffffffff

def kw_score(text, kws):
    t = text.lower()
    return sum(1 for k in kws if k in t) / max(1, len(kws))

impact_kws = ["energy","water","climate","materials","opto","raman","ai","municipal","mining","battery","grid","space","privacy"]
ai7_kws = ["hfmc","ffwt","hypergraph","yggdrasil","ai-7","power score","privacy","license","prototype","canon","tensor","least-action"]
risk_kws = ["outreach","industry","business","health","privacy","download","sync","real","personal"]

def score_tuple(a,b,c,d):
    impact = 0.35*kw_score(a+" "+b, impact_kws) + 0.25*kw_score(c, ai7_kws) + 0.20*kw_score(d, ["verify","review","test","pilot","dct","score","privacy"]) + 0.20*stable_hash_score([a,b,c,d])
    risk = 0.25*kw_score(a+" "+b+" "+c+" "+d, risk_kws)
    governance_bonus = 0.20*kw_score(d, ["privacy","license","verify","review","audit","rollback","no outreach","human"])
    return round(max(0.0, min(1.0, impact + governance_bonus - risk)), 5)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axes", default="axes/top_64_axes.json")
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--out", default="reports/generated_top.json")
    args = ap.parse_args()
    axes = json.loads(Path(args.axes).read_text(encoding="utf-8"))
    A = axes["A_institutions_sources"]
    B = axes["B_challenges_sectors"]
    C = axes["C_ai7_capabilities"]
    D = axes["D_actions_governance"]
    heap = []
    for a,b,c,d in itertools.product(A,B,C,D):
        sc = score_tuple(a,b,c,d)
        item = (sc,a,b,c,d)
        if len(heap) < args.limit:
            heapq.heappush(heap, item)
        elif sc > heap[0][0]:
            heapq.heapreplace(heap, item)
    rows = sorted(heap, reverse=True)
    out = [{"rank": i+1, "score": sc, "institution_source": a, "challenge_sector": b, "ai7_capability": c, "action": d} for i,(sc,a,b,c,d) in enumerate(rows)]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(out)} rows to {args.out}")

if __name__ == "__main__":
    main()
