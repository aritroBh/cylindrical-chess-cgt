"""C2-theory verifier: audit the flip test's ground truth (read-only on worker files)."""
import json, statistics
from collections import Counter, defaultdict
from pathlib import Path
R = Path("/Users/aritro/Downloads/Research/Chessendgames")
se = {r["id"]: r for r in json.loads((R/"engine/experiments/results/static_eval.json").read_text())["rows"]}
lc = {r["id"]: r for r in json.loads((R/"engine/experiments/results/lc0_value_n1.json").read_text())["rows"]}
print("n rows", len(se), len(lc))
# e.p. squares in originals
ep = [r["id"] for r in se.values() if r["fen"].split()[3] != "-"]
print("originals with an e.p. square:", len(ep), ep[:10])
# treb types
print("treb:", Counter(r["treb"] for r in se.values()))
print("stm by class:", Counter((r["o"], r["stm"]) for r in se.values()))
# duplicates: originals that are twins of each other
board = {}
for r in se.values():
    key = " ".join(r["fen"].split()[:3])
    board.setdefault(key, []).append(r["id"])
dups = {k: v for k, v in board.items() if len(v) > 1}
print("duplicate originals:", len(dups))
tw = set(" ".join(r["twin"].split()[:3]) for r in se.values())
pairs = [r["id"] for r in se.values() if " ".join(r["fen"].split()[:3]) in tw]
print("originals that are another original's twin:", len(pairs), pairs[:20])
# model vs TB on originals
def pred(o, stm):
    # model's predicted root result for the side to move
    if o == "N": return "win"
    if o == "P": return "loss"
    if o == "L": return "win" if stm == "W" else "loss"
    if o == "R": return "win" if stm == "B" else "loss"
agree = defaultdict(Counter)
for r in se.values():
    p = pred(r["o"], r["stm"])
    agree[r["o"]][("agree" if r["tb_root"] == p else r["tb_root"])] += 1
for o in "NPLR":
    print("class", o, dict(agree[o]))
# flip test restricted to originals where TB root == model prediction
def deltas(r):
    sgn = 1 if r["stm"] == "W" else -1
    l = lc[r["id"]]
    return (r["final"] - r["twin_final"]) * sgn, (l["lc0_orig_white_cp"] - l["lc0_twin_white_cp"]) * sgn
for o in "NP":
    allr = [r for r in se.values() if r["o"] == o]
    ok = [r for r in allr if r["tb_root"] == pred(o, r["stm"])]
    bad = [r for r in allr if r["tb_root"] != pred(o, r["stm"])]
    for name, rs in (("all", allr), ("orig TB agrees with model", ok), ("orig TB disagrees", bad)):
        if not rs: continue
        want = o == "N"
        sf = sum((deltas(r)[0] > 0) == want for r in rs)
        l0 = sum((deltas(r)[1] > 0) == want for r in rs)
        print(f"flip {o} {name}: n={len(rs)} SF right {sf} Lc0 right {l0}")
# per-class delta distribution for SF, and Lc0
for o in "NPLR":
    rs = [r for r in se.values() if r["o"] == o]
    d = [deltas(r)[0] for r in rs]; dl = [deltas(r)[1] for r in rs]
    print(o, len(rs), "SF median %+.2f, >0: %d, <0: %d, ==0: %d" % (statistics.median(d), sum(x>0 for x in d), sum(x<0 for x in d), sum(x==0 for x in d)),
          "| Lc0 median %+.0f, >0: %d, <0: %d" % (statistics.median(dl), sum(x>0 for x in dl), sum(x<0 for x in dl)))
# sign correctness on both sides (stronger test): mover-POV sign right on original AND twin vs model
for o in "NP":
    rs = [r for r in se.values() if r["o"] == o]
    def both(rw_orig, rw_twin, r):
        # White-POV evals; model says White-to-move result
        sgn = 1 if r["stm"] == "W" else -1
        eW = rw_orig if r["stm"] == "W" else rw_twin
        eB = rw_twin if r["stm"] == "W" else rw_orig
        if o == "N": return eW > 0 and eB < 0
        return eW < 0 and eB > 0
    sf = sum(both(r["final"], r["twin_final"], r) for r in rs)
    l0 = sum(both(lc[r["id"]]["lc0_orig_white_cp"], lc[r["id"]]["lc0_twin_white_cp"], r) for r in rs)
    print(f"both signs right vs model, {o}: n={len(rs)} SF {sf}, Lc0 {l0}")
