"""Run the verifier's solver on every family position.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/sumtest/C1-refute/vrun.py [--jobs 4]
writes verify/sumtest/C1-refute/out/v__<board>__<rule>__<ep|noep>__<scope>.json.gz
"""
import argparse
import gzip
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from vsolve import BOARDS, NAMES, TEXTBOOK, Board, Solver, build_refs, family, key, outcome_letter  # noqa: E402

OUT = os.path.join(HERE, "out")


def selftest():
    U, refs = build_refs()
    b = Board(1, False, False, "count")
    s = Solver(b, U)
    LF, RF = s.solve((0, 0, None))
    vec = "".join(outcome_letter(LF, RF, x) for x in refs)
    assert vec == TEXTBOOK, vec
    # one file: W a4 / B a6 = *
    sq = b.sq
    LF, RF = s.solve((1 << sq(0, 4), 1 << sq(0, 6), None))
    v_star = "".join(outcome_letter(LF, RF, x) for x in refs)
    # abstract identities on the empty board: G + G' vectors
    U2, refs2 = build_refs()
    st = refs2[1]; s2_ = refs2[2]; up = refs2[4]; dn = refs2[5]
    z2 = U2.add(st, st); zz = U2.add(s2_, s2_); ud = U2.add(up, dn)
    s3 = Solver(Board(1, False, False, "count"), U2)
    LF, RF = s3.solve((0, 0, None))
    for g in (z2, zz, ud):
        assert outcome_letter(LF, RF, g) == "P"
    assert v_star == "NPNNNNLLLRLRLNN", v_star
    print("selftest: textbook vector OK; W a4/B a6 vector", v_star)
    return True


def run(task):
    bname, rule, ep, scope = task
    path = os.path.join(OUT, f"v__{bname}__{rule}__{'ep' if ep else 'noep'}__{scope}.json.gz")
    if os.path.exists(path):
        return path, None
    t0 = time.time()
    files, wrap = BOARDS[bname]
    U, refs = build_refs()
    b = Board(files, wrap, ep, rule, scope)
    s = Solver(b, U)
    res = {}
    for W, B in family(files, wrap):
        LF, RF = s.solve((W, B, None))
        res[key(files, W, B)] = "".join(outcome_letter(LF, RF, x) for x in refs)
    meta = {"board": bname, "rule": rule, "ep": ep, "scope": scope, "positions": len(res),
            "states": len(s.memo), "race_resolutions": b.races, "seconds": round(time.time() - t0, 1)}
    tmp = path + ".tmp"
    with gzip.open(tmp, "wt") as fh:
        json.dump({"meta": meta, "outcomes": res}, fh)
    os.replace(tmp, path)
    return path, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    selftest()
    tasks = []
    for bname in BOARDS:
        for rule in ("count", "mover", "opponent"):
            tasks.append((bname, rule, False, "P"))
            tasks.append((bname, rule, True, "P"))
            tasks.append((bname, rule, True, "global"))
    with Pool(a.jobs) as p:
        for path, meta in p.imap_unordered(run, tasks):
            print(path, meta, flush=True)


if __name__ == "__main__":
    main()
