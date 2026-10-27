#!/usr/bin/env python3
"""Longer-wall follow-up: for each HIT (res files) with first-non-N index >= MINFN (default 2), keep the core (first W tokens of the ring)
and close it with alternating W2/B4 walls of length 4..MAXL (n=W+L <= 20), both phases; evaluate with rgq (full H=7 signature, solvef).
usage: walls.py MINFN MAXL > walls_results.tsv     (one rgq process at a time)"""
import sys, glob, subprocess, os
minfn = int(sys.argv[1]) if len(sys.argv) > 1 else 2
maxl = int(sys.argv[2]) if len(sys.argv) > 2 else 14
def fnidx(sig):
    return next((i for i, c in enumerate(sig) if c != 'N'), None)
cores = {}
for f in sorted(glob.glob('out/*.res')):
    job = None
    for line in open(f):
        if line.startswith('#JOB'): job = line.rstrip('\n').split('\t')[1].split()
        elif line.startswith('HIT\t'):
            _, ring, sig = line.rstrip('\n').split('\t')[:3]
            k = fnidx(sig)
            if k is None or k < minfn: continue
            W, L, PH = int(job[2]), int(job[4]), int(job[5])
            toks = ring.split()
            core = tuple(toks[:W])
            cores.setdefault(core, (sig, W, L, PH, job[0]))
rings = []; meta = []
for core, (sig, W, L, PH, jid) in sorted(cores.items()):
    for L2 in range(4, maxl + 1):
        if W + L2 > 20: break
        for ph in (0, 1):
            wall = ['W2' if (j + ph) % 2 == 0 else 'B4' for j in range(L2)]
            rings.append(' '.join(core + tuple(wall))); meta.append((core, sig, L, PH, L2, ph, jid))
open('walls_in.txt', 'w').write('\n'.join(rings) + '\n')
env = dict(os.environ, TBITS='22', QUIET='0')
out = subprocess.run(['nice', '-n', '15', './rgq', 'solvef', '7'], input='\n'.join(rings) + '\n', capture_output=True, text=True, env=env).stdout.strip().split('\n')
assert len(out) == len(rings), (len(out), len(rings))
for m, o in zip(meta, out):
    ring, sig, nodes = o.split('\t')
    print('\t'.join([' '.join(m[0]), 'orig_sig=' + m[1], 'orig_L=%d,ph=%d' % (m[2], m[3]), 'L=%d' % m[4], 'ph=%d' % m[5], 'n=%d' % (len(m[0]) + m[4]), sig, nodes]))
