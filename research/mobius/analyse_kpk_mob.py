#!/usr/bin/env python3
"""Summarise a kpsolve KPK results file (kings/SPEC.md output format) for one board.

usage: .venv/bin/python research/mobius/analyse_kpk_mob.py RESULTS_FILE [--label NAME]

Reports, from White's point of view:
  * WTM / BTM legal counts and win rates (denominator = legal positions, X excluded);
  * 'zugzwang' boards in the sense of kp_tablebases/REPORT.md section 2: WTM draw and BTM White win
    (both sides to move would rather pass; v_w < v_b);
  * the strict 'whoever moves loses' boards (WTM loss and BTM win): zero, since Black never wins KPK;
  * the value of the rook-pawn position Ka6 Pa5 vs Ka8 (both sides to move).
"""
import argparse
from collections import defaultdict


def load(path):
    rows = {}
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#") or "|" not in line:
                continue
            pos, res = line.split("|", 1)
            toks = pos.split()
            stm = toks[3]
            key = " ".join(toks[:3])  # board: piece tokens only
            a, b = res.split()
            rows[(key, stm)] = (a, b)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results")
    ap.add_argument("--label", default="")
    args = ap.parse_args()
    rows = load(args.results)
    tot = defaultdict(int)
    cnt = defaultdict(lambda: defaultdict(int))
    for (key, stm), (a, b) in rows.items():
        if a == "X":
            continue
        tot[stm] += 1
        cnt[stm][a] += 1
    boards = {k for k, _ in rows}
    z = s = 0
    for key in boards:
        w = rows.get((key, "w"))
        bl = rows.get((key, "b"))
        if w is None or bl is None or w[0] == "X" or bl[0] == "X":
            continue
        if w[0] == "D" and bl[0] == "W":
            z += 1
        if w[0] == "L" and bl[0] == "W":
            s += 1
    print("== %s (%s)" % (args.label or args.results, args.results))
    for stm in ("w", "b"):
        n = tot[stm]
        print("  %s-to-move legal=%d W=%d D=%d L=%d  White wins %.4f%%" % (
            stm.upper() + "TM" if stm == "w" else "BTM", n, cnt[stm]["W"], cnt[stm]["D"], cnt[stm]["L"],
            100.0 * cnt[stm]["W"] / n))
    print("  zugzwang boards (WTM=D, BTM=W; v_w < v_b): %d" % z)
    print("  strict whoever-moves-loses boards (WTM=L, BTM=W): %d" % s)
    for name, (ka, pa, kb) in [("Ka6 Pa5 vs Ka8", ("a6", "a5", "a8"))]:
        kk = "K%s P%s k%s" % (ka, pa, kb)
        print("  %s: WTM=%s  BTM=%s" % (name, rows.get((kk, "w"), ("missing",))[0],
                                         rows.get((kk, "b"), ("missing",))[0]))


if __name__ == "__main__":
    main()
