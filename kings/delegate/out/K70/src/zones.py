"""Board geometry for a variable white king. An edge lists its possible squares."""

from board import *
from functools import lru_cache

ALL = (1 << 64) - 1


def bit(x):
    return (1 << x) if x < X else 0


def mask(it):
    return sum(bit(x) for x in it)


def squares(m):
    while m:
        n = (m & -m).bit_length() - 1
        yield n
        m &= m - 1


N = [mask(i for i in range(64) if dist(i, j) == 1) for j in range(64)]
P = [
    [mask(i for i in range(64) if attacked(j, i, t)) for j in range(65)] for t in (0, 1)
]


def dilation(m):
    east = (m & 0x7F7F7F7F7F7F7F7F) << 1
    west = (m & 0xFEFEFEFEFEFEFEFE) >> 1
    return (east | west | ((m | east | west) << 8) | ((m | east | west) >> 8)) & ALL


def diag(t, j, w, b, c, e=X):
    return t, j, w, min(b, c), max(b, c), e


def geom(d):
    t, j, w, b, c, e = d
    # Landing legality of a white king (ignoring occupancy by black pawns).
    zone = ALL & ~(N[j] | bit(j) | bit(b) | bit(c) | bit(w))
    return zone, (P[1][b] | P[1][c]), bool(P[0][w] & bit(j))


def edges(d):
    t, j, w, b, c, e = d
    zone, check, bcheck = geom(d)
    dest = zone & ~check
    if t:
        for z in squares(N[j] & ~(bit(b) | bit(c) | P[0][w])):
            a = zone & ~(bit(z) | N[z])
            if a:
                yield "K" + name(z), diag(0, z, X if w == z else w, b, c), a, False
    else:
        # Quiet white king moves and captures have different target diagrams.
        yield "K", diag(1, j, w, b, c), dest, True
        for z in (b, c):
            if z != X and not bit(z) & (N[j] | bit(j) | check):
                yield (
                    "Kx" + name(z),
                    diag(1, j, w, X if b == z else b, X if c == z else c),
                    bit(z),
                    True,
                )
    ours, opp = ((b, c), (w,)) if t else ((w,), (b, c))
    dy = -1 if t else 1
    for p in ours:
        if p == X:
            continue
        for dx, n in ((0, 1), (0, 2), (-1, 1), (1, 1)):
            z = p + dy * 8 * n + dx
            if not 0 <= z < 64 or abs(z % 8 - p % 8) > 1:
                continue
            a = zone & ~bit(z)
            cap = X
            if dx:
                cap = z - dy * 8 if z == e else z
                if cap not in opp or z == j:
                    continue
            else:
                if z in (w, b, c, j):
                    continue
                mid = p + dy * 8
                if n == 2:
                    if p // 8 != (6 if t else 1) or mid in (w, b, c, j):
                        continue
                    a &= ~bit(mid)
            nw = (X if w == cap else w) if t else z
            nb = (z if b == p else b) if t else (X if b == cap else b)
            nc = (z if c == p else c) if t else (X if c == cap else c)
            if t and bit(j) & P[0][nw]:
                continue
            if not t:
                a &= ~(P[1][nb] | P[1][nc])
            if not a:
                continue
            ep = X
            if n == 2 and any(bit(mid) & P[1 - t][v] for v in opp):
                ep = mid
            m = (name(p)[0] + "x" if dx else "") + name(z)
            yield (
                m,
                (None if z // 8 in (0, 7) else diag(1 - t, j, nw, nb, nc, ep)),
                a,
                False,
            )
