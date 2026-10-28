#!/usr/bin/env python3
"""Summarise the kg roots files: counts of value classes per board / region, split by faithful configs."""
import sys, glob, json, collections, re, os
sys.path.insert(0, os.path.dirname(__file__))
from classes import parse, order
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
iD = order.index('dud')
HOT = {'{+|}', '{|-}', '{+|-}', '{+|0}', '{0|-}', '{+|on}', '{off|-}'}
out = {}
rows = []
import gzip
for rf in sorted(glob.glob(D + '/logs/roots_*.txt') + glob.glob(D + '/logs/roots_*.txt.gz')):
    base = os.path.basename(rf)[len('roots_'):].replace('.txt.gz', '').replace('.txt', '')
    lg = D + '/logs/' + base + ('_free' if not re.search(r'_m\d$', base) else '') + '.log'
    if not os.path.exists(lg):
        continue
    faith = {}
    for l in open(lg):
        m = re.match(r'CONFIG (.*?) : nodes (\d+)  faithful (\d)', l)
        if m: faith[m.group(1).strip()] = int(m.group(3))
    cnt = collections.Counter(); cntf = collections.Counter(); nconf = len(faith)
    ex = {}
    nstop = 0; nshort = 0
    for l in (gzip.open(rf, 'rt') if rf.endswith('.gz') else open(rf)):
        cn, pos, nm, sh, sig = parse(l)
        nstop += int(sh) >= 2; nshort += int(sh) % 2
        cn = cn.strip()
        quiet = sig[2 * iD:2 * iD + 2] == '11'
        if nm == 'UNMATCHED': cls = 'loopy, not classified (quiet)' if quiet else 'loopy, not classified (decisive)'
        elif nm in HOT: cls = 'decisive ' + nm
        else: cls = nm
        cnt[cls] += 1
        if faith.get(cn, 0): cntf[cls] += 1
        if cls in ('+1', '-1', '*', '{1|0}', '{0|-1}', '0', 'tis', 'tisn', '{on|off}') and (cls, faith.get(cn, 0)) not in ex:
            ex[(cls, faith.get(cn, 0))] = cn + ' :: ' + pos
    out[base] = {'configs': nconf, 'faithful_configs': sum(faith.values()), 'roots': sum(cnt.values()), 'stopper_roots': nstop, 'short_roots': nshort, 'classes': dict(cnt), 'classes_faithful_only': dict(cntf),
                 'examples': {'%s/faithful=%d' % k: v for k, v in ex.items()}}
json.dump(out, open(D + '/summary_classes.json', 'w'), indent=1)
keys = ['dud', 'on', 'off', '0', '*', '+1', '-1', '{1|0}', '{0|-1}', 'tis', 'tisn', '{on|off}', 'loopy, not classified (quiet)', 'loopy, not classified (decisive)']
print('| board/region | cfgs (faithful) | roots | ' + ' | '.join(keys) + ' | decisive named |')
print('|' + '---|' * (len(keys) + 4))
for b, v in out.items():
    c = v['classes']; dec = sum(x for k, x in c.items() if k.startswith('decisive'))
    print('| %s | %d (%d) | %d | %s | %d |' % (b, v['configs'], v['faithful_configs'], v['roots'], ' | '.join(str(c.get(k, 0)) for k in keys), dec))
