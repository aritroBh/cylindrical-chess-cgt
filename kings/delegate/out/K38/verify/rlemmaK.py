# rlemmaK.py -- exhaustive check of K38's Lemma K' on cyl:7x6 and flat:7x6 with the referee's generator rgen.py.
import sys
sys.dont_write_bytecode = True
from rgen import Board
for name, wrap in (('cyl:7x6', True), ('flat:7x6', False)):
    B = Board(7, 6, wrap)
    sqs = [(f, r) for f in range(7) for r in range(6)]
    corners = set() if wrap else {(0, 0), (6, 0), (0, 5), (6, 5)}
    n = fails = 0; hyp_needed = 0
    for me in (0, 1):
        for s in sqs:
            for t in sqs:
                if t == s or B.adj(s, t): continue
                for q in [None] + [x for x in sqs if x[1] not in (0, 5)]:
                    if q in (s, t): continue
                    orth = q is not None and s in corners and abs(q[0]-s[0]) + abs(q[1]-s[1]) == 1
                    wk, bk = (s, t) if me == 0 else (t, s)
                    own = frozenset([q]) if q else frozenset()
                    pos = (wk, bk, own if me == 0 else frozenset(), frozenset() if me == 0 else own, me, None)
                    if not B.legal_pos(pos): continue
                    km = [c for k, c, lab in B.moves(pos) if lab.startswith('K')]
                    if orth:
                        if not km: hyp_needed += 1
                        continue
                    n += 1
                    if not km: fails += 1
    print(name, "Lemma K' instances", n, "failures", fails, "| excluded (flat corner, orthogonal pawn) instances with no king move:", hyp_needed)
