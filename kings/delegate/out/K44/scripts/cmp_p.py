#!/usr/bin/env python3
"""cmp_p.py key result [outprefix]: D 'alone' outcome vs P result per class. key lines 'pos | class | cfg | D', result lines 'pos | X'."""
import sys, collections
key = {}
for l in open(sys.argv[1]):
    pos, nm, cn, d = [x.strip() for x in l.rstrip('\n').rsplit(' | ', 3)]
    key[pos] = (nm, cn, d)
tot = collections.Counter(); ag = collections.Counter(); bycfg = collections.defaultdict(lambda: [0, 0]); conf = collections.Counter()
n = 0
for l in open(sys.argv[2]):
    pos, x = [t.strip() for t in l.rstrip('\n').rsplit('|', 1)]
    if pos not in key: continue
    nm, cn, d = key[pos]
    n += 1
    if x == 'X': tot[('illegal', nm)] += 1; continue
    tot[nm] += 1
    bycfg[cn][0] += 1
    if x == d: ag[nm] += 1; bycfg[cn][1] += 1
    else: conf[(d, x)] += 1
print('positions %d; legal %d; agree %d' % (n, sum(v for k, v in tot.items() if not isinstance(k, tuple)), sum(ag.values())))
for nm in sorted(set(k for k in tot if not isinstance(k, tuple))): print('  %-34s %6d agree %6d' % (nm, tot[nm], ag[nm]))
print('disagreements (D, P):', dict(conf))
print('per config:', {c: tuple(v) for c, v in sorted(bycfg.items())})
