"""For the e.p.-on rows: is the S/W disagreement caused by passer cancellation or by
local (stale) e.p. rights?  Sglob = sum-model game form in which every e.p. right expires
after ANY move (pawn move in any component, or a move in the integer). Independent code."""
import sys
from functools import lru_cache
sys.path.insert(0, ".")
from indep import B, parse, make_solvers, comps, has_passer, gen, race_winner, show, reach

ROWS = [
    ((8, 8, True, True), "W: a2 c4 e4 h2 / B: a6 b5 d7 e7", "count"),
    ((8, 8, True, True), "W: a5 b6 d2 e2 / B: a7 c7 e7", "count"),
    ((7, 6, False, True), "W: b2 d3 f2 / B: c4 c5 e5 g5", "count"),
    ((8, 8, True, True), "W: a3 e2 e4 h6 / B: a4 a5 f5 g7", "opponent"),
]

def sglob(bd, rule, BIG):
    @lru_cache(maxsize=None)
    def S(state, n, tm):
        other = "B" if tm == "W" else "W"
        clear = lambda cs: tuple((c[0], c[1], None) for c in cs)
        if tm == "W" and n > 0 and S(tuple(sorted(clear(state), key=repr)), n - 1, other) == "W":
            return "W"
        if tm == "B" and n < 0 and S(tuple(sorted(clear(state), key=repr)), n + 1, other) == "B":
            return "B"
        for i, c in enumerate(state):
            rest = clear(state[:i] + state[i + 1:])
            for ch in gen(bd, c, tm):
                wp, bp = has_passer(bd, ch, "W"), has_passer(bd, ch, "B")
                if wp and bp:
                    nn, ns = n + (BIG if race_winner(bd, ch, tm, rule) == "W" else -BIG), rest
                elif wp:
                    nn, ns = n + BIG, rest
                elif bp:
                    nn, ns = n - BIG, rest
                else:
                    nn, ns = n, rest + tuple(comps(bd, ch))
                if S(tuple(sorted(ns, key=repr)), nn, other) == tm:
                    return tm
        return other
    def o(p):
        st = tuple(sorted(comps(bd, p), key=repr))
        a, b = S(st, 0, "W"), S(st, 0, "B")
        return "L" if a == b == "W" else "R" if a == b == "B" else ("N" if a == "W" else "P")
    return o

def E_fails(bd, x):
    """count reachable non-terminal nodes with >=2 components and a usable e.p. right"""
    k = 0
    for y in reach(bd, x):
        if y[2] is None or has_passer(bd, y, "W") or has_passer(bd, y, "B"):
            continue
        if len(comps(bd, y)) < 2:
            continue
        side = y[2][2]
        base = (y[0], y[1], None)
        if len(gen(bd, y, side)) > len(gen(bd, base, side)):  # the right adds a capture
            k += 1
    return k

for bk, text, rule in ROWS:
    bd = B(*bk)
    x = parse(text)
    oW, oS, _, _ = make_solvers(bd, rule, 256)
    og = sglob(bd, rule, 256)
    print(f"{bk} {text} [{rule}]  o(S local ep)={oS(x)}  o(S global ep)={og(x)}  o(W)={oW(x)}  "
          f"(E)-violating nodes={E_fails(bd, x)}", flush=True)
