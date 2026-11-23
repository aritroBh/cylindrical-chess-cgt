"""flagan.py RING : the e.p. flags in the reduced graph of RING: count per (file, landing rank, holder), and the files
of the pawns that can capture e.p. (so the files that a flag touches)."""
import sys, os, collections
sys.setrecursionlimit(1000000)
import fverify_lib as V
B, root, nodes = V.reduced(sys.argv[1])
cnt = collections.Counter(); touch = set()
for p in nodes:
    if p[1]:
        f, rl, rs, h = p[1]; cnt[(f, rl, h)] += 1; touch.add(f)
        for g in (f - 1, f + 1): touch.add(g % B.n)
print('n', B.n, 'nodes', len(nodes), 'flagged', sum(cnt.values()))
for k, v in sorted(cnt.items()): print('  flag file %d landing rank %d holder %s : %d nodes' % (k[0], k[1], 'WB'[k[2]], v))
print('  files touched by flags (victim file +-1):', sorted(touch))
