"""Direct whole-board cylcgt values for the finite Q-family base cases.

Run from the project root with .venv/bin/python. The runner in run_q_family.sh
compares each value's nim-heap signature with the separate C whole-board solver.
"""
import re
import os
import resource
import subprocess
import sys
import time

ROOT = os.path.abspath(".")
OUT = os.path.join(ROOT, "research", "ring_q_family_check")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "research", "ring_n_plus_2_proof"))
import fam
from cylcgt import cgt, pawns


def position(tokens):
    white, black = set(), set()
    for f, token in enumerate(tokens):
        side = None
        for char in token:
            if char in "WB":
                side = char
            elif char.isdigit():
                (white if side == "W" else black).add((f, int(char)))
    return pawns.Pos(frozenset(white), frozenset(black))


def main(n):
    board = pawns.Board(n, 8, True, True)
    pos = position(fam.Q(n))
    pawns.RACE_RULE = "count"
    pawns.PASSED_RESPECTS_EP = True
    pawns.components = lambda _board, p: [p]
    pawns._value.cache_clear()
    t0 = time.monotonic()
    value = pawns.value(board, pos)
    sig = "".join(cgt.outcome(cgt.add(value, cgt.nimber(h))) for h in range(8))

    rg = subprocess.run(
        [os.path.join(OUT, "rg"), "solve", "7"],
        input=" ".join(fam.Q(n)) + "\n",
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip().split()
    assert rg and rg[0] == sig, (n, cgt.show(value), sig, rg)
    assert len(pos.white) + len(pos.black) == n + 2
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mib = peak / (1024 * 1024 if sys.platform == "darwin" else 1024)
    print(
        f"Q n={n} pawns={len(pos.white) + len(pos.black)} "
        f"whole-board cylcgt={cgt.show(value)} signature={sig} "
        f"rg={rg[0]} CHECKED-2 ({time.monotonic() - t0:.1f}s) "
        f"peak-rss={peak_mib:.1f} MiB",
        flush=True,
    )


if __name__ == "__main__":
    if len(sys.argv) != 2 or not re.fullmatch(r"(?:8|1[02468]|20|22)", sys.argv[1]):
        raise SystemExit("usage: .venv/bin/python research/ring_q_family_check/q_whole_cyl.py N (even 8..22)")
    main(int(sys.argv[1]))
