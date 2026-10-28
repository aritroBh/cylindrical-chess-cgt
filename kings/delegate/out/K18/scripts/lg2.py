#!/usr/bin/env python3
"""lg2.py -- second, independent implementation of the local promotion game (LOOPY Def. 2.6), K18.

Written separately from lg.cpp (different data structures: sets of (file, rank) tuples, attack tests by search
instead of bitboards; explicit reachable graph from the root + Jacobi iteration instead of dense tables).
s = White, sbar = Black.  Usage:  python lg2.py --board cyl:8x6 --fz 0:3 < positions   (prints the four n-values)
"""
import sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--board", default="cyl:8x6")
ap.add_argument("--fz", default="0:3")
args = ap.parse_args()
kind, dims = args.board.split(":")
CYL = kind == "cyl"
W, H = map(int, dims.split("x"))
fz0, fzn = map(int, args.fz.split(":"))
FZFILES = {(fz0 + i) % W for i in range(fzn)}
INF = 10 ** 9


def nbf(f, d):
    g = f + d
    if CYL:
        return g % W
    return g if 0 <= g < W else None


def king_nbrs(sq):
    f, r = sq
    out = set()
    for df in (-1, 0, 1):
        for dr in (-1, 0, 1):
            if df == 0 and dr == 0:
                continue
            g = nbf(f, df)
            if g is None or not (0 <= r + dr < H):
                continue
            if (g, r + dr) != sq:
                out.add((g, r + dr))
    return out


def pawn_attacks_square(color, pawns, sq):
    """does some pawn of `color` in `pawns` attack sq?"""
    f, r = sq
    pr = r - 1 if color == "w" else r + 1  # rank where an attacking pawn would stand
    for df in (-1, 1):
        g = nbf(f, df)
        if g is not None and (g, pr) in pawns:
            return True
    return False


def moves(state, color, confine):
    """legal moves of `color`; yields (newstate, kind, from, to) with kind 'm' or 'promo'."""
    Wp, Bp, wk, bk, stm, ep = state
    own, en = (Wp, Bp) if color == "w" else (Bp, Wp)
    ok, ek = (wk, bk) if color == "w" else (bk, wk)
    ecol = "b" if color == "w" else "w"
    occ = set(Wp) | set(Bp) | {wk, bk}
    res = []

    def mk(newown, newen, nok, kind, frm, to, nep):
        # own king must not be attacked by enemy pawns
        if pawn_attacks_square(ecol, newen, nok):
            return
        if color == "w":
            ns = (frozenset(newown), frozenset(newen), nok, bk, "b", nep)
        else:
            ns = (frozenset(newen), frozenset(newown), wk, nok, "w", nep)
        res.append((ns, kind, frm, to))

    # king
    for d in king_nbrs(ok):
        if d in own or d == ek or d in king_nbrs(ek):
            continue
        if confine and color == "b" and d[0] not in FZFILES:
            continue
        en2 = en - {d}
        if pawn_attacks_square(ecol, en2, d):
            continue
        mk(own, en2, d, "m", ok, d, None)
    # pawns
    dr = 1 if color == "w" else -1
    start = 1 if color == "w" else H - 2
    last = H - 1 if color == "w" else 0
    for (f, r) in own:
        t = (f, r + dr)
        if t not in occ:
            if r + dr == last:
                mk(own - {(f, r)}, en, ok, "promo", (f, r), t, None)
            else:
                mk((own - {(f, r)}) | {t}, en, ok, "m", (f, r), t, None)
                t2 = (f, r + 2 * dr)
                if r == start and t2 not in occ:
                    # e.p. right only matters if an enemy pawn stands beside the landing square
                    beside = any((nbf(f, d2) is not None) and ((nbf(f, d2), r + 2 * dr) in en) for d2 in (-1, 1))
                    mk((own - {(f, r)}) | {t2}, en, ok, "m", (f, r), t2, t if beside else None)
        for df in (-1, 1):
            g = nbf(f, df)
            if g is None:
                continue
            tc = (g, r + dr)
            if tc in en:
                if r + dr == last:
                    mk(own - {(f, r)}, en - {tc}, ok, "promo", (f, r), tc, None)
                else:
                    mk((own - {(f, r)}) | {tc}, en - {tc}, ok, "m", (f, r), tc, None)
            elif ep is not None and ep == tc and (g, r) in en:
                mk((own - {(f, r)}) | {tc}, en - {(g, r)}, ok, "m", (f, r), tc, None)
    return res


def solve(root, passing, qclause, full=False):
    """n(root) for White to move (s), or Black to move; returns int or INF."""
    # explicit reachable graph
    nodes = {}
    stack = [root]
    while stack:
        st = stack.pop()
        if st in nodes:
            continue
        Wp, Bp, wk, bk, stm, ep = st
        if stm == "b":
            ms = moves(st, "b", True)
            opts = []  # ('win',) or ('succ', state)
            for ns, kd, frm, to in ms:
                if kd == "promo":
                    if not qclause:
                        opts.append(("win",))
                    else:
                        # can White capture the new queen on `to` at once?
                        bp2 = Bp - {frm}
                        cap = (to in king_nbrs(wk)) and (to not in king_nbrs(bk)) and not pawn_attacks_square("b", bp2, to)
                        if not cap:
                            opts.append(("win",))
                else:
                    opts.append(("succ", ns))
                    stack.append(ns)
            nodes[st] = ("A", opts)
        else:
            ms = moves(st, "w", False)
            chk = pawn_attacks_square("b", Bp, wk)
            if not ms and chk:
                nodes[st] = ("B", "mated")
                continue
            opts = []
            promo = False
            for ns, kd, frm, to in ms:
                if kd == "promo":
                    promo = True
                else:
                    opts.append(ns)
                    stack.append(ns)
            if passing and not chk:
                ps = (Wp, Bp, wk, bk, "b", None)
                opts.append(ps)
                stack.append(ps)
            nodes[st] = ("B", ("promo" if promo else opts))
    val = {st: INF for st in nodes}
    for st, (ty, d) in nodes.items():
        if ty == "B" and d == "mated":
            val[st] = 0
    changed = True
    while changed:
        changed = False
        for st, (ty, d) in nodes.items():
            if ty == "A":
                best = INF
                for o in d:
                    if o[0] == "win":
                        best = min(best, 1)
                    else:
                        v = val[o[1]]
                        if v < INF:
                            best = min(best, v + 1)
                nv = best
            else:
                if d == "mated":
                    nv = 0
                elif d == "promo":
                    nv = INF
                elif not d:
                    nv = INF  # plain stalemate
                else:
                    nv = max(val[o] for o in d)
            if nv != val[st]:
                val[st] = nv
                changed = True
    if full:
        return val[root], nodes, val
    return val[root]


def parse(line):
    toks = line.split()
    Wp, Bp = set(), set()
    wk = bk = None
    for t in toks[:-2]:
        f, r = ord(t[1]) - 97, int(t[2:]) - 1
        c = t[0]
        if c == "K": wk = (f, r)
        elif c == "k": bk = (f, r)
        elif c == "P": Wp.add((f, r))
        elif c == "p": Bp.add((f, r))
    stm = toks[-2]
    ep = None if toks[-1] == "-" else (ord(toks[-1][0]) - 97, int(toks[-1][1:]) - 1)
    return (frozenset(Wp), frozenset(Bp), wk, bk, stm, ep)


if __name__ == "__main__":
    names = [("plain/P", False, False), ("plain/Q", False, True), ("pass/P", True, False), ("pass/Q", True, True)]
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line or line[0] == "#":
            continue
        st = parse(line)
        out = []
        for nm, ps, q in names:
            v = solve(st, ps, q)
            out.append(f"{nm}={'inf' if v >= INF else v}")
        print(f"{line} | " + " ".join(out), flush=True)
