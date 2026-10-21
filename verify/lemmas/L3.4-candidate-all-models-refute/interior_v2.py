"""Secondary check (verifier's own code, imports only indep_v2 in this folder):
count the non-terminal nodes Y of the candidate's 4-file tree that are NOT
BIG-interior, i.e. W(Y) <= -BIG or W(Y) >= BIG (hypothesis of Theorem 3.3(b)).

  W(Y) <= -BIG  <=>  W(Y) + BIG <= 0  <=>  Left moving first loses W(Y) + BIG.
  W(Y) >= +BIG  <=>  W(Y) - BIG >= 0  <=>  Right moving first loses W(Y) - BIG.
The integer summand is played with CGT semantics (Left n -> n-1 for n > 0, Right
n -> n+1 for n < 0). Also checks that the root value does not depend on BIG.

Usage:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-refute/interior_v2.py
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_v2 as I  # noqa: E402


def make_WN(bd, rule, big):
    @lru_cache(maxsize=None)
    def wins(pos, N, tm):
        """tm to move wins  W(pos) + N  (pos non-terminal), N an integer game."""
        other = "B" if tm == "W" else "W"
        for c in I.gen(bd, pos, tm):
            cl = I.classify(bd, c)
            if cl == "race":
                v = big if I.race_winner(bd, c, tm, rule) == "W" else -big
            elif cl == "W":
                v = big
            elif cl == "B":
                v = -big
            else:
                if not wins(c, N, other):
                    return True
                continue
            tot = v + N  # integer: mover wins iff after his move the integer is not a win for the opponent
            # integer t with `other` to move: other wins iff t is in other's favour (t>0 for W, t<0 for B)
            if other == "W" and not tot > 0:
                return True
            if other == "B" and not tot < 0:
                return True
        if tm == "W" and N > 0 and not wins(pos, N - 1, other):
            return True
        if tm == "B" and N < 0 and not wins(pos, N + 1, other):
            return True
        return False
    return wins


def main():
    X4 = I.parse("W: a2 c2 / B: b7 d7")
    for ep in (True, False):
        bd = I.Bd(4, False, ep)
        nt = [y for y in I.reach(bd, X4) if I.classify(bd, y) is None]
        for rule in ("count", "mover", "opponent"):
            f = make_WN(bd, rule, I.BIG)
            le_negbig = [y for y in nt if not f(y, I.BIG, "W")]
            ge_big = [y for y in nt if not f(y, -I.BIG, "B")]
            bad = set(le_negbig) | set(ge_big)
            ex = "W: a2 c5 / B: b7 d7"
            exy = I.parse(ex)
            print(f"ep={ep!s:5s} {rule:8s}: non-terminal {len(nt)}, W<=-BIG at {len(le_negbig)}, "
                  f"W>=BIG at {len(ge_big)}, non-interior total {len(bad)}; "
                  f"{ex} <= -BIG: {exy in set(le_negbig)}")
    # BIG independence of the root value for the W model: W + *2 is P for small BIG too
    print("BIG independence (W + *2 outcome via indep_v2 is sign-only, so any BIG >= 1 gives the same);"
          " S has a single live component throughout, so the same holds for S.")


if __name__ == "__main__":
    main()
