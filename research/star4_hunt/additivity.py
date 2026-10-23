#!/usr/bin/env python3
"""Pair-attachment census: for each core (the 13 minimal *3 cores and the 35 flat *2 cores) add every W/B pair (one W pawn and
one B pawn on the same or adjacent files, files within one file of the core's files) and compare the value of core+pair with
nimber(core) xor nimber(pair alone) (pair alone must be a valid nimber position).  Counts additive / non-additive nimbers / other."""
import itertools, os, subprocess, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect import parse, fmt
H = './h4'
def ev(pos, width):
    open('/tmp/_add.txt', 'w').write("\n".join(pos) + "\n")
    out = subprocess.run([H, '--flat', '--width', str(width), '--max-entries', '8388608', '--evalbudget', '2000000', '--eval', '/tmp/_add.txt'], capture_output=True, text=True).stdout.splitlines()[1:]
    res = []
    for l in out:
        p = l.split('\t')
        if len(p) > 4 and p[3] in 'NLRP' and p[4].lstrip('-').isdigit(): res.append(int(p[4]))
        elif len(p) > 3 and p[3] in ('PASSED', 'BUDGET'): res.append(None)
        else: res.append(-1)
    return res
cores2 = [l.strip() for l in open('seeds/cores2_all.txt')]
cores3 = [l.strip() for l in open('seeds/cores3_all.txt')] + [l.strip() for l in open('seeds/w5p10_star3.txt')]
stats = collections.Counter(); weird = []
for label, cores in (('*2 cores', cores2), ('*3 cores', cores3)):
    for c in cores:
        w, b = parse(c)
        files = sorted({f for f, _ in w + b})
        lo, hi = files[0], files[-1]
        W = 8
        occ = set(w) | set(b)
        sqs_w = [(f, r) for f in range(max(0, lo - 1), min(W, hi + 2)) for r in range(2, 7) if (f, r) not in occ]
        sqs_b = [(f, r) for f in range(max(0, lo - 1), min(W, hi + 2)) for r in range(3, 8) if (f, r) not in occ]
        pairs = [(x, y) for x in sqs_w for y in sqs_b if abs(x[0] - y[0]) <= 1 and y[1] > x[1] - 1]
        full = [fmt(w + [x], b + [y]) for x, y in pairs]
        alone = [fmt([x], [y]) for x, y in pairs]
        base = ev([fmt(w, b)], W)[0]
        rf = ev(full, W); ra = ev(alone, W)
        for (x, y), f_, a_ in zip(pairs, rf, ra):
            if f_ is None or a_ is None: stats[(label, 'undecided')] += 1; continue
            if a_ < 0: stats[(label, 'pair alone not a nimber')] += 1; continue
            if f_ < 0: stats[(label, f'pair alone *{a_}: core+pair not a nimber')] += 1; continue
            if f_ == (base ^ a_): stats[(label, 'additive nimber')] += 1
            else:
                stats[(label, 'NON-additive nimber')] += 1; weird.append((c, x, y, base, a_, f_))
for k in sorted(stats): print(k, stats[k])
cnt=collections.Counter((w_[3],w_[4],w_[5]) for w_ in weird)
print('non-additive (core,pair,result) -> count:', dict(sorted(cnt.items())))
print('non-additive nimber cases:', len(weird))
for w_ in weird[:10]: print('  ', w_)
