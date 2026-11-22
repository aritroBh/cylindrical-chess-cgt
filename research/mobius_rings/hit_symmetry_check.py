#!/usr/bin/env python3
"""Every hit (*2 / *3 ring) must keep its signature under all 2n rotations rho^t (seam shifts, with rank and
direction flips: the images carry reversed pawns), the mirror and the colour swap, in both C1 and C2.
usage (in research/mobius_rings): hit_symmetry_check.py HITFILE"""
import re, subprocess, sys
SW = {'N': 'N', 'L': 'R', 'R': 'L', 'P': 'P'}
def parse(ring):
    P = set()
    for f, t in enumerate(ring.split()):
        for m in re.finditer(r'([WB])(\d+)', t):
            c = 0 if m.group(1) == 'W' else 1
            for r in m.group(2): P.add((f, int(r), c, c))          # default: white up (di 0), black down (di 1)
    return P
def fmt(P, n):
    toks = []
    for f in range(n):
        s = ''
        for c, di, ch in ((0, 0, 'W'), (0, 1, 'w'), (1, 1, 'B'), (1, 0, 'b')):
            rs = ''.join(str(r) for r in range(1, 9) if (f, r, c, di) in P)
            if rs: s += ch + rs
        toks.append(s or '-')
    return ' '.join(toks)
def rho(P, n): return {((0, 9 - r, c, 1 - di) if f == n - 1 else (f + 1, r, c, di)) for (f, r, c, di) in P}
def run(b, lines):
    return subprocess.run(["./" + b, "solve", "--kind", "2"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.split()
hits = [l.split(None, 2) for l in open(sys.argv[1]) if l.startswith("HIT")]
bad = tot = 0
for _, sig, ring in hits:
    ring = ring.strip(); n = len(ring.split()); P = parse(ring); imgs = []; Q = P
    for t in range(2 * n):
        imgs.append(("rho^%d" % t, Q, sig)); Q = rho(Q, n)
    imgs.append(("mirror", {(n - 1 - f, r, c, di) for (f, r, c, di) in P}, sig))
    imgs.append(("colour swap", {(f, r, 1 - c, di) for (f, r, c, di) in P}, "".join(SW[x] for x in sig)))
    for b in ("mob1", "mob2"):
        out = run(b, [fmt(Q_, n) for _, Q_, _ in imgs])
        for (name, _, want), got in zip(imgs, out):
            tot += 1
            if got != want: bad += 1; print("BAD", b, name, ring, got, want)
print("hits %d, images checked %d, mismatches %d" % (len(hits), tot, bad))
