#!/usr/bin/env python3
"""K26 audit: a SECOND, independent enumerator of two-shuttle placements on F_Z = files a-c (written for the K26 audit, from the
definition only, with no code of k26lib.py: plain tuples of (file, rank), no bitmasks).

A placement: <= nw White and <= nb Black pawns on F_Z ranks 2..H-1 (disjoint squares), a White king pair (two adjacent squares)
and a Black king pair, such that in each of the four combined king states
  (K1) no king stands on a pawn square or on a square attacked by an enemy pawn of the placement (the kings' squares only),
  (K2) the two kings are not adjacent (Chebyshev distance >= 2).
An unordered pair of squares is one shuttle; a placement is (frozenset White pawns, frozenset Black pawns, frozenset White pair,
frozenset Black pair).
  enum2.py H nw nb      -> prints the number of placements
"""
import itertools, sys

FILES = 'abcdefgh'


def name(s):
    return FILES[s[0] - 1] + str(s[1])


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def textbook_passed(own, enemy, white):
    """own: pawns of one colour; any passed (no enemy pawn on the same or an adjacent file strictly ahead)?  (no e.p. flag at a root)"""
    out = []
    for (f, r) in own:
        ahead = [(g, q) for (g, q) in enemy if abs(g - f) <= 1 and ((q > r) if white else (q < r))]
        out.append(not ahead)
    return out


def pawn_configs(H, nw, nb, NF=3):
    psq = [(f, r) for f in range(1, NF + 1) for r in range(2, H)]
    for kw in range(nw + 1):
        for wp in itertools.combinations(psq, kw):
            for kb in range(nb + 1):
                for bp in itertools.combinations(psq, kb):
                    if set(wp) & set(bp):
                        continue
                    yield wp, bp


def placements_of_config(H, wp, bp, NF=3):
    sqs = [(f, r) for f in range(1, NF + 1) for r in range(1, H + 1)]
    adj = [(a, b) for a, b in itertools.combinations(sqs, 2) if cheb(a, b) == 1]
    occ = set(wp) | set(bp)
    att_by_white = {(f + d, r + 1) for (f, r) in wp for d in (-1, 1)}
    att_by_black = {(f + d, r - 1) for (f, r) in bp for d in (-1, 1)}
    wok = {s for s in sqs if s not in occ and s not in att_by_black}
    bok = {s for s in sqs if s not in occ and s not in att_by_white}
    WP = [p for p in adj if p[0] in wok and p[1] in wok]
    BP = [p for p in adj if p[0] in bok and p[1] in bok]
    for z in WP:
        for w in BP:
            if all(cheb(a, b) >= 2 for a in z for b in w):
                yield z, w


def placements(H, nw, nb, NF=3):
    for wp, bp in pawn_configs(H, nw, nb, NF):
        for z, w in placements_of_config(H, wp, bp, NF):
            yield wp, bp, z, w


def pawn_string(wp, bp):
    return ' '.join(['P' + name(s) for s in wp] + ['p' + name(s) for s in bp])


if __name__ == '__main__':
    H, nw, nb = map(int, sys.argv[1:4])
    n = sum(1 for _ in placements(H, nw, nb))
    print('H', H, 'limits', nw, nb, 'placements', n)
