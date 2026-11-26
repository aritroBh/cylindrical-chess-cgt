"""Variable black king, fixed white king. Entry position is after c5+."""

from zones import ALL, bit, N, P, squares, dilation, diag
from board import X, name


def geom(d):
    t, k, w, b, c, e = d
    valid = ALL & ~(N[k] | bit(k) | bit(w) | bit(b) | bit(c))
    return valid, P[0][w], bool(bit(k) & (P[1][b] | P[1][c]))


def edges(d):
    t, k, w, b, c, e = d
    valid, check, wcheck = geom(d)
    if t:
        for z in squares(N[k] & ~(bit(w) | P[1][b] | P[1][c])):
            legal = valid & ~(bit(z) | N[z])
            if legal:
                yield (
                    "K" + name(z),
                    diag(0, z, w, X if b == z else b, X if c == z else c),
                    legal,
                    False,
                )
    else:
        yield "K", diag(1, k, w, b, c), valid & ~check, True
        if w != X and not bit(w) & (N[k] | bit(k)):
            yield "Kx" + name(w), diag(1, k, X, b, c), bit(w), True
    ours, opp = ((w,), (b, c)) if t else ((b, c), (w,))
    dy = 1 if t else -1
    for p in ours:
        if p == X:
            continue
        for dx, n in ((0, 1), (0, 2), (-1, 1), (1, 1)):
            z = p + dy * 8 * n + dx
            if not 0 <= z < 64 or abs(z % 8 - p % 8) > 1:
                continue
            valid_here = valid & ~bit(z)
            cap = X
            if dx:
                cap = z - dy * 8 if z == e else z
                if cap not in opp or z == k:
                    continue
            else:
                if z in (w, b, c, k):
                    continue
                if n == 2:
                    if p // 8 != (1 if t else 6) or p + dy * 8 in (w, b, c, k):
                        continue
                    valid_here &= ~bit(p + dy * 8)
            nw = z if t else X if w == cap else w
            nb = (X if b == cap else b) if t else (z if b == p else b)
            nc = (X if c == cap else c) if t else (z if c == p else c)
            if t and bit(k) & (P[1][nb] | P[1][nc]):
                continue
            if not t:
                valid_here &= ~P[0][nw]
            if not valid_here:
                continue
            ep = X
            if n == 2 and any(bit(p + dy * 8) & P[t][v] for v in opp):
                ep = p + dy * 8
            yield (
                (name(p)[0] + "x" if dx else "") + name(z),
                (None if z // 8 in (0, 7) else diag(1 - t, k, nw, nb, nc, ep)),
                valid_here,
                False,
            )


def fortress(d):
    """The three blockade shapes in the hand proof, with Black to move."""
    t, k, w, b, c, e = d
    if t or c != X or b == X or b % 8 != 2 or w not in (X, 41, 49):
        return 0
    r = b // 8 + 1
    valid = geom(d)[0]
    if r == 2:
        return valid & (bit(17) | bit(19)) if k == 2 else 0
    if not 3 <= r <= 6:
        return 0
    if k == b - 8:
        return valid
    if k == b - 16:
        return valid & (bit(b + 7) | bit(b + 8) | bit(b + 9))
    if k == b - 17:
        return valid & bit(b - 1)
    if k == b - 15:
        return valid & bit(b + 1)
    return 0
