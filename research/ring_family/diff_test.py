"""Differential test: ringeval (C) vs cylcgt (Python) on random rings; default setting.
Compares outcome class and, for nimbers, the nimber."""
import sys, random, time
sys.path.insert(0, "research/ring_family")
from ringlib import *
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos
pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
seed = int(sys.argv[1]); N = int(sys.argv[2]); n = int(sys.argv[3]); npawns = int(sys.argv[4])
random.seed(seed)
def rand_ring():
    while True:
        W = set(); B = set()
        files = list(range(n))
        # every file occupied
        for f in files:
            if random.random() < 0.5: W.add((f, random.randint(2, 6)))
            else: B.add((f, random.randint(3, 7)))
        while len(W) + len(B) < npawns:
            f = random.randrange(n)
            if random.random() < 0.5:
                s = (f, random.randint(2, 6))
            else: s = None
            t = (f, random.randint(3, 7))
            if s and s not in B: W.add(s)
            elif t not in W: B.add(t)
        if len(W) + len(B) != npawns or (W & B): continue
        ring = [([], []) for _ in range(n)]
        for f, r in W: ring[f][0].append(r)
        for f, r in B: ring[f][1].append(r)
        ring = tuple((tuple(sorted(a)), tuple(sorted(b))) for a, b in ring)
        return ring
cand = [rand_ring() for _ in range(15 * N)]
cres = evaluate(cand)
sel = [(r, x) for r, x in zip(cand, cres) if not (x[0].endswith("passed-at-root") or "RACE" in x[0])][:N]
rings = [r for r, x in sel]; res = [x for r, x in sel]
bad = 0; t0 = time.time(); counts = {}
for ring, r in zip(rings, res):
    if r[0].endswith("passed-at-root") or "RACE" in r[0]:
        continue
    pawns._value.cache_clear()
    g = pawns.value(Board(n, 8, True, True), Pos.parse(to_text(ring)))
    o = cgt.outcome(g)
    nim = g.nim if g.nim is not None else -1
    mine = (r[0], r[1])
    ok = (o == r[0]) and (nim == r[1] or (nim == -1 and r[1] == -1))
    counts[o] = counts.get(o, 0) + 1
    if not ok:
        bad += 1; print("MISMATCH", to_text(ring), "cylcgt:", o, nim, cgt.show(g), "C:", r)
print(f"C{n} {npawns} pawns: {N} random rings, compared {sum(counts.values())}, mismatches {bad}, outcomes {counts}, {time.time()-t0:.0f}s")
