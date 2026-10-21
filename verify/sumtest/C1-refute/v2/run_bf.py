"""Run the independent brute-force solver over every family position.

  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=verify/sumtest/C1-refute/v2 .venv/bin/python verify/sumtest/C1-refute/v2/run_bf.py --jobs 6

writes v2/out/bf__<board>__<rule>__<ep|noep>__<scope>.json.gz  {key: 15-letter outcome string}
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
import bf  # noqa: E402

OUT = os.path.join(HERE, "out")


def job(args):
    board, rule, ep, scope = args
    path = os.path.join(OUT, f"bf__{board}__{rule}__{'ep' if ep else 'noep'}__{scope}.json.gz")
    if os.path.exists(path):
        return path, None
    t0 = time.time()
    F, wrap = bf.BOARDS[board]
    geo, fam = bf.family(F, wrap)
    s = bf.Solver(F, wrap, ep, rule, scope)
    res = {geo.show(W, B): [] for W, B in fam}
    for name in bf.REF_NAMES:
        x = bf.REF[name]
        s.memo.clear()
        for W, B in fam:
            res[geo.show(W, B)].append(s.outcome(W, B, x))
    res = {k: "".join(v) for k, v in res.items()}
    meta = {"board": board, "rule": rule, "ep": ep, "scope": scope, "positions": len(fam),
            "pawn_move_states": len(s.gm), "seconds": round(time.time() - t0, 1)}
    with gzip.open(path + ".tmp", "wt") as fh:
        json.dump({"meta": meta, "outcomes": res}, fh)
    os.replace(path + ".tmp", path)
    return path, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--boards", default=",".join(bf.BOARDS))
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    tasks = []
    for b in a.boards.split(","):
        for r in ("count", "mover", "opponent"):
            tasks.append((b, r, False, "pcomp"))
            for sc in ("pcomp", "G", "global"):
                tasks.append((b, r, True, sc))
    tasks.sort(key=lambda t: -bf.BOARDS[t[0]][0] - 0.5 * bf.BOARDS[t[0]][1])
    with Pool(a.jobs) as p:
        for out in p.imap_unordered(job, tasks):
            print(out[0], out[1], flush=True)


if __name__ == "__main__":
    main()
