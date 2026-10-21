"""Exact necessity / sufficiency statements for L4.2 via MONOTONICITY (verifier scratch).

Fact (standard CGT): if A' >= A then {A', ... | ...} >= {A, ... | ...} and
{... | A', ...} >= {... | A, ...}. W (and WF) is built from the race scores +-BIG by
cgt.make over a DAG, so by induction the root value is an order-preserving function
of the race-verdict vector (order: "White wins" > "Black wins" on every coordinate).
Hence for any partial assignment P, every completion has value v with
    v_lo(P) <= v <= v_hi(P),   v_lo = rest all "B wins", v_hi = rest all "W wins".
So if NOT(v_lo <= *2) or NOT(*2 <= v_hi), no completion of P has value *2 (exact).
If v_lo = v_hi = *2, every completion has value *2 (exact sufficiency).

Checks:
 1. For every race k: P = {k: flipped away from count}. Is *2 still reachable in
    principle (bounds), i.e. is the count verdict of k individually NECESSARY for *2?
 2. P = {4 critical races won by the mover}: v_lo, v_hi (is P sufficient?).
 3. Global bounds: all races W-wins / all B-wins.
 4. Monotonicity sanity check on random pairs of assignments a <= a'.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/lemmas/L4.2-critical-races-theory/necessity.py
"""
import random
import sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import race_winner
from lemmas.test_L4_races import race_nodes, W_override

sys.path.insert(0, "verify/lemmas/L4.2-critical-races-theory")
from wf_sensitivity import WF_override, key  # noqa: E402

other = lambda m: "B" if m == "W" else "W"
STAR2 = cgt.nimber(2)

CRIT = {("W: a2 b5 / B: d7", "W"), ("W: a2 / B: c4 d7", "B"),
        ("W: a3 b5 / B: d6", "W"), ("W: a3 / B: c4 d6", "B")}


def main(ep):
    b = Board(4, 8, False, ep)
    x = Pos.parse("W: a2 c2 / B: b7 d7")
    races = sorted(race_nodes(b, x), key=key)
    crit = [k for k in races if (str(k[0]), k[1]) in CRIT]
    assert len(crit) == 4
    print(f"=== e.p. {'on' if ep else 'off'}: {len(races)} race nodes")
    for name, F in (("W", W_override), ("WF", WF_override)):
        v = lambda ov: F(b, x, "count", ov, {})
        allW = v({k: "W" for k in races})
        allB = v({k: "B" for k in races})
        print(f"  [{name}] all races won by White: {cgt.show(allW)}; all won by Black: {cgt.show(allB)}")
        # 1. individual necessity
        nec = []
        for k in races:
            w = race_winner(b, k[0], k[1], "count")
            P = {k: other(w)}
            lo = v({**{j: "B" for j in races}, **P})
            hi = v({**{j: "W" for j in races}, **P})
            reachable = cgt.le(lo, STAR2) and cgt.le(STAR2, hi)
            if not reachable:
                nec.append((str(k[0]), k[0].ep, k[1], w, cgt.show(lo), cgt.show(hi)))
        print(f"  [{name}] races whose count verdict is NECESSARY for *2 (bounds exclude *2 when flipped): {len(nec)}")
        for t in nec:
            print("       ", t)
        # 2. sufficiency of the 4 critical races
        P = {k: k[1] for k in crit}
        lo = v({**{j: "B" for j in races}, **P})
        hi = v({**{j: "W" for j in races}, **P})
        print(f"  [{name}] 4 critical won by mover: completions lie in [{cgt.show(lo)}, {cgt.show(hi)}]; "
              f"sufficient = {lo is STAR2 and hi is STAR2}")
        # 3b. 4 critical lost by the mover
        P = {k: other(k[1]) for k in crit}
        lo = v({**{j: "B" for j in races}, **P})
        hi = v({**{j: "W" for j in races}, **P})
        print(f"  [{name}] 4 critical LOST by mover: completions in [{cgt.show(lo)}, {cgt.show(hi)}]; "
              f"*2 excluded = {not (cgt.le(lo, STAR2) and cgt.le(STAR2, hi))}")
        # each critical lost individually, others free (incl. other 3 critical)
        for k in crit:
            P = {k: other(k[1])}
            lo = v({**{j: "B" for j in races}, **P})
            hi = v({**{j: "W" for j in races}, **P})
            print(f"  [{name}]   {str(k[0]):20s} lost by mover {k[1]}, all else free: [{cgt.show(lo)}, {cgt.show(hi)}]; "
                  f"*2 excluded = {not (cgt.le(lo, STAR2) and cgt.le(STAR2, hi))}")
    # 4. monotonicity sanity check
    rng = random.Random(3)
    bad = 0
    for _ in range(40):
        a = {k: rng.choice("WB") for k in races}
        a2 = dict(a)
        for k in rng.sample(races, 10):
            a2[k] = "W"
        va, va2 = W_override(b, x, "count", a, {}), W_override(b, x, "count", a2, {})
        if not cgt.le(va, va2):
            bad += 1
    print(f"  monotonicity sanity check (40 random pairs a <= a'): violations {bad}")


if __name__ == "__main__":
    for ep in (True, False):
        main(ep)
