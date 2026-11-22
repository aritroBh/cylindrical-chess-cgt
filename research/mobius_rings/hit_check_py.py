#!/usr/bin/env python3
"""Third, independent check of every *2 / *3 hit: the existing Part B engine (research/mobius/mob_pawns.py,
whole-board game value as a canonical CGT form) must give value *2 (resp. *3) exactly.
usage (repo root): PYTHONPATH=. .venv/bin/python research/mobius_rings/hit_check_py.py HITFILE [LIMIT]
HITFILE lines: 'HIT <sig> <ring tokens>'."""
import sys, re, time
from cylcgt import cgt
from research.mobius import mob_pawns as mp
lines = [l.split(None, 2) for l in open(sys.argv[1]) if l.startswith("HIT")]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else len(lines)
bad = 0
for _, sig, ring in lines[:limit]:
    toks = ring.split()
    w, b = set(), set()
    for f, t in enumerate(toks):
        for m in re.finditer(r'([WB])(\d+)', t):
            for r in m.group(2):
                (w if m.group(1) == 'W' else b).add((f, int(r)))
    board = mp.Board(len(toks), "mob")
    pos = mp.Pos(frozenset((f, r, 1) for f, r in w), frozenset((f, r, -1) for f, r in b))
    t0 = time.time()
    g = mp.value(board, pos)
    want = cgt.nimber(int(sig_k)) if (sig_k := {'NNPN': 2, 'NNNP': 3}[sig]) else None
    ok = cgt.le(g, want) and cgt.le(want, g)
    bad += not ok
    print("%s %s n=%d value=%s %s (%.1fs)" % ("OK " if ok else "BAD", sig, len(toks), cgt.show(g), ring, time.time() - t0), flush=True)
print("python engine: %d hits checked, %d not equal to the claimed nimber" % (min(limit, len(lines)), bad))
