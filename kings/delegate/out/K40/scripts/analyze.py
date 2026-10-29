"""K40: classes of K+P v K positions by their results against the test games.

For each position (x, s): theta = least integer n in [-12, 12] with x (+) n a White win (n > 0: White has
n spare moves; n < 0: Black has -n), 'none' if no n in range wins, '<=-12' if n = -12 wins.  The class is
theta together with the results against on, off, dud, over, under, *, up, down, +-1.
Usage: python analyze.py [normal]   -> prints a JSON line per board and writes data/classes[_normal].json
"""
import json, lzma, os, sys
from collections import Counter, defaultdict

D = os.path.dirname(os.path.abspath(__file__)) + '/..'
tag = 'normal_' if 'normal' in sys.argv else ''
boards = [(w, h) for h in (6, 8) for w in range(3, 9)]
allres = {}
for W, H in boards:
    fh = lzma.open(f'{D}/data/sums_{tag}cyl_{W}x{H}.tsv.xz', 'rt')
    cols = fh.readline().split()[1:]
    ii = [cols.index(str(n)) for n in range(-12, 13)]
    other = ['on', 'off', 'dud', 'over', 'under', '*', 'up', 'down', '+-1']
    oi = [cols.index(c) for c in other]
    cls = Counter(); ex = {}; nonmono = 0
    for ln in fh:
        pos, *r = ln.rstrip('\n').split('\t')
        v = [r[i] for i in ii]
        if 'W' in v:
            k = v.index('W')
            if 'D' in v[k:]:
                nonmono += 1
            theta = '<=-12' if k == 0 else str(k - 12)
        else:
            theta = 'none'
        stm = pos.split()[-1]
        key = stm + ' theta=' + theta + ' ' + ' '.join(f'{c}:{r[i]}' for c, i in zip(other, oi))
        cls[key] += 1
        ex.setdefault(key, pos)
    res = {'board': f'cyl:{W}x{H}', 'nonmonotone': nonmono,
           'classes': {k: [cls[k], ex[k]] for k in sorted(cls)}}
    allres[f'{W}x{H}'] = res
    print(json.dumps(res))
json.dump(allres, open(f'{D}/data/classes{"_normal" if tag else ""}.json', 'w'), indent=1)
