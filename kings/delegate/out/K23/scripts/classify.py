#!/usr/bin/env python3
"""classify.py WIDTH FILE_P FILE_F [ZPREFIX_TOKENS=4]: for each context (Z + context pawns, e.p. '-'), report whether the context
has a passed pawn (textbook test on the context pawns only, cylinder wrap), the frozen pair (convention) and the P pair.
Prints counts by (passer?, frozen pair, agree?) and the passer-free contexts with frozen pair (L,W) where P differs / agrees."""
import sys, collections
W = int(sys.argv[1]); ZN = int(sys.argv[4]) if len(sys.argv) > 4 else 4
def load(fn):
    d = {}
    for l in open(fn):
        pos, r = l.rstrip('\n').rsplit(' | ', 1); t = pos.split()
        d.setdefault(' '.join(t[:-2]), {})[t[-2]] = r.split()[0]
    return d
P, F = load(sys.argv[2]), load(sys.argv[3])
def pawns(key):
    t = key.split()[ZN:]
    wp = [(ord(x[1]) - 97, int(x[2:])) for x in t if x[0] == 'P']
    bp = [(ord(x[1]) - 97, int(x[2:])) for x in t if x[0] == 'p']
    return wp, bp
def has_passer(wp, bp):
    for f, r in wp:
        if not any((bf - f) % W in (0, 1, W - 1) and br > r for bf, br in bp): return True
    for f, r in bp:
        if not any((wf - f) % W in (0, 1, W - 1) and wr < r for wf, wr in wp): return True
    return False
cnt = collections.Counter(); ex = collections.defaultdict(list)
for k in P:
    wp, bp = pawns(k)
    ps = has_passer(wp, bp); p = P[k]['w'] + P[k]['b']; f = F[k]['w'] + F[k]['b']
    cnt[(ps, f == p)] += 1
    if not ps: ex[(f, f == p)].append((k, p))
for key in sorted(cnt): print('passer' if key[0] else 'passer-free', 'P==frozen' if key[1] else 'P!=frozen', cnt[key])
print('passer-free contexts by frozen pair and agreement:')
for key in sorted(ex): print(' frozen', key[0], 'agree' if key[1] else 'DIFFER', len(ex[key]))
if len(sys.argv) > 5:
    for k, p in ex[('LW', False)][:int(sys.argv[5])]: print('  LW-frozen but P =', p, ':', ' '.join(k.split()[ZN:]))
