"""Falsification tests for Lemma L2 (when may passed pawns be replaced by +-BIG
inside sums?).

Run (from the project root):
    PYTHONPATH=. .venv/bin/python lemmas/test_L2_big.py [--n N] [--seed S]

Models (see lemmas/common.py): S = cylcgt.pawns.value (sum model, nested),
W = whole-board convention game (first passer ends the whole game),
alt = plain alternating minimax of the whole-board convention game (no CGT),
xc = crosscheck/minimax.py (Codex's independent implementation; used on
8-rank boards only, because it hard-codes Black's start rank as 7).

Checks
  T1  Theorem L2: if X is hereditarily sum-safe (HSS) and BIG exceeds the
      move bound, then o(S(X)) == o(W(X)) == alt(X). Any HSS disagreement is a
      FAIL.
  T2  o(W) == alt on every sample (CGT outcome = minimax outcome), and
      == xc on 8-rank samples.
  T3  statistics of cylcgt.pawns.sum_safe versus HSS, and every case where
      sum_safe() is True but o(S) != o(W)  (a counterexample to sum_safe as a
      correctness criterion).
  T4  regression: the fixed counterexamples below really are counterexamples
      (sum_safe True, o(S) != o(W), W confirmed by alt and, on 8 ranks, xc),
      and for each one the first non-pairwise-safe nested node is printed.
  T5  the 10 cross-check disagreements (crosscheck/REPORT_after_fix.md) all
      have sum_safe False and HSS False, and o(W) equals the cross-check.
"""
from __future__ import annotations

import argparse
import random
import re
import sys
from collections import Counter

from cylcgt import cgt, pawns
from cylcgt.pawns import BIG, Board, Pos

from lemmas.common import (RULES, S, W, alt_outcome, hereditarily_safe, pairwise_safe,
                           random_position, reachable, terminal, threats)

FAIL = []

COUNTEREXAMPLES = [
    # (board, position, rule)   all: single component, sum_safe() True
    (Board(8, 8, True, False), "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count"),
    (Board(8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count"),
    (Board(8, 8, True, False), "W: b3 f4 g5 / B: a5 b6 f5 h6", "count"),
    (Board(8, 7, True, False), "W: c2 g2 h4 / B: a5 b6 f5 g6", "count"),
]


def fail(msg):
    FAIL.append(msg)
    print("FAIL:", msg)


def xc_outcome(b: Board, x: Pos):
    if b.ranks != 8:
        return None
    from crosscheck import minimax as mm
    return mm.outcome_class(mm.Board(b.files, b.ranks, b.wrap, b.ep), mm.Position(x.white, x.black, x.ep))


def move_bound(b: Board, x: Pos):
    mw = sum(b.ranks - r for _, r in x.white)
    mb = sum(r - 1 for _, r in x.black)
    return mw, mb


def first_bad_nodes(b, x, rule, k=3):
    out = []
    for y in reachable(b, x):
        if terminal(b, y) is not None or len(pawns.components(b, y)) < 2 or pairwise_safe(b, y):
            continue
        so, wo = cgt.outcome(S(b, y, rule)), cgt.outcome(W(b, y, rule))
        if so != wo:
            out.append((len(y.white | y.black), str(y), so, wo,
                        [(str(c), sorted(threats(b, c))) for c in pawns.components(b, y)]))
    out.sort(key=lambda t: -t[0])
    return out[:k]


def run(n_samples: int, seed: int, verbose=True):
    rng = random.Random(seed)
    stats = Counter()
    sum_safe_failures = []
    done = 0
    while done < n_samples:
        files = rng.choice([4, 5, 6, 7, 8])
        ranks = rng.choice([6, 7, 8])
        b = Board(files, ranks, rng.random() < 0.6, rng.random() < 0.5)
        x = None
        nw, nb = rng.randint(1, 4), rng.randint(1, 4)
        for _ in range(300):
            p = random_position(rng, b, nw, nb)
            if terminal(b, p) is None:
                x = p
                break
        if x is None:
            continue
        rule = rng.choice(RULES)
        try:
            s, w = S(b, x, rule), W(b, x, rule)
            a = alt_outcome(b, x, rule)
        except pawns.RaceError:
            continue
        done += 1
        mw, mb = move_bound(b, x)
        if max(mw, mb) >= BIG:
            fail(f"move bound {mw},{mb} >= BIG")
        so, wo = cgt.outcome(s), cgt.outcome(w)
        if wo != a:
            fail(f"T2 o(W) {wo} != minimax {a}: {b} {x} {rule}")
        if ranks == 8 and rule == "count":
            xc = xc_outcome(b, x)
            stats["xc_checked"] += 1
            if xc != wo:
                fail(f"T2 xc {xc} != o(W) {wo}: {b} {x}")
        hss = hereditarily_safe(b, x)
        ss = pawns.sum_safe(b, x)
        multi = len(pawns.components(b, x)) > 1
        stats[(("multi" if multi else "single"), "sum_safe" if ss else "unsafe",
               "HSS" if hss else "notHSS", "agree" if so == wo else "DISAGREE")] += 1
        if hss and so != wo:
            fail(f"T1 HSS but o(S)={so} != o(W)={wo}: {b} {x} {rule}")
        if ss and so != wo:
            sum_safe_failures.append((str(b), str(x), rule, so, wo))
    if verbose:
        print(f"T1-T3 on {n_samples} random non-terminal positions:")
        for k in sorted(stats, key=str):
            print("   ", k, stats[k])
        print("T3 sum_safe() True but outcome wrong:", len(sum_safe_failures))
        for f in sum_safe_failures[:5]:
            print("    ", f)
    return stats, sum_safe_failures


def regression():
    for b, text, rule in COUNTEREXAMPLES:
        x = Pos.parse(text)
        s, w = S(b, x, rule), W(b, x, rule)
        a = alt_outcome(b, x, rule)
        xc = xc_outcome(b, x)
        ok = (pawns.sum_safe(b, x) and len(pawns.components(b, x)) == 1 and
              cgt.outcome(s) != cgt.outcome(w) and cgt.outcome(w) == a and (xc is None or xc == a))
        print(f"T4 {b} {text}: components={len(pawns.components(b, x))} sum_safe={pawns.sum_safe(b, x)} "
              f"HSS={hereditarily_safe(b, x)} o(S)={cgt.outcome(s)} o(W)={cgt.outcome(w)} minimax={a} crosscheck={xc}")
        for node in first_bad_nodes(b, x, rule, 2):
            print("      nested node with opposite threats in two components:", node)
        if not ok:
            fail(f"T4 regression {text}")


def crosscheck_ten():
    try:
        txt = open("crosscheck/REPORT_after_fix.md").read()
    except OSError:
        print("T5 skipped: crosscheck/REPORT_after_fix.md not found")
        return
    n = 0
    for bl in txt.split("### ")[1:]:
        m = re.search(r"board: (\w+), 8x8; e.p. rule: (\w+)", bl)
        text = re.search(r"Position: `([^`]*)`", bl).group(1)
        b = Board(8, 8, m.group(1) == "cylinder", m.group(2) == "on")
        x = Pos.parse(text)
        exact = re.search(r"class `(\w)`", bl).group(1)
        if pawns.sum_safe(b, x) or hereditarily_safe(b, x) or cgt.outcome(W(b, x, "count")) != exact:
            fail(f"T5 {text}")
        n += 1
    print(f"T5 cross-check disagreements re-examined: {n}; all sum_safe False, HSS False, o(W) = exact")


def test_regression():
    FAIL.clear()
    regression()
    crosscheck_ten()
    assert not FAIL, FAIL


def test_random_small():
    FAIL.clear()
    run(80, 7, verbose=False)
    assert not FAIL, FAIL


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    regression()
    crosscheck_ten()
    run(a.n, a.seed)
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)
