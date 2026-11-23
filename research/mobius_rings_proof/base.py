"""base.py -- base cases: signature of FAM(m) + *h (h = 0..3) for m = 0..6 by
  (1) rgraph.py (own code, reduced game, Lemma 1), (2) difftest.unreduced (own code, full game, m <= 2 only),
  (3) bin/mob1_32, (4) bin/mob2_32, (5) bin/check (n <= 21) from research/mobius_rings_n (one ring per process)."""
import sys, os, subprocess
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
from rgraph import FAM, reduced, solve
from difftest import unreduced
BIN = os.path.join(D, '../mobius_rings_n/bin')
def ext(args, ring):
    return subprocess.run(['nice', '-n', '15'] + args, input=ring + '\n', capture_output=True, text=True,
                          timeout=600).stdout.split()[0]
for fam in ('F1', 'F2', 'F3'):
    for m in range(0, 7):
        ring = FAM[fam](m); B, root, nodes = reduced(ring); n = len(root[0])
        own = solve(nodes, root, 3)
        unr = unreduced(B, root) if m <= 2 else '-'
        m1 = ext([BIN + '/mob1_32', 'solve'], ring); m2 = ext([BIN + '/mob2_32', 'solve'], ring)
        ck = ext([BIN + '/check', 'mobius', str(n), 'solve'], ring) if n <= 21 else '-'
        print('%s m=%d n=%d  rgraph=%s unreduced=%s mob1=%s mob2=%s check=%s' % (fam, m, n, own, unr, m1, m2, ck), flush=True)
