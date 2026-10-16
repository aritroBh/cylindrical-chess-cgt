"""Theory-lens checks for claim L4.2 (verifier scratch; does not modify worker files).

1. Critical set (single flips) at the MOVER baseline and at the OPPONENT baseline,
   not only at the count baseline.
2. Necessity: with one critical race LOST by its mover, can the value still be *2
   for some assignment of the other races? (random search, deterministic order)
3. Sufficiency gap: with the 4 critical races won by the mover, fraction of random
   assignments of the others giving *2 (deterministic sorted order, so independent
   of PYTHONHASHSEED).
4. Which race nodes are reachable by ALTERNATING play from the root (W first or B
   first) -- only these correspond to real 8x8 chess positions with the side to
   move fixed; the rest occur only in non-alternating (sum) play.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/theory_checks.py
"""
import random, sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import race_winner, terminal, split_ep
from lemmas.test_L4_races import W_override, race_nodes

other = lambda m: "B" if m == "W" else "W"

def alt_race_nodes(b, x):
    """race (child, mover) reachable in strictly alternating play from x, either side first."""
    out = set()
    seen = set()
    stack = [(x, "W"), (x, "B")]
    while stack:
        y, tm = stack.pop()
        if (y, tm) in seen:
            continue
        seen.add((y, tm))
        if terminal(b, y) is not None:
            continue
        lpos, rpos = split_ep(y)
        src = lpos if tm == "W" else rpos
        for c in pawns.moves(b, src, tm):
            t = terminal(b, c)
            if t == 0:
                out.add((c, tm))
            elif t is None:
                stack.append((c, other(tm)))
    return out

def main(ep):
    b = Board(4, 8, False, ep)
    x = Pos.parse("W: a2 c2 / B: b7 d7")
    races = sorted(race_nodes(b, x), key=lambda t: (str(t[0]), str(t[0].ep), t[1]))
    print(f"=== e.p. {'on' if ep else 'off'}: {len(races)} race nodes")
    crit_count = []
    for base in ("count", "mover", "opponent"):
        v0 = W_override(b, x, base, {}, {})
        crit = []
        for c, m in races:
            w = race_winner(b, c, m, base)
            v = W_override(b, x, base, {(c, m): other(w)}, {})
            if v is not v0:
                crit.append((str(c), m, w, cgt.show(v)))
        print(f"  baseline {base}: value {cgt.show(v0)}; single flips that change it: {len(crit)}")
        for t in crit:
            print("     ", t)
        if base == "count":
            crit_count = crit
    critkeys = [(c, m) for c, m in races if any(str(c) == s and m == mm for s, mm, _, _ in crit_count)]
    alt = alt_race_nodes(b, x)
    print(f"  race nodes reachable by alternating play from the root (either side first): {len(alt)} of {len(races)}")
    print(f"  all 4 critical races alternating-reachable: {all(k in alt for k in critkeys)}")
    # critical set restricted to the alternating-reachable races only matters for outcome
    rest = [k for k in races if k not in critkeys]
    # 3. sufficiency gap, deterministic order
    rng = random.Random(20261016)
    hist = {}
    N = 400
    for _ in range(N):
        ov = {k: k[1] for k in critkeys}
        for k in rest:
            ov[k] = rng.choice("WB")
        s = cgt.show(W_override(b, x, "count", ov, {}))
        hist[s] = hist.get(s, 0) + 1
    print(f"  4 critical won by mover, others uniform random ({N} trials, seed 20261016): {hist}")
    # 2. necessity: each critical race lost by mover, others random
    for k in critkeys:
        rng = random.Random(7)
        hist = {}
        for _ in range(N):
            ov = {kk: kk[1] for kk in critkeys}
            ov[k] = other(k[1])
            for kk in rest:
                ov[kk] = rng.choice("WB")
            s = cgt.show(W_override(b, x, "count", ov, {}))
            hist[s] = hist.get(s, 0) + 1
        print(f"  critical {str(k[0])} (mover {k[1]}) LOST by mover, other 3 won, rest random ({N}): {hist}")
    # all 4 lost by mover, rest random
    rng = random.Random(9)
    hist = {}
    for _ in range(N):
        ov = {kk: other(kk[1]) for kk in critkeys}
        for kk in rest:
            ov[kk] = rng.choice("WB")
        s = cgt.show(W_override(b, x, "count", ov, {}))
        hist[s] = hist.get(s, 0) + 1
    print(f"  all 4 critical LOST by mover, rest random ({N}): {hist}")

if __name__ == "__main__":
    for ep in (True, False):
        main(ep)
