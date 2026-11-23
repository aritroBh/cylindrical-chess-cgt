"""K49: does a small feature set determine the normal-play class?  Counts placements of feature vectors with >1 class."""
import load, sys
from collections import defaultdict, Counter
def cd(a, b, W): d = (a - b) % W; return min(d, W - d)
def feats(pos, W, H, which):
    wk, bk, p, s = pos.split()
    (wf, wr), (bf, br), (pf, pr) = map(load.sq, (wk, bk, p))
    sd = lambda f: ((f - pf + W // 2) % W) - W // 2
    F = {'s': s, 'r': pr, 'wdf': cd(wf, pf, W), 'wdr': wr - pr, 'bdf': cd(bf, pf, W), 'bdr': br - pr,
         'side': (sd(wf) * sd(bf) > 0) - (sd(wf) * sd(bf) < 0), 'kdf': cd(wf, bf, W)}
    return tuple(F[k] for k in which)
which = sys.argv[1].split(',')
for W in (3, 5, 6, 7, 8):
    for H in (6, 8):
        t = load.load(W, H); g = defaultdict(Counter)
        for pos, k in t.items(): g[feats(pos, W, H, which)][k] += 1
        amb = sum(1 for v in g.values() if len(v) > 1)
        print(W, H, len(g), 'ambiguous', amb, sum(sum(v.values()) for v in g.values() if len(v) > 1))
