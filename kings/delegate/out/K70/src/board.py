"""Coordinates and legal successors in the first-promotion game."""

X = 64


def sq(s):
    return X if s == "-" else ord(s[0]) - 97 + 8 * (int(s[1]) - 1)


def name(n):
    return "-" if n == X else chr(97 + n % 8) + str(1 + n // 8)


def dist(a, b):
    return max(abs(a // 8 - b // 8), abs(a % 8 - b % 8))


def attacked(p, k, t):
    return (
        p != X and k // 8 - p // 8 == (1 if t == 0 else -1) and abs(k % 8 - p % 8) == 1
    )


def pos(k, j, w, b, c, t=0, e=X):
    return (t, k, j, w, *sorted((b, c)), e)


def moves(s):
    t, k, j, w, b, c, e = s
    a, o = (j, k) if t else (k, j)
    ours = (b, c) if t else (w,)
    theirs = (w,) if t else (b, c)
    for z in range(64):
        if (
            dist(z, a) != 1
            or dist(z, o) <= 1
            or z in ours
            or any(attacked(p, z, 1 - t) for p in theirs)
        ):
            continue
        yield (
            "K" + name(z),
            pos(
                k if t else z,
                z if t else j,
                X if t and z == w else w,
                X if not t and z == b else b,
                X if not t and z == c else c,
                1 - t,
            ),
        )
    dy = -1 if t else 1
    for p in ours:
        if p == X:
            continue
        for dx, n in ((0, 1), (0, 2), (-1, 1), (1, 1)):
            z = p + 8 * dy * n + dx
            if not (0 <= z < 64 and abs(z % 8 - p % 8) <= 1):
                continue
            cap = z - 8 * dy if dx and z == e else z if dx else X
            if dx:
                if cap not in theirs or z in (k, j):
                    continue
            elif (
                z in (k, j, w, b, c)
                or n == 2
                and (p // 8 != (6 if t else 1) or p + 8 * dy in (k, j, w, b, c))
            ):
                continue
            if any(attacked(v, a, 1 - t) for v in theirs if v != cap):
                continue
            ep = X
            if n == 2 and any(attacked(v, p + dy * 8, 1 - t) for v in theirs):
                ep = p + dy * 8
            nw = (X if w == cap else w) if t else z
            nb = (z if b == p else b) if t else (X if b == cap else b)
            nc = (z if c == p else c) if t else (X if c == cap else c)
            label = (name(p)[0] + "x" if dx else "") + name(z)
            yield (
                label,
                (None if z // 8 in (0, 7) else pos(k, j, nw, nb, nc, 1 - t, ep)),
            )
