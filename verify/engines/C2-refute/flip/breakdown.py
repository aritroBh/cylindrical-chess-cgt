"""Breakdown of the flip test by N subgroup, plus a stricter 'both signs right' criterion.
    cd /Users/aritro/Downloads/Research/Chessendgames && .venv/bin/python verify/engines/C2-refute/flip/breakdown.py
Needs tb_twins_rows.json (tb_twins.py) and indep_rows.json (indep_flip.py)."""
import json, statistics
from collections import defaultdict
from pathlib import Path
H = Path(__file__).resolve().parent
NP = json.loads((H / "tb_twins_rows.json").read_text())
def grp(r):
    v = r["value_count"]
    if r["o_x"] == "P": return "P"
    if v.startswith("*"): return "N nimber"
    if "W" in v: return "N hot +-BIG"
    return "N other"
g = defaultdict(list)
for r in NP: g[grp(r)].append(r)
print("| group | n | Lc0 delta right | SF delta right | Lc0 both signs right (model) | SF both signs right (model) | Lc0 median |dcp| | SF median |d| |")
for k in sorted(g):
    rs = g[k]; want = 1 if k.startswith("N") else -1
    lr = sum((r["d_lc"] > 0) == (want > 0) for r in rs); sr = sum((r["d_sf"] > 0) == (want > 0) for r in rs)
    def both(r, a, b):
        w, bb = (r[a], r[b]) if r["stm"] == "W" else (r[b], r[a])  # White-to-move eval, Black-to-move eval
        return (w > 0 and bb < 0) if want > 0 else (w < 0 and bb > 0)
    lb = sum(both(r, "lc_white", "lc_twin_white") for r in rs); sb = sum(both(r, "sf_final", "sf_twin_final") for r in rs)
    print(f"| {k} | {len(rs)} | {lr} | {sr} | {lb} | {sb} | {statistics.median(abs(r['d_lc']) for r in rs):.0f} | {statistics.median(abs(r['d_sf']) for r in rs):.2f} |")
print("\nLc0 wrong:", [(r["id"], r["o_x"], r["value_count"], r["component"], r["d_lc"], "TB", r["tb_orig"], r["tb_twin"]) for r in NP if (r["d_lc"] > 0) != (r["o_x"] == "N")])
print("SF wrong P:", [(r["id"], r["component"], r["d_sf"]) for r in NP if r["o_x"] == "P" and r["d_sf"] > 0])
rows = json.loads((H / "indep_rows.json").read_text())
for o in "NPLR":
    ds = [r["d_sf"] for r in rows if r["o_x"] == o]
    print(o, "SF delta mean %+.2f median %+.2f  share<0 %d/%d" % (statistics.mean(ds), statistics.median(ds), sum(d < 0 for d in ds), len(ds)))
