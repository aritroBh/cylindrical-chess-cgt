#!/usr/bin/env python3
"""T27 step 2: recompute every count/mover *3 hit of the T24 6-file, 8-pawn scan with cylcgt
(component-sum solver) in all 9 settings and compare with the scanner (frontier_split, whole-board
solver) columns stored in scanner_rows.tsv.

Run from the project root:
  PYTHONPATH=. nice -n 10 .venv/bin/python research/star27_textbook3/verify_cylcgt.py \
      > research/star27_textbook3/cylcgt_results.tsv

Scanner encoding (frontier_split.c): "X,k" with X in {N,L,R,P} the outcome of G (N = first player
wins, L/R = Left/Right wins, P = second player wins) and k = least k with G+*k a second-player win,
i.e. G = *k (k = 0 means G = 0, -1 means G is not a nimber).
"""
import sys
import time

from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, value

HERE = "research/star27_textbook3/"
# scanner column order: (race, ep_on, aware)
SETTINGS = [
    ("count", True, False), ("count", False, False), ("count", True, True),
    ("mover", True, False), ("mover", False, False), ("mover", True, True),
    ("opponent", True, False), ("opponent", False, False), ("opponent", True, True),
]
NAMES = ["count/epon", "count/epoff", "count/epon/aware",
         "mover/epon", "mover/epoff", "mover/epon/aware",
         "opponent/epon", "opponent/epoff", "opponent/epon/aware"]


def nimber_of(g):
    if g is cgt.ZERO:
        return 0
    return g.nim if g.nim is not None else -1


def main():
    rows = [l.rstrip("\n").split("\t") for l in open(HERE + "scanner_rows.tsv")]
    print("position\tsetting\tcylcgt_value\tcylcgt_outcome\tcylcgt_nimber\tscanner_outcome\t"
          "scanner_nimber\tmatch\tseconds")
    bad = 0
    for row in rows:
        text = row[0]
        pos = Pos.parse(text)
        for k, (rule, ep_on, aware) in enumerate(SETTINGS):
            pawns.RACE_RULE = rule
            pawns.PASSED_RESPECTS_EP = aware
            pawns._value.cache_clear()
            pawns.race_hits.clear()
            t0 = time.time()
            g = value(Board(6, 8, False, ep_on), pos)
            dt = time.time() - t0
            c_out, c_nim = cgt.outcome(g), nimber_of(g)
            s_out, s_nim = row[3 + k].split(",")
            ok = (c_out == s_out) and (c_nim == int(s_nim))
            bad += not ok
            print(f"{text}\t{NAMES[k]}\t{cgt.show(g)}\t{c_out}\t{c_nim}\t{s_out}\t{s_nim}\t"
                  f"{'yes' if ok else 'NO'}\t{dt:.2f}", flush=True)
    print(f"# mismatches: {bad} of {len(rows) * len(SETTINGS)}", file=sys.stderr)


if __name__ == "__main__":
    main()
