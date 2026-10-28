#!/usr/bin/env python3
"""crosscheck.py RINGS.tsv OUT.tsv [--ep both|keep|expire] -- re-solve rings (column 1, rg signature in column 2) with Codex's
third solver research/ring_n_plus_2_check/independent.py (its game(n, ep_on_heap) -> signatures(position)), which imports only
cylcgt.pawns.{Board,Pos,passed}.  Run from the project root with PYTHONPATH=. .  Fresh game (fresh caches) per ring and variant.
OUT.tsv: ring, rg signature, independent signature [expire], independent signature [keep], agree"""
import sys, os, importlib.util, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ringlib import parse
spec = importlib.util.spec_from_file_location("independent", os.path.join(HERE, "..", "..", "ring_n_plus_2_check", "independent.py"))
ind = importlib.util.module_from_spec(spec); spec.loader.exec_module(ind)
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
out = open(sys.argv[2], "w")
mode = sys.argv[sys.argv.index("--ep") + 1] if "--ep" in sys.argv else "both"
bad = 0
for r in rows:
    ring, rgsig = r[0], r[1]
    cfg = parse(ring); n = len(cfg)
    white = sum(1 << ind.square(f, rk - 1, n) for f, (w, b) in enumerate(cfg) for rk in w)
    black = sum(1 << ind.square(f, rk - 1, n) for f, (w, b) in enumerate(cfg) for rk in b)
    res = {}
    t0 = time.time()
    for name, flag in (("expire", False), ("keep", True)):
        if mode not in ("both", name):
            res[name] = "-"; continue
        signatures, passers, state_count = ind.game(n, flag)
        assert passers(white, black, None) == (False, False)
        res[name] = signatures((white, black, None))
    ok = all(v in ("-", rgsig) for v in res.values())
    bad += (not ok)
    out.write("%s\t%s\t%s\t%s\t%s\t%.1fs\n" % (ring, rgsig, res["expire"], res["keep"], "agree" if ok else "DISAGREE", time.time() - t0))
    out.flush()
print("rings %d, disagreements %d" % (len(rows), bad))
