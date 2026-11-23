"""K42 referee: promotion-free contexts and their pawn-game class, written from the K18/K42 definitions.
Context: pawns on the context files, <= maxw White and <= maxb Black, ranks 2..H-1, no e.p. right.
Promotion-free: no sequence of pawn moves of the context alone (any colours, any order, captures and e.p.) promotes.
Pawn game: alternate moves, normal play (no move = loss), e.p. included.
Output: one line per promotion-free context whose White-to-move pawn game is lost: class Z (Black to move also loses)
or N (Black to move wins), and the mirror-class count (reflection a<->c about file b).
usage: python3 vctx.py W H files maxw maxb
"""
import sys, itertools
from functools import lru_cache

W, H = int(sys.argv[1]), int(sys.argv[2])
files = [ord(c) - 97 for c in sys.argv[3]]
maxw, maxb = int(sys.argv[4]), int(sys.argv[5])


def fwrap(f):
    return f % W  # cylinder


def moves(wp, bp, ep, side):
    """pawn moves of side (0 White, 1 Black); yields (wp, bp, ep, promoted)."""
    own, opp = (wp, bp) if side == 0 else (bp, wp)
    d = 1 if side == 0 else -1
    last = H - 1 if side == 0 else 0
    start = 1 if side == 0 else H - 2
    occ = wp | bp
    out = []
    for (f, r) in own:
        t = (f, r + d)
        if t not in occ:
            out.append(((f, r), t, None, None))
            if r == start:
                t2 = (f, r + 2 * d)
                if t2 not in occ:
                    out.append(((f, r), t2, None, t))
        for df in (-1, 1):
            u = (fwrap(f + df), r + d)
            if u in opp:
                out.append(((f, r), u, u, None))
            elif ep is not None and u == ep:
                out.append(((f, r), u, (u[0], r), None))
    for (s, t, cap, newep) in out:
        o2 = (own - {s}) | {t}
        p2 = opp - {cap} if cap else opp
        prom = t[1] == last
        if side == 0:
            yield (frozenset(o2), frozenset(p2), newep, prom)
        else:
            yield (frozenset(p2), frozenset(o2), newep, prom)


def promotion_free(wp, bp):
    seen = set()
    stack = [(wp, bp, None, 0), (wp, bp, None, 1)]
    # any order: the e.p. right only for the very next move of the other side; explore both "who moves next"
    while stack:
        st = stack.pop()
        if st in seen:
            continue
        seen.add(st)
        w, b, ep, side = st
        for nside in (0, 1):
            e = ep if nside == side else None
            for (w2, b2, ep2, prom) in moves(w, b, e, nside):
                if prom:
                    return False
                stack.append((w2, b2, ep2, 1 - nside))
                stack.append((w2, b2, None, nside))
    return True


@lru_cache(maxsize=None)
def lost(wp, bp, ep, side):
    """side to move loses the pawn game (normal play); assumes promotion-free."""
    for (w2, b2, ep2, prom) in moves(wp, bp, ep, side):
        assert not prom
        if lost(w2, b2, ep2, 1 - side):
            return False
    return True


sqs = [(f, r) for f in files for r in range(1, H - 1)]
res = []
for nw in range(maxw + 1):
    for nb in range(maxb + 1):
        for ws in itertools.combinations(sqs, nw):
            rest = [s for s in sqs if s not in ws]
            for bs in itertools.combinations(rest, nb):
                wp, bp = frozenset(ws), frozenset(bs)
                if not promotion_free(wp, bp):
                    continue
                if lost(wp, bp, None, 0):
                    cls = 'Z' if lost(wp, bp, None, 1) else 'N'
                    res.append((wp, bp, cls))


def mirror(s):
    return frozenset((fwrap(2 - f), r) for (f, r) in s)


def name(wp, bp):
    return ' '.join(['P%s%d' % (chr(97 + f), r + 1) for (f, r) in sorted(wp)] +
                    ['p%s%d' % (chr(97 + f), r + 1) for (f, r) in sorted(bp)])


classes = set()
for wp, bp, cls in res:
    key = min(name(wp, bp), name(mirror(wp), mirror(bp)))
    classes.add(key)
    print(cls, name(wp, bp))
nz = sum(1 for r in res if r[2] == 'Z')
print('# total %d zero %d negative %d mirror classes %d' % (len(res), nz, len(res) - nz, len(classes)))
