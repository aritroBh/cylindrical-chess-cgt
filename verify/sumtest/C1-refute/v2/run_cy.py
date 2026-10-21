"""cylcgt's predictions outcome(value(G) + X), computed afresh (imports cylcgt only; the
family enumeration and keys come from the verifier's own bf.py, not from sumtest).

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=.:verify/sumtest/C1-refute/v2 .venv/bin/python verify/sumtest/C1-refute/v2/run_cy.py --jobs 6
"""
import argparse
import gzip
import json
import os
import sys
import time
from fractions import Fraction
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bf  # noqa: E402

OUT = os.path.join(HERE, "out")


def xgames(cgt):
    one, mone = cgt.integer(1), cgt.integer(-1)
    star = cgt.make([cgt.ZERO], [cgt.ZERO])
    up = cgt.make([cgt.ZERO], [star])
    return {
        "0": cgt.make([], []), "*": star, "*2": cgt.nimber(2), "*3": cgt.nimber(3),
        "up": up, "down": cgt.make([star], [cgt.ZERO]), "up*": cgt.add(up, star),
        "dup*": cgt.add(cgt.add(up, up), star),
        "1/2": cgt.make([cgt.ZERO], [one]), "-1/2": cgt.make([mone], [cgt.ZERO]),
        "1": one, "-1": mone, "{1|0}": cgt.make([one], [cgt.ZERO]),
        "+-1": cgt.make([one], [mone]),
        "tiny1": cgt.make([cgt.ZERO], [cgt.make([cgt.ZERO], [mone])]),
    }


def job(args):
    board, rule, ep = args
    path = os.path.join(OUT, f"cy__{board}__{rule}__{'ep' if ep else 'noep'}.json.gz")
    if os.path.exists(path):
        return path, None
    from cylcgt import cgt, pawns
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    del pawns.race_hits[:]
    X = xgames(cgt)
    xo = "".join(cgt.outcome(X[n]) for n in bf.REF_NAMES)
    F, wrap = bf.BOARDS[board]
    geo, fam = bf.family(F, wrap)
    b = pawns.Board(F, 8, wrap, ep)
    t0 = time.time()
    res, info, errs = {}, {}, 0
    for W, B in fam:
        wset = frozenset(geo.fr(s) for s in bf.bits(W))
        bset = frozenset(geo.fr(s) for s in bf.bits(B))
        p = pawns.Pos(wset, bset, None)
        k = geo.show(W, B)
        assert pawns.Pos.parse(k) == p, k
        try:
            v = pawns.value(b, p)
        except Exception as e:  # noqa: BLE001
            res[k] = "ERR:" + type(e).__name__
            errs += 1
            continue
        res[k] = "".join(cgt.outcome(cgt.add(v, X[n])) for n in bf.REF_NAMES)
        info[k] = {"value": cgt.show(v), "safe": bool(pawns.sum_safe(b, p)),
                   "ncomp": len(pawns.components(b, p))}
    meta = {"board": board, "rule": rule, "ep": ep, "positions": len(fam), "errors": errs,
            "race_hits": len(pawns.race_hits), "x_outcomes": xo, "seconds": round(time.time() - t0, 1)}
    with gzip.open(path + ".tmp", "wt") as fh:
        json.dump({"meta": meta, "outcomes": res, "info": info}, fh)
    os.replace(path + ".tmp", path)
    return path, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tasks = [(b, r, ep) for b in bf.BOARDS for r in ("count", "mover", "opponent") for ep in (False, True)]
    tasks.sort(key=lambda t: -bf.BOARDS[t[0]][0] - 0.5 * bf.BOARDS[t[0]][1])
    with Pool(a.jobs) as p:
        for out in p.imap_unordered(job, tasks):
            print(out[0], out[1], flush=True)


if __name__ == "__main__":
    main()
