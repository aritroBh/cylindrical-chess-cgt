#!/usr/bin/env python3
"""Each hit must be a root ring: pawn on every file, ranks 2..7, no shared square, no passed pawn (independent
cover-coordinate test, as in ringcount.py).  usage: hit_ring_legality.py HITFILE"""
import re, sys
bad = n = 0
for l in open(sys.argv[1]):
    if not l.startswith("HIT"): continue
    ring = l.split(None, 2)[2].split(); N = len(ring); pawns = []
    for f, t in enumerate(ring):
        for m in re.finditer(r'([WB])(\d+)', t):
            for r in m.group(2): pawns.append((f, int(r), 0 if m.group(1) == 'W' else 1))
    cov = []
    for (f, r, c) in pawns:
        cov.append((f, r, c)); cov.append((f + N, 9 - r, c))
    files = {f for f, _, _ in pawns}
    ok = len(files) == N and all(2 <= r <= 7 for _, r, _ in pawns) and len({(f, r) for f, r, _ in pawns}) == len(pawns)
    for (f, r, c) in pawns:
        d = 1 if c == 0 else -1
        # enemy lifts on cover files f-1, f, f+1 (mod 2N), strictly ahead; twin lifts reverse the notion of ahead via the rank flip
        blocked = any(c2 != c and (g - f) % (2 * N) in (0, 1, 2 * N - 1) and (s - r) * d > 0 for (g, s, c2) in cov)
        ok = ok and blocked
    n += 1; bad += not ok
    if not ok: print("NOT A ROOT RING", l.strip())
print("hits %d, not legal root rings: %d" % (n, bad))
