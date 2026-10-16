"""Distribution of (d_mover - d_opp) over the promotion-race nodes in the game
tree of the *2 candidate W a2 c2 / B b7 d7 (files a-d, 8 ranks, e.p. on),
using the independent move generator / passed test / distance of indep_race.py
(no cylcgt import).  The CGT tree lets either side move at any node, so we
enumerate every position reachable by ANY sequence of pawn moves that never
passes through a decided node (one side passed, or a race).

    cd /Users/aritro/Downloads/Research/Chessendgames && \
      .venv/bin/python -I verify/engines/C3-refute/star2_races.py
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import indep_race as I  # noqa: E402  (our own module, not the worker's)


def sqs(t):
    return frozenset((I.FILES.index(x[0]), int(x[1:])) for x in t.split())


def main():
    W0, B0 = sqs("a2 c2"), sqs("b7 d7")
    # state: (W, B, ep_square, side_allowed_to_capture_ep)
    start = (W0, B0, None, None)
    seen = {start}
    stack = [start]
    races = {}  # (W', B', mover) -> diff
    while stack:
        W, B, ep, epside = stack.pop()
        for side in "WB":
            e = ep if epside == side else None
            for u in I.gen_moves(side, W, B, e):
                W2, B2, ep2 = I.apply_uci(u, side, W, B, e)
                wp, bp = I.has_passer("W", W2, B2), I.has_passer("B", W2, B2)
                if wp and bp:
                    other = "B" if side == "W" else "W"
                    races[(W2, B2, side)] = I.distance(side, W2, B2) - I.distance(other, W2, B2)
                    continue
                if wp or bp:
                    continue
                st = (W2, B2, ep2, ("B" if side == "W" else "W") if ep2 else None)
                if st not in seen:
                    seen.add(st)
                    stack.append(st)
    print(f"non-terminal positions reachable (any move order): {len(seen)}")
    print(f"distinct race nodes (child position, mover): {len(races)}")
    c = collections.Counter(races.values())
    for k in sorted(c):
        print(f"  d_mover - d_opp = {k:+d}: {c[k]}")
    near = c[0] + c[-1]
    print(f"near-ties (diff 0 or -1, i.e. both sides queen on consecutive plies): {near}/{len(races)}")


if __name__ == "__main__":
    main()


def ep_races():
    """Race nodes created by a double step that the opponent can at once capture e.p.;
    report the count-rule verdict there, and whether the e.p. capture leaves the
    opponent as the only side with a passer (then the 'race' is really a loss for the mover)."""
    W0, B0 = sqs("a2 c2"), sqs("b7 d7")
    start = (W0, B0, None, None)
    seen, stack, out = {start}, [start], {}
    while stack:
        W, B, ep, epside = stack.pop()
        for side in "WB":
            e = ep if epside == side else None
            for u in I.gen_moves(side, W, B, e):
                W2, B2, ep2 = I.apply_uci(u, side, W, B, e)
                wp, bp = I.has_passer("W", W2, B2), I.has_passer("B", W2, B2)
                other = "B" if side == "W" else "W"
                if wp and bp:
                    if ep2:
                        caps = [v for v in I.gen_moves(other, W2, B2, ep2)
                                if I.FILES.index(v[2]) == ep2[0] and int(v[3]) == ep2[1] and v[0] != v[2]]
                        res = []
                        for v in caps:
                            W3, B3, _ = I.apply_uci(v, other, W2, B2, ep2)
                            res.append((I.has_passer(side, W3, B3), I.has_passer(other, W3, B3)))
                        cnt = "opp" if I.distance(other, W2, B2) <= I.distance(side, W2, B2) else "mover"
                        out[(W2, B2, side)] = (cnt, tuple(res))
                    continue
                if wp or bp:
                    continue
                st = (W2, B2, ep2, other if ep2 else None)
                if st not in seen:
                    seen.add(st)
                    stack.append(st)
    print(f"\nrace nodes with a pending e.p. capture: {len(out)}")
    c = collections.Counter((cnt, res) for cnt, res in out.values())
    for k, v in sorted(c.items(), key=str):
        print(f"  count-rule winner={k[0]:5s} e.p.-capture outcomes (mover passed?, opp passed?)={k[1]}: {v}")


if __name__ == "__main__":
    ep_races()
