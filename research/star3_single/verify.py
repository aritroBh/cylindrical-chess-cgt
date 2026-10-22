#!/usr/bin/env python3
"""Verify the value of a position with independent programs.

usage: verify.py MODE WIDTH WRAP "W: a4 b3 / B: a7 b7"
  MODE  = sum | whole | codex | all
  WRAP  = flat | cyl
sum   : cylcgt, default setting, pawns.components as shipped (disjunctive sum of components)
whole : cylcgt, default setting, pawns.components = lambda b, p: [p]  (the whole board is one game)
codex : verify_ext/codex/solver.py PawnGame(width, "count", True, "aware")  (flat boards only)
The C program s3 is the third (fast) program: run it with --eval.
"""
import sys, time, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "verify_ext", "codex"))
sys.setrecursionlimit(1000000)


def cyl(mode, width, wrap, pos):
    from cylcgt import pawns, cgt
    pawns.RACE_RULE = "count"
    pawns.PASSED_RESPECTS_EP = True
    if mode == "whole":
        pawns.components = lambda b, p: [p]
    pawns._value.cache_clear()
    b = pawns.Board(width, 8, wrap == "cyl", True)
    g = pawns.value(b, pawns.Pos.parse(pos))
    return cgt.show(g)


def codex(width, wrap, pos):
    if wrap == "cyl":
        return "n/a (flat only)"
    import solver as cx
    g = cx.PawnGame(width, "count", True, "aware")
    w, b = cx.parse_position(pos.replace(":", ""), width)
    return cx.show(g.value(w, b))


if __name__ == "__main__":
    mode, width, wrap, pos = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    modes = ["sum", "whole", "codex"] if mode == "all" else [mode]
    for m in modes:
        t = time.time()
        v = codex(width, wrap, pos) if m == "codex" else cyl(m, width, wrap, pos)
        print(f"{m}\t{wrap}{width}\t{pos}\t{v}\t{time.time()-t:.1f}s", flush=True)
