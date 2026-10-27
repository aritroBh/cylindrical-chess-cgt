#!/usr/bin/env python3
"""Referee's own enumeration of four-state-legal king groups (K1, K2) on flat WxH, F_Z = first FZ files, <= NW white and
<= NB black pawns on ranks 2..H-1 of F_Z.  No move-count cut-off.  Writes candidates as JSON lines."""
import sys, itertools, json
W, H, FZ, NW, NB = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sqs = [(f, r) for f in range(1, FZ + 1) for r in range(1, H + 1)]
pawnsq = [(f, r) for f in range(1, FZ + 1) for r in range(2, H)]
def adj(a, b): return a != b and max(abs(a[0]-b[0]), abs(a[1]-b[1])) == 1
def dist(a, b): return max(abs(a[0]-b[0]), abs(a[1]-b[1]))
def att(color, p):
    d = 1 if color == 0 else -1
    return {(p[0]+df, p[1]+d) for df in (-1, 1)}
def combos(n):
    for k in range(n+1): yield from itertools.combinations(pawnsq, k)
out = 0
for wp in combos(NW):
    wa = set().union(*[att(0, p) for p in wp]) if wp else set()
    for bp in combos(NB):
        if set(wp) & set(bp): continue
        ba = set().union(*[att(1, p) for p in bp]) if bp else set()
        occ = set(wp) | set(bp)
        wsafe = [s for s in sqs if s not in occ and s not in ba]   # white king squares: not attacked by black pawns
        bsafe = [s for s in sqs if s not in occ and s not in wa]
        wpairs = [(a, b) for a in wsafe for b in wsafe if a < b and adj(a, b)]
        bpairs = [(a, b) for a in bsafe for b in bsafe if a < b and adj(a, b)]
        for zp in wpairs:
            for wpair in bpairs:
                if all(dist(a, b) >= 2 for a in zp for b in wpair):
                    print(json.dumps({'W': zp and [list(zp[0]), list(zp[1])], 'B': [list(wpair[0]), list(wpair[1])],
                                      'wp': [list(p) for p in wp], 'bp': [list(p) for p in bp]}))
                    out += 1
print('candidates', out, file=sys.stderr)
