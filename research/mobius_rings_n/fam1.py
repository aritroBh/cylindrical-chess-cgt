import sys; sys.path.insert(0,'.')
from fam import *
import itertools, collections
bases = {
 'n7p8': 'B6 W2 W3 B6 B7 W3 W6B7',
 'n8p8': 'B7 W3 W3 B6 W3 B6 B6 W2',
 'n10a': 'B4 W2 B6 W2 W3 B6 B7 W3 B7 W5',
 'n10b': 'B6 W3 B7 W2 W3 B6 B7 W2 B6 W3',
}
res = collections.defaultdict(list)
for name, s in bases.items():
    t = s.split()
    blocks = [[x] for x in SINGLES] + [[x,y] for x in SINGLES for y in SINGLES]
    for L in (1,2):
        for i in range(len(t)-L+1):
            b = t[i:i+L]
            if b not in blocks: blocks.append(b)
    cand = []
    for m in (1,2):
        for k in range(len(t)+1):
            for b in blocks:
                cand.append((name,k,' '.join(b),m,' '.join(ins(t,k,b,m))))
    sig = solve([c[-1] for c in cand])
    c2 = collections.Counter(sig)
    print(name, len(cand), dict(c2.most_common(6)), flush=True)
    for c,sg in zip(cand,sig):
        if sg in ('NNPN','NNNP'): res[name].append((sg,)+c[1:])
import json; json.dump(res, open('results/fam_stage1.json','w'))
for name in res:
    print(name, len(res[name]))
    for r in res[name][:40]: print('  ',r)
