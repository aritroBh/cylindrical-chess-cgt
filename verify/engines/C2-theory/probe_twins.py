"""C2-theory: probe the twins of all 21 CGT-P positions and a seeded sample of 18 uncached CGT-N twins.
Hard cap 40 requests in this verifier's own ledger; own cache dir. Other caches are read first (offline).
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/engines/C2-theory/probe_twins.py [--dry]
"""
import glob, json, random, sys
from pathlib import Path
R = Path("/Users/aritro/Downloads/Research/Chessendgames")
sys.path.insert(0, str(R))
from realchess.probe import Prober
HERE = R / "verify/engines/C2-theory"
se = json.loads((R/"engine/experiments/results/static_eval.json").read_text())["rows"]
dirs = [str(R/"realchess/cache")] + sorted(set(glob.glob(str(R/"verify/**/tbcache*"), recursive=True)))
offl = [Prober(cap=0, ledger="/dev/null", cache_dir=d, offline=True) for d in dirs]
def cached(fen):
    for p in offl:
        rec = p.cached(fen)
        if rec is not None:
            return rec, p.cache_dir
    return None, None
P = [r for r in se if r["o"] == "P"]
Nunc = sorted(r["id"] for r in se if r["o"] == "N" and cached(r["twin"])[0] is None)
rng = random.Random(2026)
Nsel = set(rng.sample(Nunc, 18))
todo = P + [r for r in se if r["id"] in Nsel]
print("to probe:", len(todo), "P", len(P), "N sample", len(Nsel))
if "--dry" in sys.argv:
    sys.exit()
pr = Prober(cap=40, ledger=str(HERE/"ledger.jsonl"), cache_dir=str(HERE/"tbcache"), tag="C2-theory", verbose=True)
out = []
for r in todo:
    rec, where = cached(r["twin"])
    if rec is None:
        rec = pr.probe(r["twin"]); where = pr.cache_dir
    d = rec["data"] or {}
    out.append({"id": r["id"], "o": r["o"], "twin": r["twin"], "status": rec["status"],
                "tb_root_twin": d.get("category"), "cache": where})
(HERE/"twin_probe_results.json").write_text(json.dumps(out, indent=1))
print("requests this process:", pr.requests_this_process, "ledger:", pr.ledger_count())
