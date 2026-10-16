"""Fresh cylcgt predictions outcome(value(P) + X) for the verifier's own family enumeration.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C1-refute/vcylcgt.py --jobs 6
writes verify/sumtest/C1-refute/out/c__<board>__<rule>__<ep|noep>.json.gz
Imports cylcgt (the system under test) but nothing from sumtest/.
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
from vsolve import BOARDS, family, key  # noqa: E402

OUT = os.path.join(HERE, "out")


def xs(cgt):
    z = cgt.ZERO
    one, mone = cgt.integer(1), cgt.integer(-1)
    s1 = cgt.make([z], [z])
    s2 = cgt.make([z, s1], [z, s1])
    s3 = cgt.make([z, s1, s2], [z, s1, s2])
    up = cgt.make([z], [s1])
    down = cgt.make([s1], [z])
    return [z, s1, s2, s3, up, down, cgt.add(up, s1), cgt.add(cgt.add(up, up), s1),
            cgt.make([z], [one]), cgt.make([mone], [z]), one, mone,
            cgt.make([one], [z]), cgt.make([one], [mone]),
            cgt.make([z], [cgt.make([z], [mone])])]


def run(task):
    bname, rule, ep = task
    path = os.path.join(OUT, f"c__{bname}__{rule}__{'ep' if ep else 'noep'}.json.gz")
    if os.path.exists(path):
        return path, None
    from cylcgt import cgt, pawns
    pawns.RACE_RULE = rule
    pawns._value.cache_clear()
    del pawns.race_hits[:]
    files, wrap = BOARDS[bname]
    b = pawns.Board(files, 8, wrap, ep)
    X = xs(cgt)
    t0 = time.time()
    res, vals, errs = {}, {}, 0
    for W, B in family(files, wrap):
        k = key(files, W, B)
        p = pawns.Pos.parse(k)
        try:
            v = pawns.value(b, p)
        except Exception as e:  # noqa: BLE001
            res[k] = "ERR:" + type(e).__name__
            errs += 1
            continue
        res[k] = "".join(cgt.outcome(cgt.add(v, x)) for x in X)
        vals[k] = cgt.show(v)
    meta = {"board": bname, "rule": rule, "ep": ep, "positions": len(res), "errors": errs,
            "seconds": round(time.time() - t0, 1),
            "x_outcomes": "".join(cgt.outcome(x) for x in X)}
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt") as fh:
        json.dump({"meta": meta, "outcomes": res, "values": vals}, fh)
    os.replace(tmp, path)
    return path, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tasks = [(bn, r, ep) for bn in ("cyl5", "cyl4", "flat4", "cyl3", "flat3")
             for r in ("count", "mover", "opponent") for ep in (True, False)]
    with Pool(a.jobs) as p:
        for path, meta in p.imap_unordered(run, tasks):
            print(path, meta, flush=True)


if __name__ == "__main__":
    main()
