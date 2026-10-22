#!/usr/bin/env python3
"""T27 step 4: option-by-option anatomy of one e.p.-off *3 hit (count rule, e.p. off, 6 files).

Run (project root):  PYTHONPATH=. .venv/bin/python research/star27_textbook3/explain_star3.py
For every move of the whole position, and of each independent component, prints the value of the
resulting position, then tests the standard canonical-form reductions on the *raw* option list:
  Left option A is dominated if some other Left option B has A <= B;
  Left option A is reversible if some Right reply A^R of A satisfies A^R <= G (then A is replaced by
  the Left options of A^R); symmetrically for Right.
"""
import sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos, value, moves, components, passed

pawns.RACE_RULE = "count"
pawns.PASSED_RESPECTS_EP = False   # irrelevant with e.p. off; stated for completeness
BOARD = Board(6, 8, False, False)


def raw_options(pos):
    L = [(str(p), pawns._child(BOARD, p, "W")) for p in moves(BOARD, pos, "W")]
    R = [(str(p), pawns._child(BOARD, p, "B")) for p in moves(BOARD, pos, "B")]
    return L, R


def anatomy(label, text):
    pos = Pos.parse(text)
    G = value(BOARD, pos)
    print(f"\n=== {label}: {text}   value = {cgt.show(G)}")
    comps = components(BOARD, pos)
    if len(comps) > 1:
        print("  independent components (empty files separate them):")
        for c in comps:
            print(f"    {c}   = {cgt.show(value(BOARD, c))}")
    L, R = raw_options(pos)
    for side, opts, sign in (("Left (White)", L, 1), ("Right (Black)", R, -1)):
        print(f"  {side}: {len(opts)} raw moves")
        vals = [v for _, v in opts]
        for i, (p, v) in enumerate(opts):
            dom = []
            for j, (_, w) in enumerate(opts):
                if i != j and ((sign == 1 and cgt.le(v, w) and not (cgt.le(w, v) and j > i)) or
                               (sign == -1 and cgt.le(w, v) and not (cgt.le(v, w) and j > i))):
                    dom.append(cgt.show(w))
            rev = None
            for r in (v.R if sign == 1 else v.L):
                if (sign == 1 and cgt.le(r, G)) or (sign == -1 and cgt.le(G, r)):
                    rev = r
                    break
            tag = []
            if dom:
                tag.append("dominated by " + " / ".join(dom))
            if rev is not None:
                tag.append(f"reversible through {cgt.show(rev)}")
            print(f"    {p:46s} -> {cgt.show(v):28s} {'; '.join(tag)}")
    print(f"  canonical form: Left options {[cgt.show(x) for x in G.L]}, Right options {[cgt.show(x) for x in G.R]}")


if __name__ == "__main__":
    anatomy("whole position", "W: a2 a4 c2 e2 / B: a3 a6 d7 f7")
    anatomy("a-file component", "W: a2 a4 / B: a3 a6")
    anatomy("c-f gadget (translated *2)", "W: c2 e2 / B: d7 f7")
    anatomy("4-file original *2", "W: a2 c2 / B: b7 d7")
