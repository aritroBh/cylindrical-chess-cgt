"""Sensitivity check (verifier's own code; imports only indep_v2 in this folder).

1. How many e.p. rights in the candidate's tree are actually usable (a pawn of the
   entitled side can make the e.p. capture)?
2. Does W(X) + *2 stay a second-player win if an e.p. right expires after ANY move,
   including a move in the nim heap (chess-like "next move only" semantics),
   instead of the CGT-form semantics used in the claim (the right lives in the
   component until a move is made there)?

Usage:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-refute/ep_sensitivity_v2.py
"""
import os
import sys
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_v2 as I  # noqa: E402


def make_W_global_expiry(bd, rule, kings):
    @lru_cache(maxsize=None)
    def wins(pos, k, tm):
        other = "B" if tm == "W" else "W"
        for c in I.gen(bd, pos, tm):
            cl = I.classify(bd, c)
            if cl == "race":
                if I.race_winner(bd, c, tm, rule) == tm:
                    return True
                continue
            if cl is not None:
                if cl == tm:
                    return True
                continue
            if not wins(c, k, other):
                return True
        stripped = (pos[0], pos[1], None)
        for j in range(k):
            if not wins(stripped, j, other):
                return True
        return False
    return wins


def main():
    X4 = I.parse("W: a2 c2 / B: b7 d7")
    bd = I.Bd(4, False, True)
    R = I.reach(bd, X4)
    with_right = [y for y in R if y[2] is not None and I.classify(bd, y) is None]
    usable = []
    for y in with_right:
        side = y[2][2]
        plain = (y[0], y[1], None)
        if set(I.gen(bd, y, side)) != set(I.gen(bd, plain, side)):
            usable.append(y)
    print(f"non-terminal positions carrying an e.p. right: {len(with_right)}; right usable: {len(usable)}")
    for y in usable[:10]:
        w = " ".join(sorted(map(I.sqn, y[0])))
        b = " ".join(sorted(map(I.sqn, y[1])))
        print(f"   W: {w} / B: {b}  ep target {I.sqn(y[2][0])} for {y[2][2]}")
    for rule in ("count", "mover", "opponent"):
        for kings in (False, True):
            f = make_W_global_expiry(bd, rule, kings)
            oc = "".join(I.outcome_from(f, X4, k) for k in range(4))
            print(f"global-expiry {'WF' if kings else 'W '} {rule:8s}: outcomes of model+*k, k=0..3: {oc}")


if __name__ == "__main__":
    main()
