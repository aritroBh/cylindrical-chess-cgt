"""Third route: compare cylcgt (component-sum model) with sumtest whole-board solver
on descendants of the two disputed roots, race rule 'opponent', e.p.-aware test."""
import sys
sys.path.insert(0, "sumtest")
from cylcgt import pawns, cgt
import sumsolver as S
from lemmas.common import hereditarily_safe

pawns.RACE_RULE = "opponent"; pawns.PASSED_RESPECTS_EP = True; pawns._value.cache_clear()
board = pawns.Board(5, 8, False, True)
geo, rules, T, ref, whole = S.make(5, False, ep=True, race_rule="opponent", mode="whole", ep_aware=True)
names = {0: "FILES"}
def txt(pos):
    f = lambda s: " ".join(f"{'abcde'[a]}{b}" for a, b in sorted(s))
    return f"W: {f(pos.white)} / B: {f(pos.black)}"
def whole_out(pos, node="0"):
    W, B = geo.parse(txt(pos))
    return whole.outcomes(W, B, [ref[node]])[0]
roots = ["W: a3 b3 c2 e2 / B: a6 c5 d5 e3", "W: a6 b4 c4 e3 / B: a7 c7 d6 e6"]
for rt in roots:
    p0 = pawns.Pos.parse(rt)
    print("ROOT", rt, "cylcgt:", cgt.show(pawns.value(board, p0)), "sum_safe:", pawns.sum_safe(board, p0),
          "HSS:", hereditarily_safe(board, p0))
    # descendants (ep-free states only), whole-board play
    seen = {}; stack = [p0]
    while stack:
        p = stack.pop()
        key = (p.white, p.black, p.ep)
        if key in seen: continue
        seen[key] = p
        if pawns.passed(board, p, "W") or pawns.passed(board, p, "B"): continue
        for side in "WB":
            for q in pawns.moves(board, p, side): stack.append(q)
    bad = []
    for key, p in seen.items():
        if p.ep or pawns.passed(board, p, "W") or pawns.passed(board, p, "B"): continue
        g = pawns.value(board, p)
        c = cgt.outcome(g)          # cylcgt outcome class
        w = whole_out(p)
        cm = {"Left": "L", "Right": "R", "Next": "N", "Previous": "P"}.get(c, c)
        if cm != w: bad.append((len(p.white)+len(p.black), txt(p), cgt.show(g), c, w))
    bad.sort()
    print("  ep-free descendants:", sum(1 for k,p in seen.items() if not p.ep), "outcome mismatches (cylcgt vs whole):", len(bad))
    for b in bad[:6]: print("   ", b)
