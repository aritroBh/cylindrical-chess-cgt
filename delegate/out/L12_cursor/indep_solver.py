#!/usr/bin/env python3
"""Independent pawn-CGT checker for L12 (paper rules only; no repo solvers).

Method: X has value v iff the player to move loses in X + (-v), for both movers.
Passed-pawn test: e.p.-aware (default), textbook, or off.
Race rules: count / mover / opponent. BIG = 256.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import FrozenSet, Optional, Tuple

# --- board / pawns ---
# White moves up (rank+), Black down (rank-). Files 0..files-1.

Sq = Tuple[int, int]  # (file, rank)


@dataclass(frozen=True)
class Board:
    files: int
    ranks: int = 8
    wrap: bool = False  # cylinder


@dataclass(frozen=True)
class Pos:
    white: FrozenSet[Sq]
    black: FrozenSet[Sq]
    ep: Optional[Sq] = None  # square of pawn that may be taken e.p.


# settings
EP_AWARE, EP_TEXTBOOK, EP_OFF = "aware", "textbook", "off"
RACE_COUNT, RACE_MOVER, RACE_OPP = "count", "mover", "opponent"
BIG = 256


def beside(b: Board, f: int, right: bool) -> Optional[int]:
    if right:
        if f + 1 < b.files:
            return f + 1
        return 0 if b.wrap else None
    if f > 0:
        return f - 1
    return (b.files - 1) if b.wrap else None


def occupied(p: Pos) -> FrozenSet[Sq]:
    return p.white | p.black


def home(b: Board, white: bool) -> int:
    return 2 if white else b.ranks - 1


def ahead_rank(white: bool, r: int) -> int:
    return r + 1 if white else r - 1


def is_ahead(white: bool, r: int, s: int) -> bool:
    return r < s if white else s < r


def blocks(b: Board, pf: int, pr: int, white: bool, qf: int, qr: int) -> bool:
    if qf == pf and is_ahead(white, pr, qr):
        return True
    for right in (True, False):
        g = beside(b, pf, right)
        if g is not None and qf == g and is_ahead(white, pr, qr):
            return True
    return False


def textbook_passed(b: Board, p: Pos, white: bool, sq: Sq) -> bool:
    enemies = p.black if white else p.white
    f, r = sq
    return all(not blocks(b, f, r, white, qf, qr) for qf, qr in enemies)


def _ep_targets(b: Board, pos: Pos, double_stepper_white: bool, arrival: Sq) -> list[Sq]:
    """Capturer squares that can e.p.-take the pawn that double-stepped to arrival."""
    skipped = (arrival[0], ahead_rank(not double_stepper_white, arrival[1]))
    caps = []
    capturers = pos.black if double_stepper_white else pos.white
    cap_white = not double_stepper_white
    for cf, cr in capturers:
        for right in (True, False):
            g = beside(b, cf, right)
            if g is None:
                continue
            land_r = ahead_rank(cap_white, cr)
            if (g, land_r) == skipped:
                caps.append((cf, cr))
    return caps


def ep_capturable(b: Board, p: Pos, white: bool, sq: Sq) -> bool:
    """Can the opponent take this pawn (colour `white`) en passant next move?"""
    if p.ep != sq:
        return False
    return bool(_ep_targets(b, p, white, sq))


def is_passed(b: Board, p: Pos, white: bool, sq: Sq, ep_rule: str) -> bool:
    if not textbook_passed(b, p, white, sq):
        return False
    if ep_rule == EP_AWARE and ep_capturable(b, p, white, sq):
        return False
    return True


def has_passed(b: Board, p: Pos, white: bool, ep_rule: str) -> bool:
    side = p.white if white else p.black
    return any(is_passed(b, p, white, sq, ep_rule) for sq in side)


def dist_to_promote(b: Board, sq: Sq, white: bool) -> int:
    f, r = sq
    d = (b.ranks - r) if white else (r - 1)
    if r == home(b, white) and d >= 2:
        return d - 1
    return d


def is_front(p: Pos, sq: Sq, white: bool) -> bool:
    f, r = sq
    for qf, qr in p.white | p.black:
        if qf == f and is_ahead(white, r, qr):
            return False
    return True


def race_distance(b: Board, p: Pos, white: bool, ep_rule: str) -> Optional[int]:
    side = p.white if white else p.black
    ds = [
        dist_to_promote(b, sq, white)
        for sq in side
        if is_passed(b, p, white, sq, ep_rule) and is_front(p, sq, white)
    ]
    return min(ds) if ds else None


def race_winner(b: Board, p: Pos, mover_white: bool, ep_rule: str, race: str) -> bool:
    """Return True if White wins the race."""
    if race == RACE_MOVER:
        return mover_white
    if race == RACE_OPP:
        return not mover_white
    # count: fewer moves wins; tie to non-mover
    dw = race_distance(b, p, True, ep_rule)
    db = race_distance(b, p, False, ep_rule)

    def le_inf(a, c) -> bool:
        if c is None:
            return True
        if a is None:
            return False
        return a <= c

    # if non-mover distance <= mover distance, non-mover wins
    if mover_white:
        # non-mover = black
        if le_inf(db, dw):
            return False
        return True
    else:
        if le_inf(dw, db):
            return True
        return False


def classify(b: Board, p: Pos, mover_white: bool, ep_rule: str, race: str):
    """Return ('open',) | ('decided', white_wins:bool) | """
    pw, pb = has_passed(b, p, True, ep_rule), has_passed(b, p, False, ep_rule)
    if not pw and not pb:
        return ("open",)
    if pw and not pb:
        return ("decided", True)
    if pb and not pw:
        return ("decided", False)
    return ("decided", race_winner(b, p, mover_white, ep_rule, race))


def components(b: Board, p: Pos) -> Tuple[Pos, ...]:
    occ = sorted({f for f, _ in p.white | p.black})
    if not occ:
        return ()
    runs: list[list[int]] = []
    cur = [occ[0]]
    for f in occ[1:]:
        if f == cur[-1] + 1:
            cur.append(f)
        else:
            runs.append(cur)
            cur = [f]
    runs.append(cur)
    if b.wrap and len(runs) >= 2 and runs[0][0] == 0 and runs[-1][-1] == b.files - 1:
        merged = runs[-1] + runs[0]
        runs = [merged] + runs[1:-1]
    out = []
    for fs in runs:
        fs_set = set(fs)
        w = frozenset(sq for sq in p.white if sq[0] in fs_set)
        bl = frozenset(sq for sq in p.black if sq[0] in fs_set)
        ep = p.ep if (p.ep and p.ep[0] in fs_set) else None
        out.append(Pos(w, bl, ep))
    return tuple(out)


def moves(b: Board, p: Pos, white: bool, ep_rule: str) -> list[Pos]:
    mine = p.white if white else p.black
    theirs = p.black if white else p.white
    occ = occupied(p)
    results: list[Pos] = []
    seen = set()

    def emit(nw, nb, ep):
        q = Pos(frozenset(nw), frozenset(nb), ep)
        key = (q.white, q.black, q.ep)
        if key not in seen:
            seen.add(key)
            results.append(q)

    for f, r in mine:
        # single
        r1 = ahead_rank(white, r)
        if 1 <= r1 <= b.ranks and (f, r1) not in occ:
            nm = (mine - {(f, r)}) | {(f, r1)}
            if white:
                emit(nm, theirs, None)
            else:
                emit(theirs, nm, None)
            # double
            if r == home(b, white):
                r2 = ahead_rank(white, r1)
                if 1 <= r2 <= b.ranks and (f, r2) not in occ:
                    nm2 = (mine - {(f, r)}) | {(f, r2)}
                    after_w = nm2 if white else theirs
                    after_b = theirs if white else nm2
                    after = Pos(frozenset(after_w), frozenset(after_b), None)
                    ep = None
                    if ep_rule != EP_OFF and _ep_targets(b, after, white, (f, r2)):
                        ep = (f, r2)
                    emit(after_w, after_b, ep)
        # captures
        for right in (True, False):
            g = beside(b, f, right)
            if g is None:
                continue
            tr = ahead_rank(white, r)
            if not (1 <= tr <= b.ranks):
                continue
            tgt = (g, tr)
            if tgt in theirs:
                nm = (mine - {(f, r)}) | {tgt}
                nt = theirs - {tgt}
                if white:
                    emit(nm, nt, None)
                else:
                    emit(nt, nm, None)
        # en passant
        if p.ep is not None and ep_rule != EP_OFF and p.ep in theirs:
            ep_owner_white = not white
            skipped = (p.ep[0], ahead_rank(not ep_owner_white, p.ep[1]))
            for right in (True, False):
                g = beside(b, f, right)
                if g is None:
                    continue
                land_r = ahead_rank(white, r)
                if (g, land_r) == skipped:
                    nm = (mine - {(f, r)}) | {skipped}
                    nt = theirs - {p.ep}
                    if white:
                        emit(nm, nt, None)
                    else:
                        emit(nt, nm, None)
    return results


# --- CGT trees ---
# Represent reference trees as nested tuples: ('node', left_tuple, right_tuple)
# star(k), dy(k) for 1/2^k


def t_zero():
    return ("node", (), ())


def t_star(k: int):
    def stars_list(n):
        if n == 0:
            return ()
        prev = stars_list(n - 1)
        return prev + (("node", prev, prev),)

    opts = stars_list(k)
    return ("node", opts, opts)


def t_dy(k: int):
    if k == 0:
        return ("node", (t_zero(),), ())
    return ("node", (t_zero(),), (t_dy(k - 1),))


def t_neg(t):
    tag, L, R = t
    return ("node", tuple(t_neg(x) for x in R), tuple(t_neg(x) for x in L))


# Sum position: list of components; each is ('p', Pos) | ('n', int) | ('t', tree)


def norm_comps(cs):
    n = 0
    rest = []
    for c in cs:
        if c[0] == "n":
            n += c[1]
        elif c[0] == "t" and c[1] == t_zero():
            continue
        else:
            rest.append(c)
    if n != 0:
        rest.append(("n", n))
    return tuple(rest)


def options(b, ep_rule, race, race_table, cs, white: bool):
    """All successor sums (as tuples of comps). race_table: dict[(Pos, mover_white)] -> white_wins or None."""
    out = []
    for i, c in enumerate(cs):
        prefix, suffix = cs[:i], cs[i + 1 :]
        kind = c[0]
        if kind == "n":
            n = c[1]
            if white and n > 0:
                out.append(prefix + (("n", n - 1),) + suffix)
            elif (not white) and n < 0:
                out.append(prefix + (("n", n + 1),) + suffix)
        elif kind == "t":
            _, L, R = c[1]
            for t in L if white else R:
                out.append(prefix + (("t", t),) + suffix)
        elif kind == "p":
            pos = c[1]
            for q in moves(b, pos, white, ep_rule):
                # classify with optional race table override
                pw, pb = has_passed(b, q, True, ep_rule), has_passed(b, q, False, ep_rule)
                if not pw and not pb:
                    comps = tuple(("p", x) for x in components(b, q))
                    out.append(prefix + comps + suffix)
                elif pw and not pb:
                    out.append(prefix + (("n", BIG),) + suffix)
                elif pb and not pw:
                    out.append(prefix + (("n", -BIG),) + suffix)
                else:
                    key = (q, white)
                    if race_table is not None and key in race_table:
                        ww = race_table[key]
                    elif race_table is not None:
                        # unassigned
                        out.append(None)  # type: ignore
                        continue
                    else:
                        ww = race_winner(b, q, white, ep_rule, race)
                    out.append(prefix + (("n", BIG if ww else -BIG),) + suffix)
    return out


def wins(b, ep_rule, race, race_table, fuel, cs, white: bool, memo):
    key = (fuel, norm_comps(cs), white)
    if key in memo:
        return memo[key]
    if fuel == 0:
        return None
    cs_n = norm_comps(cs)
    opts = options(b, ep_rule, race, race_table, cs_n, white)
    # no moves => loss
    if not opts:
        memo[key] = False
        return False
    unknown = False
    for o in opts:
        if o is None:
            unknown = True
            continue
        child = wins(b, ep_rule, race, race_table, fuel - 1, o, not white, memo)
        if child is None:
            unknown = True
        elif child is False:
            # opponent loses => we win
            memo[key] = True
            return True
    if unknown:
        memo[key] = None
        return None
    memo[key] = False
    return False


def is_value(b, pos, v, ep_rule, race, fuel=400, race_table=None):
    if has_passed(b, pos, True, ep_rule) or has_passed(b, pos, False, ep_rule):
        return False
    neg = t_neg(v)
    cs = tuple(("p", x) for x in components(b, pos)) + (("t", neg),)
    memo = {}
    a = wins(b, ep_rule, race, race_table, fuel, cs, True, memo)
    bres = wins(b, ep_rule, race, race_table, fuel, cs, False, memo)
    return a is False and bres is False


def not_value(b, pos, v, ep_rule, race, fuel=400):
    neg = t_neg(v)
    cs = tuple(("p", x) for x in components(b, pos)) + (("t", neg),)
    memo = {}
    a = wins(b, ep_rule, race, race_table=None, fuel=fuel, cs=cs, white=True, memo=memo)
    bres = wins(b, ep_rule, race, race_table=None, fuel=fuel, cs=cs, white=False, memo=memo)
    return a is True or bres is True


def S_win(b, pos, white, ep_rule, race, fuel=400):
    cs = tuple(("p", x) for x in components(b, pos))
    return wins(b, ep_rule, race, None, fuel, cs, white, {})


def W_win(b, pos, white, ep_rule, race, fuel=400, memo=None):
    if memo is None:
        memo = {}
    key = (fuel, pos, white)
    if key in memo:
        return memo[key]
    if fuel == 0:
        return None
    ms = moves(b, pos, white, ep_rule)
    if not ms:
        memo[key] = False
        return False
    unknown = False
    for q in ms:
        cl = classify(b, q, white, ep_rule, race)
        if cl[0] == "open":
            child = W_win(b, q, not white, ep_rule, race, fuel - 1, memo)
            if child is None:
                unknown = True
            elif child is False:
                memo[key] = True
                return True
        else:
            ww = cl[1]
            # mover wins if decided for mover
            if (ww and white) or ((not ww) and (not white)):
                memo[key] = True
                return True
            # else this option loses
    if unknown:
        memo[key] = None
        return None
    memo[key] = False
    return False


def parse(squares_w, squares_b):
    def sq(s):
        return (ord(s[0]) - ord("a"), int(s[1:]))

    return Pos(frozenset(sq(x) for x in squares_w), frozenset(sq(x) for x in squares_b), None)


def race_keys(b, pos, ep_rule, race="count", limit=100000):
    """BFS over open component positions; collect (race_pos, mover_white)."""
    keys = []
    seen_keys = set()
    todo = list(components(b, pos))
    seen_pos = set()
    steps = 0
    while todo and steps < limit:
        steps += 1
        p = todo.pop(0)
        if p in seen_pos:
            continue
        seen_pos.add(p)
        for white in (True, False):
            for q in moves(b, p, white, ep_rule):
                pw, pb = has_passed(b, q, True, ep_rule), has_passed(b, q, False, ep_rule)
                if pw and pb:
                    k = (q, white)
                    if k not in seen_keys:
                        seen_keys.add(k)
                        keys.append(k)
                elif not pw and not pb:
                    for c in components(b, q):
                        if c not in seen_pos:
                            todo.append(c)
    return keys


def main():
    flat = Board(8, 8, wrap=False)
    cyl = Board(8, 8, wrap=True)
    star2 = t_star(2)
    eighth = t_dy(3)

    posA = parse(["a4", "b3", "d2", "d3"], ["a7", "b7", "c5"])
    posB = parse(["b4", "c2", "d2"], ["a6", "a7", "c6", "d5"])
    posG = parse(["a2", "b2", "b3"], ["a5", "a6", "b6"])
    posX = parse(["b2", "d4", "g3", "h5"], ["a7", "c7", "f7", "g4"])

    print("=== L4 star-2 ===")
    print("components A", len(components(flat, posA)), "B", len(components(flat, posB)))
    for name, pos in [("A", posA), ("B", posB)]:
        ok = is_value(flat, pos, star2, EP_AWARE, RACE_COUNT)
        print(f"  {name} default IsValue(*2): {ok}")
    for r in (RACE_COUNT, RACE_MOVER, RACE_OPP):
        na = not_value(flat, posA, star2, EP_OFF, r)
        nb = not_value(flat, posB, star2, EP_OFF, r)
        print(f"  ep-off {r}: NotValue A={na} B={nb}")
    for ep in (EP_AWARE, EP_TEXTBOOK, EP_OFF):
        na = not_value(flat, posA, star2, ep, RACE_OPP)
        nb = not_value(flat, posB, star2, ep, RACE_OPP)
        print(f"  opponent {ep}: NotValue A={na} B={nb}")
    for ep, r in [(EP_AWARE, RACE_MOVER), (EP_TEXTBOOK, RACE_COUNT), (EP_TEXTBOOK, RACE_MOVER)]:
        print(
            f"  table extra {ep}/{r}: A={is_value(flat, posA, star2, ep, r)} "
            f"B={is_value(flat, posB, star2, ep, r)}"
        )

    print("=== L5 eighth ===")
    for ep in (EP_AWARE, EP_TEXTBOOK, EP_OFF):
        for r in (RACE_COUNT, RACE_MOVER, RACE_OPP):
            ok = is_value(flat, posG, eighth, ep, r)
            print(f"  {ep}/{r}: IsValue(1/8)={ok}")
    for ep in (EP_AWARE, EP_TEXTBOOK, EP_OFF):
        keys = race_keys(flat, posG, ep)
        print(f"  raceKeys {ep}: {len(keys)}")
        # check all-white and all-black assignments (extremes) + a few random
        # full 2^k may be slow; do all if k<=10
        k = len(keys)
        if k <= 10:
            ok_all = True
            for mask in range(1 << k):
                table = {}
                for i, key in enumerate(keys):
                    table[key] = bool((mask >> i) & 1)
                if not is_value(flat, posG, eighth, ep, RACE_COUNT, race_table=table):
                    ok_all = False
                    print(f"    FAIL mask={mask}")
                    break
            print(f"  all 2^{k} assignments {ep}: {ok_all}")
        else:
            print(f"  skip full sweep k={k}")

    print("=== L6 sumcounter ===")
    print("components X", len(components(cyl, posX)))
    print("passed W/B", has_passed(cyl, posX, True, EP_OFF), has_passed(cyl, posX, False, EP_OFF))
    sw = S_win(cyl, posX, True, EP_OFF, RACE_COUNT)
    sb = S_win(cyl, posX, False, EP_OFF, RACE_COUNT)
    print(f"  S white_wins={sw} black_wins={sb}  (want False, True)")
    ww = W_win(cyl, posX, True, EP_OFF, RACE_COUNT)
    wb = W_win(cyl, posX, False, EP_OFF, RACE_COUNT)
    print(f"  W white_wins={ww} black_wins={wb}  (want True, True)")


if __name__ == "__main__":
    main()
