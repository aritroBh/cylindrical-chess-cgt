"""C4 verifier negative control: does bench.verify.check_cylcgt (the function behind
E2) detect the e.p.-aware change when a row DOES contain a component that filter 5'
removed? Builds rows (gold = textbook truth via bench.generate.instance) from the 48
library-v1 components that change under the e.p.-aware test, then runs check_cylcgt
under both tests. Also counts e.p.-aware withholding events (ep_capturable True).
usage: neg_control.py EP_ROOT OUT_JSON"""
import os, sys
EP = os.path.abspath(sys.argv[1]); sys.path.insert(0, EP)
import json, random
from collections import Counter
from cylcgt import pawns, cgt
from cylcgt.pawns import Board
import bench.components as C, bench.generate as G, bench.verify as V, bench.cgtfmt as F, bench.board as bd
assert pawns.__file__.startswith(EP)
HITS = [0]
_orig = pawns.ep_capturable
def counting(*a):
    r = _orig(*a)
    HITS[0] += bool(r)
    return r
pawns.ep_capturable = counting

def set_test(aware):
    pawns.PASSED_RESPECTS_EP = aware; pawns._value.cache_clear()

P = "/Users/aritro/Downloads/Research/Chessendgames"
changed = json.load(open(P + "/bench/results/conventions_summary.json"))["v1_changed"]
lib = [json.loads(x) for x in open(P + "/bench/data/components.jsonl")]
pawns.RACE_RULE = "count"
set_test(False)
def comp_from(cid, text):
    w, b = bd.parse_pos_text(text)
    width = max(f for f, _ in w | b) + 1
    p = pawns.Pos(frozenset(w), frozenset(b))
    brd = Board(width, 8, False, True)
    g = pawns.value(brd, p)
    moves = [{"side": s, "move": n, "_game": pawns._child(brd, c, s)} for s, n, c in C._children(width, p, True)]
    return {"comp_id": cid, "width": width, "value": F.fmt(g), "_game": g, "_pos": p, "moves": moves}
negs = [(r, comp_from(r["v1_id"], r["position"])) for r in changed]
libc = [comp_from(c["comp_id"], c["position"]) for c in lib]
rng = random.Random(1)
rows = []
for r, c in negs:
    assert F.fmt(c["_game"], ascii=True) == r["textbook"], (r, F.fmt(c["_game"], ascii=True))
    for wrap in (False, True):
        rec, _ = G.instance([(c, 0)], 8, wrap); rec["tag"] = (r["v1_id"], "k1", wrap, r["root_differs"]); rows.append(rec)
        o = rng.choice([x for x in libc if x["width"] + c["width"] + 2 <= 8])
        rec, _ = G.instance([(c, 0), (o, c["width"] + 1)], 8, wrap); rec["tag"] = (r["v1_id"], "k2+" + o["comp_id"], wrap, r["root_differs"]); rows.append(rec)
# positive side: library rows built the same way must pass under both tests
for c in rng.sample(libc, 60):
    rec, _ = G.instance([(c, 0)], 8, False); rec["tag"] = (c["comp_id"], "lib-k1", False, None); rows.append(rec)
out = {}
for name, aware in (("textbook", False), ("e.p.-aware", True)):
    set_test(aware); HITS[0] = 0
    res = Counter()
    for rec in rows:
        ok = V.check_cylcgt(rec, ("count",))["count"]
        kind = "library" if rec["tag"][1] == "lib-k1" else ("filter5'-removed, root changes" if rec["tag"][3] else "filter5'-removed, only children change")
        res[f"{kind} (agree)"] += ok; res[f"{kind} (total)"] += 1
    out[name] = {"counts": dict(sorted(res.items())), "ep_capturable_true_calls": HITS[0]}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps(out, indent=1))
