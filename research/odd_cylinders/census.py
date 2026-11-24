#!/usr/bin/env python3
"""T12 driver: run the K+P vs K+P mutual-zugzwang census and the K+P vs K
opposition table on cylinders C_n x R for n = 3..9 and R = 5..8.

Uses research/odd_cylinders/kpsolve9 (kings/kpsolve ported to 128-bit
bitboards, so that 9- and 10-file cylinders fit).

Every census is run twice, once with each side of the officer cap bound
(bound 0: a capped promotion counts as a White win; bound 1: as a Black win).
A position is *exact* when the two bounds agree, i.e. when no capped promotion
could have influenced the answer.

Usage:  .venv/bin/python research/odd_cylinders/census.py [--jobs N] [--scope all|facing]
"""
import argparse
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SOLVER = os.path.join(HERE, "kpsolve9")
DATA = os.path.join(HERE, "data")

FILES = "abcdefghij"


def run(board, mode, scope=None, bound=None, cap=1, promote="Q", ep="on", threads=1):
    cmd = [SOLVER, "--board", board, "--census", mode, "--cap", str(cap),
           "--promote", promote, "--ep", ep, "--threads", str(threads)]
    if scope:
        cmd += ["--scope", scope]
    if bound is not None:
        cmd += ["--bound", str(bound)]
    return cmd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--scope", default="all")
    ap.add_argument("--cap", default="1")
    ap.add_argument("--promote", default="Q")
    ap.add_argument("--ep", default="on")
    ap.add_argument("--widths", default="3,4,5,6,7,8,9")
    ap.add_argument("--heights", default="5,6,7,8")
    ap.add_argument("--modes", default="kpkp,kpk")
    a = ap.parse_args()

    os.makedirs(DATA, exist_ok=True)
    widths = [int(x) for x in a.widths.split(",")]
    heights = [int(x) for x in a.heights.split(",")]
    modes = a.modes.split(",")

    jobs = []
    for W in widths:
        for H in heights:
            board = f"cyl:{W}x{H}"
            for mode in modes:
                if mode == "kpkp":
                    for bound in (0, 1):
                        out = os.path.join(DATA, f"census_kpkp_{W}x{H}_b{bound}.txt")
                        jobs.append((run(board, mode, a.scope if a.scope != "all" else None,
                                         bound, a.cap, a.promote, a.ep), out, board, mode, bound))
                else:
                    out = os.path.join(DATA, f"census_kpk_{W}x{H}.txt")
                    jobs.append((run(board, mode, None, None, a.cap, a.promote, a.ep), out,
                                 board, mode, None))

    print(f"{len(jobs)} jobs, {a.jobs} at a time", flush=True)
    t0 = time.time()
    running = []
    done = 0
    queue = list(jobs)
    while queue or running:
        while queue and len(running) < a.jobs:
            cmd, out, board, mode, bound = queue.pop(0)
            if os.path.exists(out) and os.path.getsize(out) > 0:
                done += 1
                continue
            fh = open(out + ".tmp", "w")
            p = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.PIPE)
            running.append((p, cmd, out, fh, board, mode, bound))
        time.sleep(0.5)
        still = []
        for p, cmd, out, fh, board, mode, bound in running:
            if p.poll() is None:
                still.append((p, cmd, out, fh, board, mode, bound))
                continue
            fh.close()
            err = p.stderr.read().decode()
            if p.returncode == 0:
                os.replace(out + ".tmp", out)
                done += 1
                print(f"[{done}/{len(jobs)}] {board} {mode} bound={bound} ok  {err.strip()}", flush=True)
            else:
                print(f"[{done}/{len(jobs)}] {board} {mode} bound={bound} FAILED rc={p.returncode} "
                      f"{err.strip()}", flush=True)
        running = still
    print(f"total {time.time() - t0:.1f}s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
