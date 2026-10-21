"""Theory-lens check of the e.p. caveat in claim L3.4 (no project code).

The claim says W(X) = *2 "with e.p. on". The textbook passed test counts a pawn
that has just double-stepped past an enemy pawn as passed, so the game ends
(+-BIG) before the opponent's legal e.p. capture can be played. Here the
passed test is made e.p.-aware: a pawn that may be taken e.p. right now (it is
the pawn of the live right and an enemy pawn stands beside it) is NOT passed.
This is the convention RESULTS.md says the project adopted on 2026-10-16.

Method (CGT-free): G = H  <=>  G + (-H) is a second-player win (P).
Reference games: *k, and K = {2+-1 | -2+-1} (= -K), which RESULTS.md reports.

Run (from this directory):
  PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python epaware_check.py
"""
import sys, time
sys.path.insert(0, ".")
import indep
from indep import Bd, parse, nim, ZERO, STAR, add, outcome, reachable, _cls


def ep_capturable(bd, p, side, pawn):
    W, B, ep = p
    if ep is None or ep[1] != pawn or ep[2] == side:
        return False
    f, r = pawn
    theirs = B if side == "W" else W
    return any((g, r) in theirs for g in bd.adj(f))


def make_term(aware):
    def is_passed_p(bd, p, side, pawn):
        W, B, _ = p
        if not indep.is_passed(bd, W, B, side, pawn):
            return False
        return not (aware and ep_capturable(bd, p, side, pawn))

    def has_passer_p(bd, p, side):
        mine = p[0] if side == "W" else p[1]
        return any(is_passed_p(bd, p, side, x) for x in mine)

    def term(bd, p):
        a, b = has_passer_p(bd, p, "W"), has_passer_p(bd, p, "B")
        if a and b: return "race"
        if a: return "W"
        if b: return "B"
        return None

    def dist(bd, p, side):
        W, B, _ = p
        best = 10**6
        for (f, r) in (W if side == "W" else B):
            if not is_passed_p(bd, p, side, (f, r)):
                continue
            if side == "W":
                d = bd.ranks - r - (1 if (r == 2 and bd.ranks >= 4) else 0)
            else:
                d = r - 1 - (1 if (r == bd.ranks - 1 and bd.ranks >= 4) else 0)
            best = min(best, d)
        return best
    return term, dist


def integer(n):
    g = ZERO
    for _ in range(abs(n)):
        g = ((g,), ()) if n > 0 else ((), (g,))
    return g


def pm(a, b):            # {a | b} for integers a > b
    return ((integer(a),), (integer(b),))


K = ((pm(3, 1),), (pm(-1, -3),))          # {2+-1 | -2+-1}
REFS = {"*0": ZERO, "*1": STAR, "*2": nim(2), "*3": nim(3), "{2+-1|-2+-1}": K}

X4 = parse("W: a2 c2 / B: b7 d7")
X8 = parse("W: a2 c2 g4 / B: b7 d7 g5")
t0 = time.time()
for aware in (False, True):
    indep.term, indep.dist = make_term(aware)
    for ep in (True, False):
        for files, X in ((4, X4), (8, X8)):
            bd = Bd(files, 8, False, ep)
            for rule in ("count", "mover", "opponent"):
                row = {name: outcome(bd, X, h, rule) for name, h in REFS.items()}
                eq = [n for n, o in row.items() if o == "P"]
                print(f"test={'e.p.-aware' if aware else 'textbook  '} ep={ep!s:5} files={files} rule={rule:8} "
                      f"o(X + R): {row}  => X = {eq[0] if eq else 'none of the references'}", flush=True)
    # tree facts under this test, 4-file strip
    for ep in (True, False):
        bd = Bd(4, 8, False, ep)
        R = reachable(bd, X4)
        nt = [y for y in R if indep.term(bd, y) is None]
        split = [y for y in nt if indep.n_components(bd, y) > 1]
        print(f"   [{'aware' if aware else 'textbook'}] ep={ep}: reachable {len(R)}, non-terminal {len(nt)}, "
              f"non-terminal with >=2 components: {len(split)}")
print("time %.1fs" % (time.time() - t0))
