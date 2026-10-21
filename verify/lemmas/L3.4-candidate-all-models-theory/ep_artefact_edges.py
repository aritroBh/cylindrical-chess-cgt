"""Count the edges of the candidate's e.p.-on tree (textbook passed test) that end
the game at +-BIG although the opponent still has a legal e.p. capture of the
'passed' pawn. No project code.
Run: PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python ep_artefact_edges.py"""
import sys
sys.path.insert(0, ".")
from indep import Bd, parse, gen, term, reachable, fmt


def ep_capturable(bd, p, side, pawn):
    W, B, ep = p
    if ep is None or ep[1] != pawn or ep[2] == side:
        return False
    f, r = pawn
    theirs = B if side == "W" else W
    return any((g, r) in theirs for g in bd.adj(f))

bd = Bd(4, 8, False, True)
X = parse("W: a2 c2 / B: b7 d7")
R = reachable(bd, X)
edges = []
for y in R:
    if term(bd, y) is not None:
        continue
    for side in "WB":
        for c in gen(bd, y, side):
            t = term(bd, c)
            if t is None or c[2] is None:
                continue
            # the moved pawn is c[2][1]; is it the (or a) reason the child is terminal, and e.p.-capturable?
            if ep_capturable(bd, c, side, c[2][1]):
                edges.append((fmt(y), side, fmt(c), t))
print(f"edges into a terminal child whose double-stepped pawn is still e.p.-capturable: {len(edges)}")
for e in sorted(edges)[:12]:
    print("  from", e[0], "| mover", e[1], "| child", e[2], "| textbook verdict", e[3])

# refine: edges whose terminal verdict actually changes under the e.p.-aware test
import indep
def term_aware(bd, p):
    W, B, ep = p
    def hp(side):
        mine = W if side == "W" else B
        return any(indep.is_passed(bd, W, B, side, x) and not ep_capturable(bd, p, side, x) for x in mine)
    a, b = hp("W"), hp("B")
    return "race" if a and b else "W" if a else "B" if b else None
chg = [(y, s, c, t, term_aware(bd, c)) for (y, s, c, t) in
       [(y, s, c, t) for y in R if term(bd, y) is None for s in "WB" for c in gen(bd, y, s) for t in [term(bd, c)] if t is not None]
       if term_aware(bd, c) != t]
print(f"edges (textbook tree, e.p. on) whose terminal verdict changes under the e.p.-aware test: {len(chg)}")
from collections import Counter
print("  (textbook verdict -> aware status):", dict(Counter((t, a) for _, _, _, t, a in chg)))
for y, s, c, t, a in sorted(chg, key=lambda z: fmt(z[0]))[:8]:
    print("  from", fmt(y), "| mover", s, "| child", fmt(c), "| textbook", t, "| aware", a or "non-terminal")
