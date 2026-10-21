"""C5-theory: recompute every atom (single component, <=5 pawns) of the worker's atlas under the
ADOPTED e.p.-aware passed test (count rule, e.p. on), and as a control a sample under the textbook
test (PASSED_RESPECTS_EP=False in the same module) compared with the worker's stored key.

Run (4 shards in the background), from the project root:
  SP=<session scratchpad>; for i in 0 1 2 3; do PYTHONPATH=$SP/ep-wt:. nohup .venv/bin/python \
     verify/cylatlas/C5-theory/epaware_atoms.py --shard $i --nshards 4 > verify/cylatlas/C5-theory/epa_$i.log 2>&1 & done
"""
import argparse
import json
import os
import sys
import time

from cylcgt import cgt, pawns

HERE = os.path.dirname(os.path.abspath(__file__))
assert hasattr(pawns, "PASSED_RESPECTS_EP"), "needs the ep-aware-passed copy of cylcgt on PYTHONPATH"

_km = {}


def vkey(g):
    r = _km.get(g.id)
    if r is not None:
        return r
    if g.num is not None:
        x = g.num
        r = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    elif g.nim is not None:
        r = f"*{g.nim}"
    else:
        r = "{" + ",".join(sorted(vkey(x) for x in g.L)) + "|" + ",".join(sorted(vkey(x) for x in g.R)) + "}"
    _km[g.id] = r
    return r


_bm = {}


def has_big(g):
    r = _bm.get(g.id)
    if r is None:
        r = abs(g.num) >= pawns.BIG // 2 if g.num is not None else any(has_big(x) for x in g.L + g.R)
        _bm[g.id] = r
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--nshards", type=int, default=1)
    ap.add_argument("--control-every", type=int, default=0)
    ap.add_argument("--control-only", action="store_true", help="textbook test only, every Nth atom, compare with worker key")
    a = ap.parse_args()
    atoms = [json.loads(l) for l in open(os.path.join(HERE, "atoms.jsonl"))]
    mine = atoms[a.shard::a.nshards]
    if a.control_only:
        pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = False
        ok = bad = 0; t0 = time.time()
        for d in mine[::a.control_every or 25]:
            g = pawns.value(pawns.Board(d["n"], 8, d["board"] == "cyl", True), pawns.Pos.parse(d["pos"]))
            if vkey(g) == d["key_textbook"]: ok += 1
            else: bad += 1; print("MISMATCH", d["board"], d["n"], d["pos"], flush=True)
        print(f"control (textbook test vs worker keys): ok={ok} bad={bad} in {time.time()-t0:.0f}s", flush=True)
        return
    out = open(os.path.join(HERE, f"epa_{a.shard}.jsonl"), "w")
    pawns.RACE_RULE = "count"
    t0 = time.time()
    ctrl_ok = ctrl_bad = 0
    for i, d in enumerate(mine):
        board = pawns.Board(d["n"], 8, d["board"] == "cyl", True)
        pos = pawns.Pos.parse(d["pos"])
        pawns.PASSED_RESPECTS_EP = True
        g = pawns.value(board, pos)
        rec = {"board": d["board"], "n": d["n"], "pos": d["pos"], "key_epa": vkey(g),
               "nim_epa": g.nim, "big_epa": has_big(g), "show_epa": cgt.show(g)[:200],
               "key_textbook_worker": d["key_textbook"]}
        if a.control_every and i % a.control_every == 0:
            pawns.PASSED_RESPECTS_EP = False
            pawns._value.cache_clear()
            gt = pawns.value(board, pos)
            ok = vkey(gt) == d["key_textbook"]
            rec["control_textbook_match"] = ok
            ctrl_ok += ok
            ctrl_bad += (not ok)
            pawns.PASSED_RESPECTS_EP = True
            pawns._value.cache_clear()
        out.write(json.dumps(rec) + "\n")
        if i % 500 == 0:
            out.flush()
            print(f"{i}/{len(mine)} {time.time()-t0:.0f}s ctrl ok={ctrl_ok} bad={ctrl_bad}", flush=True)
    out.close()
    print(f"done {len(mine)} in {time.time()-t0:.0f}s ctrl ok={ctrl_ok} bad={ctrl_bad}", flush=True)


if __name__ == "__main__":
    main()
