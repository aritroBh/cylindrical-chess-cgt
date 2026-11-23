#!/usr/bin/env python3
"""K44: run the referee-style implementation lk (scripts/lk_ref.cpp, bin/lk) on every configuration/region of the cfg files
and compare its class counts with kg44's (logs/fsig_new_*).  Roots = distinct full-pawn-set roots."""
import subprocess, sys, os, re, collections, glob
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D + '/scripts')
from agg import load
Ws = [int(a) for a in sys.argv[1].split(',')]
regs = sys.argv[2].split(',')
rows, _ = load('new')
kg = collections.defaultdict(collections.Counter); kgd = collections.defaultdict(set); kgfa = {}
for r in rows:
    key = (r['W'], r['reg'], r['cfg'].strip())
    kg[key][r['nm']] += r['cnt']
    if r['nm'] == 'UNMATCHED': kgd[key].add(r['sig'])
    kgfa[key] = r['faith']
def norm(nm):
    parts = nm.split('='); return parts[0]
out = open(D + '/logs/cmp_lk_%s_%s.txt' % ('_'.join(map(str, Ws)), '_'.join(regs)), 'w')
nbad = 0; ntot = 0
for W in Ws:
    for reg in regs:
        for line in open(D + '/cfg/cyl%dx6_w6_%s.txt' % (W, reg)):
            line = line.strip()
            if not line: continue
            rg, cfg = line.split('|')
            pairs = ','.join(cfg.split())
            margin = 'free' if rg == 'all' else 'F' + rg
            p = subprocess.run([D + '/bin/lk', 'classify', 'cyl:%dx6' % W, pairs, margin], capture_output=True, text=True)
            cnt = collections.Counter(); nd = None
            for l in p.stdout.splitlines():
                m = re.match(r'  (\S.*?)\s{2,}(\d+)\s+e\.g\.', l)
                if m: cnt[m.group(1).strip()] += int(m.group(2))
                m = re.match(r'distinct other signatures: (\d+)', l)
                if m: nd = int(m.group(1))
            key = (W, reg, cfg.strip())
            mine = collections.Counter()
            for nm, c in kg[key].items():
                mine['other' if nm == 'UNMATCHED' else nm.split('=')[0]] += c
            lkc = collections.Counter({k.split('=')[0]: v for k, v in cnt.items()})
            ok = (mine == lkc) and (nd == len(kgd[key]))
            ntot += 1
            if not ok:
                nbad += 1
                out.write('DIFF %s %s | kg %s nd %d | lk %s nd %s\n' % (key, rg, dict(mine), len(kgd[key]), dict(lkc), nd))
            out.flush()
out.write('TOTAL configs %d with differences %d\n' % (ntot, nbad)); out.close()
print('TOTAL configs %d with differences %d' % (ntot, nbad))
