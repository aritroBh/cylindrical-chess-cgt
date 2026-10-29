"""compare the referee's own solver (myx.py) with ref3 (P) and mine.c (p, bb=EPW, bw=EPB) on the K30 position lists. usage: mycmp.py cyl|flat"""
import sys
import myx
from myx import *
n = sys.argv[1]
res = {m: solve(m)[1] for m in ('P','EPW','EPB')}
def parse(line):
    toks = line.split(); stm = 0 if toks[-2] == 'w' else 1
    wk=bk=wp=bp=None
    for t in toks[:-2]:
        s_ = P(t[1:])
        if t[0]=='K': wk=s_
        elif t[0]=='k': bk=s_
        elif t[0]=='P': wp=s_
        elif t[0]=='p': bp=s_
    assert wp in (None, D7)
    return (stm, wk, bk, wp, bp)
files = {'P': ['ref3_%s.out' % n, 'mine_%s_p.out' % n], 'EPW': ['mine_%s_bb.out' % n], 'EPB': ['mine_%s_bw.out' % n]}
for model, fl in files.items():
    for f in fl:
        tot = diff = ill = 0
        from collections import Counter
        c = Counter()
        for line in open(f):
            pos, val = line.rsplit(' | ', 1); val = val.strip()
            st = parse(pos)
            tot += 1
            mv = res[model].get(st)
            if mv is None: ill += 1; continue
            c[mv] += 1
            if mv != val: diff += 1
        print(n, model, 'vs', f, ': positions', tot, 'not legal in own generator', ill, 'differences', diff, dict(c))
