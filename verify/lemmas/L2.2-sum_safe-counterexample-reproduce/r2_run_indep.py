"""Run the independent implementation (r2_indep.py, no project imports) on the
headline counterexample, all 9 rows of notes/lemmas.md §2, the mechanism node,
and the per-child disagreement counts.

cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/lemmas/L2.2-sum_safe-counterexample-reproduce/r2_run_indep.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r2_indep import Game, comps, gen, parse, show  # noqa: E402

ROWS = [  # (files, ranks, wrap, ep, position, rule, claimed o(S), claimed o(W))
    (8, 8, True, False, "W: b2 d4 g3 h5 / B: a7 c7 f7 g4", "count", "R", "N"),
    (8, 8, True, False, "W: b3 f4 g5 / B: a5 b6 f5 h6", "count", "N", "L"),
    (8, 8, True, False, "W: b2 c5 d4 f3 / B: c7 d6 e7 g6", "count", "L", "N"),
    (8, 8, True, True, "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count", "R", "N"),
    (8, 8, True, True, "W: a5 b6 d2 e2 / B: a7 c7 e7", "count", "L", "N"),
    (8, 7, True, False, "W: c2 g2 h4 / B: a5 b6 f5 g6", "count", "R", "N"),
    (7, 6, False, True, "W: b2 d3 f2 / B: c4 c5 e5 g5", "count", "N", "R"),
    (8, 8, True, True, "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent", "N", "L"),
    (6, 8, False, False, "W: b2 d4 f4 / B: b7 c5 e5 e7", "opponent", "R", "N"),
]

allok = True
for n, m, wrap, ep, text, rule, cs, cw in ROWS:
    t0 = time.time()
    x = parse(text)
    g = Game(n, m, wrap, ep, rule)
    nc = len(comps(n, m, wrap, x))
    s, w = g.S_outcome(x), g.W_outcome(x)
    # BIG sensitivity: the outcome of S should not depend on BIG once BIG is large
    s64 = Game(n, m, wrap, ep, rule, BIG=64).S_outcome(x)
    s1000 = Game(n, m, wrap, ep, rule, BIG=1000).S_outcome(x)
    ok = (nc == 1 and s == cs and w == cw and s != w and s64 == s and s1000 == s)
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} {n}x{m} {'cyl' if wrap else 'flat'} ep={'on' if ep else 'off'} {rule:8s} {text}: "
          f"components={nc} o(S)={s} (BIG64 {s64}, BIG1000 {s1000}) o(W)={w}  claimed {cs}/{cw}  {time.time()-t0:.1f}s",
          flush=True)

# headline details
n, m, wrap, ep, rule = 8, 8, True, False, "count"
g = Game(n, m, wrap, ep, rule)
x = parse("W: b2 d4 g3 h5 / B: a7 c7 f7 g4")
print("\nheadline component files:", sorted({f for f, _ in x[0] | x[1]}), "->", [show(c) for c in comps(n, m, wrap, x)])
for side in ("W", "B"):
    kids = sorted(gen(n, m, wrap, ep, x, side), key=show)
    diff = 0
    for c in kids:
        wp, bp = g.term(c)
        if wp or bp:
            print(f"   {side} -> {show(c)}: terminal (W passer {wp}, B passer {bp})")
            continue
        so, wo = g.S_outcome(c), g.W_outcome(c)
        diff += so != wo
        print(f"   {side} -> {show(c)}: o(S)={so} o(W)={wo} {'DIFF' if so != wo else ''}")
    print(f"  {side}: {len(kids)} moves, {diff} children with o(S) != o(W)")

# mechanism node
y = parse("W: b5 d4 g3 / B: c6 f6 g4 h6")


def reach(start):
    seen, st = {start}, [start]
    while st:
        p = st.pop()
        wp, bp = g.term(p)
        if wp or bp:
            continue
        for side in ("W", "B"):
            src = p if (p[2] is not None and p[2][2] == side) else (p[0], p[1], None)
            for c in gen(n, m, wrap, ep, src, side):
                if c not in seen:
                    seen.add(c)
                    st.append(c)
    return seen


R = reach(x)
print("\nmechanism node", show(y), "reachable from headline:", y in R, f"(|reachable| = {len(R)})")
print("   components:", [(show(c), sorted(g.threats(c))) for c in comps(n, m, wrap, y)])
print("   o(S) =", g.S_outcome(y), " o(W) =", g.W_outcome(y))
print("\nALL ROWS OK" if allok else "\nSOME ROW BAD")
