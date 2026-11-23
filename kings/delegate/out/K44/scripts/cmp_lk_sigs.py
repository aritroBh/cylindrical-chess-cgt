#!/usr/bin/env python3
"""K44: stronger comparison of kg44 with the referee-style lk: for every (config, region) case compare the SET of distinct unclassified B34
signatures (lk prints them with DUMPSIG=1 in its own context order and its own outcome coding; translated here)."""
import subprocess, sys, os, re, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load
lk_order = ["0","*","+1","-1","+2","-2","+3","-3","1/2","-1/2","up","down","up*","down*","*2","on","off","dud","over","under","tis","tisn","{+|}","{|-}","{+|-}","{+|0}","{0|-}","{+|on}","{off|-}","{1|0}","{0|-1}","{2|0}","{0|-2}","{on|off}"]
kg_order = ["0","*","+1","-1","+2","-2","+3","-3","1/2","-1/2","up","down","up*","down*","*2","on","off","dud","over","under","tis","tisn","{+|}","{|-}","{+|-}","{+|0}","{0|-}","{1|0}","{0|-1}","{2|0}","{0|-2}","{+|on}","{off|-}","{on|off}"]
perm = [lk_order.index(n) for n in kg_order]
def translate(s):
    out = ''
    for n in perm:
        out += '%d%d' % (2 - int(s[2 * n]), 2 - int(s[2 * n + 1]))
    return out
Ws = [int(a) for a in sys.argv[1].split(',')]; regs = sys.argv[2].split(',')
rows, _ = load('new')
kgs = collections.defaultdict(set)
for r in rows:
    if r['nm'] == 'UNMATCHED': kgs[(r['W'], r['reg'], r['cfg'].strip())].add(r['sig'])
out = open(D + '/logs/cmp_lk_sigs_%s_%s.txt' % ('_'.join(map(str, Ws)), '_'.join(regs)), 'w')
nbad = ntot = nsig = 0
env = dict(os.environ); env['DUMPSIG'] = '1'
for W in Ws:
    for reg in regs:
        for line in open(D + '/cfg/cyl%dx6_w6_%s.txt' % (W, reg)):
            line = line.strip()
            if not line: continue
            rg, cfg = line.split('|')
            margin = 'free' if rg == 'all' else 'F' + rg
            p = subprocess.run([D + '/bin/lk', 'classify', 'cyl:%dx6' % W, ','.join(cfg.split()), margin], capture_output=True, text=True, env=env)
            mine = {translate(l[4:].strip()) for l in p.stdout.splitlines() if l.startswith('SIG ')}
            key = (W, reg, cfg.strip())
            ntot += 1; nsig += len(mine)
            if mine != kgs[key]:
                nbad += 1; out.write('DIFF %s lk %d kg %d\n' % (key, len(mine), len(kgs[key])))
            out.flush()
out.write('TOTAL cases %d, signatures compared %d, cases with a different signature set %d\n' % (ntot, nsig, nbad)); out.close()
print('cases', ntot, 'signatures', nsig, 'differences', nbad)
