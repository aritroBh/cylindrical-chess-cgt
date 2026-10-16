"""Part 2(b): outcome vectors of G + R for every position of the test families.

Families: (w,b) in {(1,1),(2,1),(1,2),(2,2)} pawns, 8 ranks, pawns on ranks 2-7,
no passed pawn in the initial position; boards flat3, flat4, cyl3, cyl4, cyl5.

Usage (from the project root):
  PYTHONPATH=. .venv/bin/python -m sumtest.enum_positions --jobs 12
writes sumtest/data/mine__<board>__<rule>__<epvariant>__<mode>.json.gz
(position -> 15-letter outcome string in REF_NAMES order).
"""
import argparse
import gzip
import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

from sumtest.sumsolver import REF_NAMES, FILES, Geometry, Rules, SumSolver, Trees, reference_set

BOARDS = {"flat3": (3, False), "flat4": (4, False), "cyl3": (3, True), "cyl4": (4, True), "cyl5": (5, True)}
COUNTS = [(1, 1), (2, 1), (1, 2), (2, 2)]
# e.p. variants: name -> (ep, ep_aware, ep_scope)
EPV = {"off": (False, True, "component"),
       "plain": (True, False, "component"),
       "aware": (True, True, "component"),
       "plain-global": (True, False, "global"),
       "aware-global": (True, True, "global")}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def key(geo, W, B):
    return geo.show(W, B)


def positions(files, wrap):
    """All (W, B) with the given counts and no initial passed pawn (any e.p. setting:
    there is no e.p. right in an initial position, so the passer test is the same)."""
    geo = Geometry(files, wrap)
    rules = Rules(geo, ep=False)
    sqs = [geo.sq(f, r) for f in range(files) for r in range(2, 8)]
    out = []
    for nw, nb in COUNTS:
        for ws in itertools.combinations(sqs, nw):
            W = sum(1 << s for s in ws)
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                B = sum(1 << s for s in bs)
                if not rules.has_initial_passer(W, B):
                    out.append((W, B))
    return geo, out


def run(board, rule, epv, mode):
    files, wrap = BOARDS[board]
    ep, aware, scope = EPV[epv]
    if mode == "comp" and scope == "global":
        return None
    path = os.path.join(OUT, f"mine__{board}__{rule}__{epv}__{mode}.json.gz")
    if os.path.exists(path):
        return path, None
    t0 = time.time()
    geo, pos = positions(files, wrap)
    T = Trees()
    ref = reference_set(T)
    idx = [ref[n] for n in REF_NAMES]
    s = SumSolver(Rules(geo, ep=ep, ep_aware=aware, race_rule=rule), T, mode=mode, ep_scope=scope)
    res = {}
    for W, B in pos:
        wl, wr = s.solve(s.start_state(W, B))
        res[key(geo, W, B)] = "".join(s.outcome(wl, wr, k) for k in idx)
    meta = {"board": board, "rule": rule, "epv": epv, "mode": mode, "positions": len(pos),
            "states": s.nodes, "race_hits": s.rules.race_hits, "seconds": round(time.time() - t0, 1),
            "ref_names": REF_NAMES}
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt") as fh:
        json.dump({"meta": meta, "outcomes": res}, fh)
    os.replace(tmp, path)
    return path, meta


def _run(args):
    return run(*args)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--boards", default=",".join(BOARDS))
    ap.add_argument("--rules", default="count,mover,opponent")
    ap.add_argument("--epv", default="off,plain,aware")
    ap.add_argument("--modes", default="whole,comp")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tasks = [(b, r, e, m) for b in a.boards.split(",") for r in a.rules.split(",")
             for e in a.epv.split(",") for m in a.modes.split(",")]
    # biggest boards first for load balance
    tasks.sort(key=lambda t: -BOARDS[t[0]][0] - (0.5 if BOARDS[t[0]][1] else 0))
    with Pool(a.jobs) as p:
        for out in p.imap_unordered(_run, tasks):
            if out:
                print(out[0], out[1], flush=True)


if __name__ == "__main__":
    main()
