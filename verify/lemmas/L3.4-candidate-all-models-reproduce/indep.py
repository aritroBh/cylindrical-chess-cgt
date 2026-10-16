"""Independent re-check of claim L3.4 (the *2 candidate W a2 c2 / B b7 d7).

Written by the verifier from the stated rules only. It imports NOTHING from
cylcgt/, lemmas/ or crosscheck/ (own move generator, passer test, race rules,
and a CGT-free minimax). Values are certified by sum tests:

    G = *2  iff  G + *2 is a second-player win (P), because -*2 = *2;
    G = 0   iff  G is P.

In the sum G + *k a component that reaches +BIG (resp. -BIG) decides the whole
sum, because BIG + *j > 0 for every j. The e.p. right of the component stays
attached to the component while players move in the nim heap (this is the
CGT meaning of the game W as a summand).

Run: cd <root> && .venv/bin/python -I verify/lemmas/L3.4-candidate-all-models-reproduce/indep.py
"""
from __future__ import annotations

import sys
from functools import lru_cache

sys.setrecursionlimit(200000)

BIG = 256


def sq(name):
    return ("abcdefgh".index(name[0]), int(name[1:]))


def mkpos(white, black, ep=None):
    return (frozenset(map(sq, white.split())), frozenset(map(sq, black.split())), ep)


# board = (files, ranks, ep_on)  -- flat boards only

def nbrs(board, f):
    return [g for g in (f - 1, f + 1) if 0 <= g < board[0]]


def is_passed(board, pos, side, p):
    f, r = p
    enemy = pos[1] if side == "W" else pos[0]
    fs = {f, *nbrs(board, f)}
    if side == "W":
        return not any(g in fs and s > r for g, s in enemy)
    return not any(g in fs and s < r for g, s in enemy)


def has_passer(board, pos, side):
    mine = pos[0] if side == "W" else pos[1]
    return any(is_passed(board, pos, side, p) for p in mine)


def term(board, pos):
    w, b = has_passer(board, pos, "W"), has_passer(board, pos, "B")
    if w and b:
        return 0
    if w:
        return 1
    if b:
        return -1
    return None


def gen(board, pos, side):
    """Children after one pawn move of `side`. The right in pos is usable only
    if it belongs to `side`; children carry a fresh right only after a double step."""
    files, ranks, ep_on = board
    white, black, ep = pos
    mine, theirs = (white, black) if side == "W" else (black, white)
    occ = white | black
    d = 1 if side == "W" else -1
    start = 2 if side == "W" else ranks - 1
    my_ep = ep if (ep is not None and ep[2] == side) else None
    other = "B" if side == "W" else "W"
    out = []

    def put(nm, nt, e=None):
        nm, nt = frozenset(nm), frozenset(nt)
        out.append((nm, nt, e) if side == "W" else (nt, nm, e))

    for p in mine:
        f, r = p
        rest = mine - {p}
        r1 = r + d
        if not 1 <= r1 <= ranks:
            continue
        if (f, r1) not in occ:
            put(rest | {(f, r1)}, theirs)
            r2 = r + 2 * d
            if r == start and (f, r2) not in occ:
                put(rest | {(f, r2)}, theirs, ((f, r1), (f, r2), other) if ep_on else None)
        for g in nbrs(board, f):
            t = (g, r1)
            if t in theirs:
                put(rest | {t}, theirs - {t})
            elif my_ep is not None and my_ep[0] == t and my_ep[1] in theirs:
                put(rest | {t}, theirs - {my_ep[1]})
    return list(dict.fromkeys(out))


def pdist(board, pos, side):
    files, ranks, _ = board
    mine = pos[0] if side == "W" else pos[1]
    best = 10 ** 6
    for p in mine:
        f, r = p
        if not is_passed(board, pos, side, p):
            continue
        ahead = [q for q in mine if q[0] == f and ((q[1] > r) if side == "W" else (q[1] < r))]
        if ahead:
            continue
        dd = (ranks - r - (r == 2)) if side == "W" else (r - 1 - (r == ranks - 1))
        best = min(best, dd)
    return best


def race_win(board, pos, mover, rule):
    other = "B" if mover == "W" else "W"
    if rule == "mover":
        return mover
    if rule == "opponent":
        return other
    return other if pdist(board, pos, other) <= pdist(board, pos, mover) else mover


def child_result(board, c, mover, rule):
    """'W'/'B' if the child is decided, None if play continues."""
    t = term(board, c)
    if t == 0:
        return race_win(board, c, mover, rule)
    if t == 1:
        return "W"
    if t == -1:
        return "B"
    return None


@lru_cache(maxsize=None)
def wins(board, pos, heap, stm, rule, kings):
    """True iff `stm` (side to move) wins W(pos) + *heap (WF if kings)."""
    t = term(board, pos)
    assert t != 0
    if t is not None:
        return (t == 1) == (stm == "W")
    other = "B" if stm == "W" else "W"
    for c in gen(board, pos, stm):
        res = child_result(board, c, stm, rule)
        if res is None:
            res = stm if not wins(board, c, heap, other, rule, kings) else other
        if res == stm:
            return True
    for j in range(heap):
        if not wins(board, pos, j, other, rule, kings):
            return True
    # a king move (kings=True) loses at once, so it never wins: nothing to add
    return False


def outcome_sum(board, pos, heap, rule, kings=False):
    a = wins(board, pos, heap, "W", rule, kings)          # Left first
    b = not wins(board, pos, heap, "B", rule, kings)      # Left wins with Right first
    return {(True, True): "L", (False, False): "R", (True, False): "N", (False, True): "P"}[(a, b)]


# ----------------------------------------------------------------- tree facts
def reachable(board, pos):
    seen, stack = {pos}, [pos]
    while stack:
        x = stack.pop()
        if term(board, x) is not None:
            continue
        for side in "WB":
            src = x if (x[2] is None or x[2][2] == side) else (x[0], x[1], None)
            for c in gen(board, src, side):
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
    return seen


def n_components(pos):
    fs = sorted({f for f, _ in pos[0] | pos[1]})
    return 1 + sum(1 for a, b in zip(fs, fs[1:]) if b > a + 1) if fs else 0


# integer-pile sums for the BIG-interior test: W(Y) + n
@lru_cache(maxsize=None)
def wins_int(board, pos, n, stm, rule):
    t = term(board, pos)
    if t is not None:
        tot = (BIG if t == 1 else -BIG) + n
        if tot == 0:
            return False
        return (tot > 0) == (stm == "W")
    other = "B" if stm == "W" else "W"
    for c in gen(board, pos, stm):
        res = child_result(board, c, stm, rule)
        if res is not None:
            tot = (BIG if res == "W" else -BIG) + n
            # mover has just moved; the opponent moves next in an integer
            if tot == 0:
                win = True
            else:
                win = (tot > 0) == (stm == "W")
        else:
            win = not wins_int(board, c, n, other, rule)
        if win:
            return True
    if stm == "W" and n > 0 and not wins_int(board, pos, n - 1, other, rule):
        return True
    if stm == "B" and n < 0 and not wins_int(board, pos, n + 1, other, rule):
        return True
    return False


def le_minus_big(board, y, rule):   # W(y) <= -BIG  iff Left moving first loses W(y)+BIG
    return not wins_int(board, y, BIG, "W", rule)


def ge_big(board, y, rule):         # W(y) >= BIG  iff Right moving first loses W(y)-BIG
    return not wins_int(board, y, -BIG, "B", rule)


if __name__ == "__main__":
    cand4 = mkpos("a2 c2", "b7 d7")
    cand8 = mkpos("a2 c2 g4", "b7 d7 g5")
    ok = True
    print("== sum tests (independent minimax) ==")
    for ep_on in (True, False):
        for files, pos in ((4, cand4), (8, cand8)):
            board = (files, 8, ep_on)
            for rule in ("count", "mover", "opponent"):
                for kings in (False, True):
                    outs = {k: outcome_sum(board, pos, k, rule, kings) for k in range(4)}
                    if rule == "opponent":
                        val = "0" if outs[0] == "P" else "?"
                        expect = "0"
                    else:
                        val = "*2" if outs[2] == "P" else "?"
                        expect = "*2"
                    good = (val == expect and all(outs[k] == "N" for k in range(4)
                                                  if k != (0 if expect == "0" else 2)))
                    ok &= good
                    print(f"ep={ep_on!s:5s} files={files} rule={rule:8s} {'WF' if kings else 'W '}: "
                          f"o(G+*k), k=0..3: {outs} -> G = {val} {'OK' if good else 'MISMATCH'}")
    print("== tree facts (4-file strip) ==")
    for ep_on in (True, False):
        board = (4, 8, ep_on)
        R = reachable(board, cand4)
        nt = [y for y in R if term(board, y) is None]
        split = [y for y in nt if n_components(y) > 1]
        print(f"ep={ep_on}: reachable {len(R)}, non-terminal {len(nt)}, non-terminal with >=2 components {len(split)}")
        for rule in ("count", "mover", "opponent"):
            bad = [y for y in nt if le_minus_big(board, y, rule) or ge_big(board, y, rule)]
            print(f"   rule={rule:8s}: non-terminal nodes with W<=-BIG or W>=BIG: {len(bad)}")
        ex = mkpos("a2 c5", "b7 d7")
        print("   W: a2 c5 / B: b7 d7 reachable:", ex in R,
              " <=-BIG (count):", le_minus_big(board, ex, "count"))
    print("ALL OK" if ok else "SOME MISMATCH")
