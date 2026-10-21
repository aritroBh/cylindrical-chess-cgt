"""Find tablebase results for the side-to-move twins of the N positions in every cache on disk (no network).
  cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C1-refute/static_eval_c1/twin_cache.py
"""
import glob, json, os
R = "/Users/aritro/Downloads/Research/Chessendgames/"
idx = {}
for p in glob.glob(R + "**/*.json", recursive=True):
    if "/tablebase/" in p or "cache" not in p:
        continue
    try:
        rec = json.load(open(p))
    except Exception:
        continue
    if not isinstance(rec, dict) or "fen" not in rec or rec.get("status") != 200 or not rec.get("data"):
        continue
    idx[" ".join(rec["fen"].split()[:4])] = rec["data"]
me = json.load(open(R + "verify/engines/C1-refute/static_eval_c1/indep_eval.json"))
def twin(fen):
    f = fen.split(); f[1] = "b" if f[1] == "w" else "w"; f[3] = "-"; return " ".join(f[:4])
found, missing = {}, []
for d in me:
    if d["tb"] in ("win", "loss") and d["o"] == "N":
        t = twin(d["fen"])
        if t in idx:
            found[d["id"]] = idx[t]["category"]
        else:
            missing.append((d["id"], t))
print("N positions:", len(found) + len(missing), "twins cached:", len(found), "missing:", len(missing))
print("cached twin categories:", {k: v for k, v in sorted(found.items())})
json.dump({"found": found, "missing": missing}, open(R + "verify/engines/C1-refute/static_eval_c1/twin_cache.json", "w"), indent=0)
