"""Independent re-implementation of the C7 freeze test (verifier scratch).

Written from scratch: own pawn move generator, own passed test, own
placement enumeration, own king/pawn attack sets.  Does not import cylcgt.

Run:
  cd /Users/aritro/Downloads/Research/Chessendgames && \
  .venv/bin/python verify/cylatlas/C7-reproduce/indep_freeze.py
"""
from __future__ import annotations
import itertools, json, sys
from collections import deque

FILES = "abcdefghijklmnop"

# ---------------------------------------------------------------- pawn game
def passed_side(W, B, width, side, wrap=False, ep=None, ep_aware=False):
    """Textbook passed test; ep_aware: a pawn that can be taken e.p. right now
    (by the opponent, who is the one holding the ep right) is not passed."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    for (f, r) in mine:
        if ep_aware and ep is not None and ep[1] == (f, r) and ep[2] != side:
            continue
        adj = {f}
        for d in (-1, 1):
            g = f + d
            if wrap:
                adj.add(g % width)
            elif 0 <= g < width:
                adj.add(g)
        ok = True
        for (g, s) in theirs:
            if g in adj and ((side == "W" and s > r) or (side == "B" and s < r)):
                ok = False
                break
        if ok:
            return True
    return False


def gen(W, B, ep, side, width, ranks=8, with_ep=True):
    """Yield (W', B', ep') after one move of `side`. ep=(target, victim, who_may_capture)."""
    mine, theirs = (W, B) if side == "W" else (B, W)
    occ = W | B
    d = 1 if side == "W" else -1
    home = 2 if side == "W" else ranks - 1
    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not (1 <= r1 <= ranks):
            continue
        if (f, r1) not in occ:
            yield rest | {(f, r1)}, theirs, None
            r2 = r + 2 * d
            if r == home and (f, r2) not in occ and 1 <= r2 <= ranks:
                e = ((f, r1), (f, r2), "B" if side == "W" else "W") if with_ep else None
                yield rest | {(f, r2)}, theirs, e
        for df in (-1, 1):
            g = f + df
            if not (0 <= g < width):
                continue
            t = (g, r1)
            if t in theirs:
                yield rest | {t}, theirs - {t}, None
            elif ep is not None and ep[2] == side and ep[0] == t:
                yield rest | {t}, theirs - {ep[1]}, None


def swap(side, a, b):
    return (a, b) if side == "W" else (b, a)


def reach_any_order(W0, B0, width, with_ep=True, ep_aware=False, include_terminal=True):
    start = (frozenset(W0), frozenset(B0), None)
    seen = {start}
    dq = deque([start])
    while dq:
        W, B, ep = dq.popleft()
        if passed_side(W, B, width, "W", ep=ep, ep_aware=ep_aware) or \
           passed_side(W, B, width, "B", ep=ep, ep_aware=ep_aware):
            continue
        for side in "WB":
            # an ep right is only usable by the immediately-next move of the right holder
            ep_use = ep if (ep is not None and ep[2] == side) else None
            for m, t, e in gen(W, B, ep_use, side, width, with_ep=with_ep):
                nW, nB = swap(side, m, t)
                k = (frozenset(nW), frozenset(nB), e)
                if k not in seen:
                    seen.add(k)
                    dq.append(k)
    out = set()
    for W, B, ep in seen:
        term = passed_side(W, B, width, "W", ep=ep, ep_aware=ep_aware) or \
               passed_side(W, B, width, "B", ep=ep, ep_aware=ep_aware)
        if term and not include_terminal:
            continue
        out.add((W, B))
    return out


def reach_alternating(W0, B0, width, first, with_ep=True):
    """Only strictly alternating play from `first` to move (single component +
    frozen trebuchet: any non-component move is a king move)."""
    start = (frozenset(W0), frozenset(B0), None, first)
    seen = {start}
    dq = deque([start])
    while dq:
        W, B, ep, side = dq.popleft()
        if passed_side(W, B, width, "W") or passed_side(W, B, width, "B"):
            continue
        ep_use = ep if (ep is not None and ep[2] == side) else None
        for m, t, e in gen(W, B, ep_use, side, width, with_ep=with_ep):
            nW, nB = swap(side, m, t)
            k = (frozenset(nW), frozenset(nB), e, "B" if side == "W" else "W")
            if k not in seen:
                seen.add(k)
                dq.append(k)
    return {(W, B) for W, B, _, _ in seen}

# ---------------------------------------------------------------- 8-file board
N = 8


def king_nbrs(k, wrap):
    f, r = k
    s = set()
    for df, dr in itertools.product((-1, 0, 1), repeat=2):
        if df == 0 and dr == 0:
            continue
        g, q = f + df, r + dr
        if wrap:
            g %= N
        if 0 <= g < N and 1 <= q <= 8:
            s.add((g, q))
    return s


def pawn_targets(p, colour, wrap):
    f, r = p
    q = r + (1 if colour == "W" else -1)
    s = set()
    for df in (-1, 1):
        g = f + df
        if wrap:
            g %= N
        if 0 <= g < N:
            s.add((g, q))
    return s


def all_placements(width):
    """Trebuchet pawns on g (file 6) ranks r / r+1; kings on f/h in both
    orientations; component of `width` files inside a..e (files 0..4) at any
    offset, mirrored or not."""
    for off in range(0, 5 - width + 1):
        for mir in (False, True):
            for s in (1, -1):
                for r in range(2, 7):
                    wk = ((6 + s) % N, r + 1)
                    bk = ((6 - s) % N, r)
                    yield off, mir, s, r, wk, bk


def classify(nodes, width, off, mir, wk, bk, wrap):
    mp = (lambda c: off + width - 1 - c) if mir else (lambda c: off + c)
    wkn, bkn = king_nbrs(wk, wrap), king_nbrs(bk, wrap)
    kinds = set()
    for W, B in nodes:
        for (f, q) in W:
            sq = (mp(f), q)
            if sq in bkn:
                kinds.add("Wpawn_adjacent_BK")
            if bk in pawn_targets(sq, "W", wrap):
                kinds.add("Wpawn_checks_BK")
        for (f, q) in B:
            sq = (mp(f), q)
            if sq in wkn:
                kinds.add("Bpawn_adjacent_WK")
            if wk in pawn_targets(sq, "B", wrap):
                kinds.add("Bpawn_checks_WK")
    return kinds


def run(label, nodes, width):
    res = {}
    for wrap in (False, True):
        ok = 0
        tot = 0
        check_fail = 0
        adj_only = 0
        okl = []
        for off, mir, s, r, wk, bk in all_placements(width):
            tot += 1
            k = classify(nodes, width, off, mir, wk, bk, wrap)
            if not k:
                ok += 1
                okl.append((off, mir, s, r))
            elif any("checks" in x for x in k):
                check_fail += 1
            else:
                adj_only += 1
        res["cyl8" if wrap else "flat8"] = dict(ok=ok, total=tot, fail_with_check=check_fail,
                                                fail_adjacency_only=adj_only,
                                                ok_offsets=sorted({o for o, *_ in okl}))
    print(label, len(nodes), json.dumps(res))
    return res


if __name__ == "__main__":
    W0 = [(0, 2), (2, 2)]
    B0 = [(1, 7), (3, 7)]
    width = 4
    n_any = reach_any_order(W0, B0, width)
    run("any-order, ep on, textbook passed, terminals included:", n_any, width)
    run("any-order, ep on, terminals EXCLUDED:", reach_any_order(W0, B0, width, include_terminal=False), width)
    run("any-order, ep off:", reach_any_order(W0, B0, width, with_ep=False), width)
    run("any-order, ep on, ep-aware passed test:", reach_any_order(W0, B0, width, ep_aware=True), width)
    for first in "WB":
        run(f"alternating, {first} first, ep on:", reach_alternating(W0, B0, width, first), width)
    # the start position alone
    run("start position only:", {(frozenset(W0), frozenset(B0))}, width)
    # proposed FEN placement: off=0, mir=False, s=-1, r=4 (WK f5, BK h4)
    for wrap in (False, True):
        k = classify(n_any, width, 0, False, (5, 5), (7, 4), wrap)
        print("proposed FEN placement", "cyl8" if wrap else "flat8", sorted(k))
    # 1.a3 from the proposed FEN on the cylinder
    print("a3 attacks (cyl):", sorted(pawn_targets((0, 3), "W", True)), "BK at (7,4)")
    print("h4 king nbrs (cyl):", sorted(king_nbrs((7, 4), True)))
