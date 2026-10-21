"""Sanity checks of mine.py and race-rule / e.p.-rule variants (verifier run 2).

Imports only mine.py (this verifier's own code).
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  PYTHONPATH=. .venv/bin/python verify/sumtest/C2-refute/run2/sanity_and_variants.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mine  # noqa: E402
from mine import REF, STAR2, norm, outcome, parse, vector, configure  # noqa: E402

E = frozenset()


def ref_vec(G):
    return "".join(outcome(E, E, norm(G + X)) for _, X in REF)


configure(files=1, ep=False, aware=False, scope="local", race="count")
VEC = {n: ref_vec(X) for n, X in REF}
print("Reference vectors (game alone + X):")
for n, _ in REF:
    print(f"  {n:6s} {VEC[n]}")

# textbook sanity: X + X has outcome P for each X (X - X = 0 only for X = -X games;
# here check the identities that must hold)
print("*2+*2 outcome:", outcome(E, E, norm((STAR2, STAR2))), "(expect P)")
print("up+down outcome:", outcome(E, E, norm((mine.UP, mine.DOWN))), "(expect P)")
print("1/2+1/2-1 outcome:", outcome(E, E, norm((mine.HALF, mine.HALF, mine.MONE))), "(expect P)")
print("+-1 + +-1 outcome:", outcome(E, E, norm((mine.PM1, mine.PM1))), "(expect P)")

checks = [
    (1, "W: a4 / B: a6", "*"),     # either side blocks: {0|0}
    (1, "W: a2 / B: a5", "up"),    # hand: {0 | *}? verify by vector
    (1, "W: a4 / B: a5", "0"),     # blocked, no moves
]
for files, pos, name in checks:
    configure(files=files, ep=True, aware=False, scope="local", race="count")
    W, B = parse(pos)
    v = vector(W, B)
    print(f"{files}-file {pos}: {v}  equals {name}'s vector: {v == VEC[name]}")

# 2-file: W a2 / B b3 -> White a2xb3 makes b3 passed? and Black b3xa2 is passed: +-BIG
configure(files=2, ep=True, aware=False, scope="local", race="count")
W, B = parse("W: a2 / B: b3")
print("2-file W a2 / B b3:", vector(W, B), "(expect all N: +-BIG)")

# --- variants on the candidate
W, B = parse("W: a2 c2 / B: b7 d7")
target = VEC["*2"]
zero = VEC["0"]


def run(label, **kw):
    configure(files=4, **kw)
    v = vector(W, B)
    tag = "*2" if v == target else ("0" if v == zero else "other")
    print(f"{label:60s} {v}  -> {tag}")


print("\nCandidate under variants:")
orig_dist = mine.dist
orig_cap = mine.ep_capture_possible
for ep, aware, scope in ((False, False, "local"), (True, False, "local"), (True, False, "global")):
    # count with ties to the mover
    def dist_ties_mover(side, W_, B_, ep_):
        return orig_dist(side, W_, B_, ep_)
    configure(files=4)
    # ties to mover: emulate by adding 0.5 to the opponent's distance
    mine.dist = lambda side, W_, B_, ep_, _o=orig_dist: _o(side, W_, B_, ep_)
    run(f"count (spec) ep={ep} aware={aware} {scope}", ep=ep, aware=aware, scope=scope, race="count")

    def terminal_variant(W_, B_, ep_, mover, variant):
        wp = mine.has_passer("W", W_, B_, ep_)
        bp = mine.has_passer("B", W_, B_, ep_)
        if wp and bp:
            opp = mine.OTHER[mover]
            if variant == "ties_mover":
                return opp if orig_dist(opp, W_, B_, ep_) < orig_dist(mover, W_, B_, ep_) else mover
            if variant == "no_credit":
                saved = mine.C.ranks
                # recompute without the double-step credit
                def d(side):
                    best = 10 ** 6
                    occ = W_ | B_
                    for p in (W_ if side == "W" else B_):
                        if not mine.pawn_passed(p, side, W_, B_, ep_):
                            continue
                        f, r = p
                        if side == "W":
                            if any((f, s) in occ for s in range(r + 1, saved + 1)):
                                continue
                            best = min(best, saved - r)
                        else:
                            if any((f, s) in occ for s in range(1, r)):
                                continue
                            best = min(best, r - 1)
                    return best
                return opp if d(opp) <= d(mover) else mover
            if variant == "white":
                return "W"
            if variant == "black":
                return "B"
        if wp:
            return "W"
        if bp:
            return "B"
        return None

    orig_terminal = mine.terminal
    for variant in ("ties_mover", "no_credit", "white", "black"):
        mine.terminal = lambda W_, B_, ep_, mover, _v=variant: terminal_variant(W_, B_, ep_, mover, _v)
        run(f"race={variant} ep={ep} aware={aware} {scope}", ep=ep, aware=aware, scope=scope)
    mine.terminal = orig_terminal

# opponent rule with a stricter e.p. variant: double-stepped pawn never passed while
# any e.p. right on it exists, capturable or not
print()
mine.ep_capture_possible = lambda W_, B_, ep_: ep_ is not None
for scope in ("local", "global"):
    for race in ("opponent", "count", "mover"):
        run(f"{race}, ep on, strict-aware (any live right), {scope}", ep=True, aware=True, scope=scope, race=race)
mine.ep_capture_possible = orig_cap
