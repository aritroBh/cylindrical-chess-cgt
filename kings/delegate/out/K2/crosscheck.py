"""Cross-check kings/kpsolve (C) against the independent reference solver kings/ref
(Python, written from SPEC.md alone) on every placement of small material sets on
tiny boards.

Usage (from the project root):
  python3 kings/delegate/out/K2/crosscheck.py --board cyl:4x5 --material KPK KPKP KPPK --cap 1 [--kpsolve PATH]
Appends one summary line per run to kings/delegate/out/K2/crosscheck.txt and writes any
differences to kings/delegate/out/K2/crosscheck_diffs.txt.
"""
import argparse
import itertools
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
OUTDIR = os.path.dirname(os.path.abspath(__file__))
FILES = "abcdefgh"


def positions(W, H, material):
    """All placements of the material (e.g. 'KPKP' = white K+P vs black K+P) with
    distinct squares and non-adjacent kings, both sides to move. Legality beyond
    that (checks) is left to the solvers, which must both answer X."""
    white = material[1:material.index("K", 1)]
    black = material[material.index("K", 1) + 1:]
    sqs = [(f, r) for f in range(W) for r in range(1, H + 1)]
    pawn_sqs = [(f, r) for f, r in sqs if 2 <= r <= H - 1]

    def adjacent(a, b):
        df = abs(a[0] - b[0])
        if WRAP:
            df = min(df, W - df)
        return max(df, abs(a[1] - b[1])) <= 1

    out = []
    for wk, bk in itertools.permutations(sqs, 2):
        if adjacent(wk, bk):
            continue
        free = [s for s in pawn_sqs if s not in (wk, bk)]
        for wp in itertools.combinations(free, white.count("P")):
            rest = [s for s in free if s not in wp]
            for bp in itertools.combinations(rest, black.count("P")):
                toks = [f"K{FILES[wk[0]]}{wk[1]}", f"k{FILES[bk[0]]}{bk[1]}"]
                toks += [f"P{FILES[f]}{r}" for f, r in wp] + [f"p{FILES[f]}{r}" for f, r in bp]
                for stm in "wb":
                    out.append(" ".join(toks) + f" {stm} -")
    return out


WRAP = False


def main():
    global WRAP
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True)
    ap.add_argument("--material", nargs="+", required=True)
    ap.add_argument("--cap", default="1")
    ap.add_argument("--promote", default="QRBN")
    ap.add_argument("--ep", default="on")
    ap.add_argument("--kpsolve", default=f"{ROOT}/kings/kpsolve")
    a = ap.parse_args()
    kind, size = a.board.split(":")
    W, H = map(int, size.split("x"))
    WRAP = kind == "cyl"
    lines = []
    for m in a.material:
        lines += positions(W, H, m)
    inp = "\n".join(lines) + "\n"
    opts = ["--board", a.board, "--cap", a.cap, "--promote", a.promote, "--ep", a.ep]
    t0 = time.time()
    c = subprocess.run([a.kpsolve, *opts, "--threads", "4"], input=inp, capture_output=True, text=True, check=True)
    t1 = time.time()
    r = subprocess.run([sys.executable, "-m", "kings.ref.solve", *opts], input=inp, capture_output=True,
                       text=True, check=True, cwd=ROOT)
    t2 = time.time()
    cl, rl = c.stdout.splitlines(), r.stdout.splitlines()
    assert len(cl) == len(rl) == len(lines), (len(cl), len(rl), len(lines))
    diffs = [(x, y) for x, y in zip(cl, rl) if x.split("|")[1].split() != y.split("|")[1].split()]
    counts = {}
    for x in cl:
        v = tuple(x.split("|")[1].split())
        key = v[0] if v[0] == v[1] else "bounds"
        counts[key] = counts.get(key, 0) + 1
    summary = (f"{a.board} {'+'.join(a.material)} cap {a.cap} promote {a.promote} ep {a.ep}: "
               f"{len(lines)} positions, {len(diffs)} differ; kpsolve values {counts}; "
               f"time C {t1 - t0:.0f}s, Python {t2 - t1:.0f}s")
    print(summary)
    os.makedirs(OUTDIR, exist_ok=True)
    with open(f"{OUTDIR}/crosscheck.txt", "a") as fh:
        fh.write(summary + "\n")
    if diffs:
        with open(f"{OUTDIR}/crosscheck_diffs.txt", "a") as fh:
            fh.write(f"## {summary}\n")
            for x, y in diffs[:200]:
                fh.write(f"C:  {x}\nPy: {y}\n")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
