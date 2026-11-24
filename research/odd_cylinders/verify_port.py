#!/usr/bin/env python3
"""T12: check the ported solver research/odd_cylinders/kpsolve9 against
kings/kpsolve (the original, verified C solver) and against kings/ref/solve.py
(the independent Python reference solver).

The port changes the bitboards from 64 to 128 bits and the board limit from 8 to
10 files, so that 9- and 10-file cylinders fit.  Agreement on boards with at
most 8 files is the evidence that the port is faithful.

Usage:
  .venv/bin/python research/odd_cylinders/verify_port.py --material KPKP --samples 20000
"""
import argparse
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FILES = "abcdefghij"


def rand_positions(W, H, material, n_samples, rng, wrap=True):
    white = material[1:material.index("K", 1)]
    black = material[material.index("K", 1) + 1:]
    sqs = [(f, r) for f in range(W) for r in range(1, H + 1)]
    pawn_sqs = [(f, r) for f, r in sqs if 2 <= r <= H - 1]

    def adjacent(a, b):
        df = abs(a[0] - b[0])
        if wrap:
            df = min(df, W - df)
        return max(df, abs(a[1] - b[1])) <= 1

    out = []
    tries = 0
    while len(out) < n_samples and tries < n_samples * 60:
        tries += 1
        wk = rng.choice(sqs)
        bk = rng.choice(sqs)
        if wk == bk or adjacent(wk, bk):
            continue
        free = [s for s in pawn_sqs if s not in (wk, bk)]
        if len(free) < white.count("P") + black.count("P"):
            continue
        wp = rng.sample(free, white.count("P"))
        rest = [s for s in free if s not in wp]
        bp = rng.sample(rest, black.count("P"))
        toks = [f"K{FILES[wk[0]]}{wk[1]}", f"k{FILES[bk[0]]}{bk[1]}"]
        toks += [f"P{FILES[f]}{r}" for f, r in wp] + [f"p{FILES[f]}{r}" for f, r in bp]
        toks += [rng.choice("wb")]
        out.append(" ".join(toks) + " -")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--material", default="KPKP")
    ap.add_argument("--samples", type=int, default=20000)
    ap.add_argument("--boards", default="cyl:3x5,cyl:4x6,cyl:5x5,cyl:6x7,cyl:7x8,cyl:8x5,cyl:8x8")
    ap.add_argument("--cap", default="1")
    ap.add_argument("--promote", default="QRBN")
    ap.add_argument("--ep", default="on")
    ap.add_argument("--ref", action="store_true", help="also run the Python reference solver")
    ap.add_argument("--seed", type=int, default=20261021)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    kps = os.path.join(ROOT, "kings", "kpsolve")
    kps9 = os.path.join(HERE, "kpsolve9")
    bad = 0
    for board in a.boards.split(","):
        kind, size = board.split(":")
        W, H = map(int, size.split("x"))
        lines = rand_positions(W, H, a.material, a.samples, rng, wrap=(kind == "cyl"))
        inp = "\n".join(lines) + "\n"
        opts = ["--board", board, "--cap", a.cap, "--promote", a.promote, "--ep", a.ep]
        c1 = subprocess.run([kps, *opts], input=inp, capture_output=True, text=True, check=True)
        c2 = subprocess.run([kps9, *opts], input=inp, capture_output=True, text=True, check=True)
        l1, l2 = c1.stdout.splitlines(), c2.stdout.splitlines()
        assert len(l1) == len(l2) == len(lines), (len(l1), len(l2), len(lines))
        d = [(x, y) for x, y in zip(l1, l2) if x.split("|")[1].split() != y.split("|")[1].split()]
        msg = f"{board} {a.material} cap {a.cap} promote {a.promote} ep {a.ep}: {len(lines)} positions, " \
              f"kpsolve9 vs kpsolve: {len(d)} differ"
        if a.ref:
            r = subprocess.run([sys.executable, "-m", "kings.ref.solve", *opts], input=inp,
                               capture_output=True, text=True, check=True, cwd=ROOT)
            l3 = r.stdout.splitlines()
            d3 = [(x, y) for x, y in zip(l1, l3) if x.split("|")[1].split() != y.split("|")[1].split()]
            msg += f"; kpsolve9 vs kings/ref: {len(d3)} differ"
            for x, y in d3[:5]:
                print("  REF DIFF:", x, "|", y)
        print(msg, flush=True)
        for x, y in d[:5]:
            print("  DIFF:", x, "|", y)
        bad += len(d)
    print("total differences:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
