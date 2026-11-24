#!/usr/bin/env python3
"""T12 analysis: classify the K+P vs K+P mutual zugzwangs found by the census.

For every cylinder C_n x R (n = 3..9, R = 5..8) the census lists the positions in
which *both* sides to move lose.  This script groups them by the relative
geometry of the four pieces (up to rotation of the cylinder and reflection), so
that the families can be listed.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def sq(s):
    return (ord(s[0]) - ord("a"), int(s[1:]))


def load(path):
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            t = line.split()
            out.append((sq(t[0][1:]), sq(t[1][1:]), sq(t[2][1:]), sq(t[3][1:])))
    return out


def canon(pos, W):
    """Canonical form of (wp, bp, wk, bk) under rotation of the cylinder and
    reflection of the files, keeping colours fixed."""
    wp, bp, wk, bk = pos
    best = None
    for rot in range(W):
        for refl in (1, -1):
            def f(s):
                x = s[0] if refl == 1 else (W - 1 - s[0])
                return ((x + rot) % W, s[1])
            cand = (f(wp), f(bp), f(wk), f(bk))
            if best is None or cand < best:
                best = cand
    return best


def main():
    print(f"{'board':>8} {'n_zug':>6} {'exact':>6}  families (canonical: wp bp wk bk)")
    for n in range(3, 10):
        for R in range(5, 9):
            p0 = os.path.join(DATA, f"census_kpkp_{n}x{R}_b0.txt")
            p1 = os.path.join(DATA, f"census_kpkp_{n}x{R}_b1.txt")
            if not os.path.exists(p0):
                continue
            a = load(p0)
            b = set(load(p1))
            exact = [x for x in a if x in b]
            fams = collections.Counter(canon(x, n) for x in exact)
            fams_all = collections.Counter(canon(x, n) for x in a)
            famstr = ", ".join(f"{k} x{v}" for k, v in sorted(fams.items()))
            print(f"{n}x{R:<5} {len(a):>6} {len(exact):>6}  {famstr}")
            if len(fams_all) != len(fams):
                extra = {k: v for k, v in fams_all.items() if k not in fams}
                print(f"        (bound-only families: {extra})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
