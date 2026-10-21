"""Verifier scratch: for the cylinder placements of W a2 c2 / B b7 d7 that
pass the freeze test on NON-terminal nodes, list what fails at terminal nodes.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/cylatlas/C7-reproduce/terminal_detail.py
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_freeze import *

W0 = [(0, 2), (2, 2)]; B0 = [(1, 7), (3, 7)]; width = 4
alln = reach_any_order(W0, B0, width)
nonterm = reach_any_order(W0, B0, width, include_terminal=False)
term = alln - nonterm
print("nodes", len(alln), "non-terminal", len(nonterm), "terminal", len(term))
def nm(s): return f"{FILES[s[0]]}{s[1]}"
for wrap in (True, False):
    print("=== cyl8" if wrap else "=== flat8")
    for off, mir, s, r, wk, bk in all_placements(width):
        if classify(nonterm, width, off, mir, wk, bk, wrap):
            continue
        k = classify(term, width, off, mir, wk, bk, wrap)
        mp = (lambda c: off + width - 1 - c) if mir else (lambda c: off + c)
        wkn, bkn = king_nbrs(wk, wrap), king_nbrs(bk, wrap)
        stats = collections.Counter()
        ex = {}
        for W, B in term:
            wp = passed_side(W, B, width, "W"); bp = passed_side(W, B, width, "B")
            who = "race" if wp and bp else ("Wpasser" if wp else "Bpasser")
            for (f, q) in W:
                sq = (mp(f), q)
                single_passed = passed_side(frozenset([(f, q)]), B, width, "W")
                tag = None
                if bk in pawn_targets(sq, "W", wrap): tag = "W-check"
                elif sq in bkn: tag = "W-adj-BK"
                if tag:
                    key = (who, tag, "pawn is passed" if single_passed else "pawn not passed")
                    stats[key] += 1
                    ex.setdefault(key, (sorted(map(nm, [(mp(a), b) for a, b in W])), sorted(map(nm, [(mp(a), b) for a, b in B]))))
            for (f, q) in B:
                sq = (mp(f), q)
                single_passed = passed_side(W, frozenset([(f, q)]), width, "B")
                tag = None
                if wk in pawn_targets(sq, "B", wrap): tag = "B-check"
                elif sq in wkn: tag = "B-adj-WK"
                if tag:
                    key = (who, tag, "pawn is passed" if single_passed else "pawn not passed")
                    stats[key] += 1
                    ex.setdefault(key, (sorted(map(nm, [(mp(a), b) for a, b in W])), sorted(map(nm, [(mp(a), b) for a, b in B]))))
        print(f"off={off} mirror={mir} s={s:+d} r={r} WK={nm(wk)} BK={nm(bk)} terminal-fail kinds={sorted(k)}")
        for key, c in sorted(stats.items()):
            print("    ", key, c, "e.g. W", ex[key][0], "B", ex[key][1])
