#!/usr/bin/env python3
"""K44 extra runs with lk (referee-style solver, no 64-square limit): class tallies over a cfg file of cyl:WxH.
usage: lk_extra.py W H cfgfile tag"""
import subprocess, sys, os, re, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, cf, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
tot = collections.Counter(); rare = []
out = open(D + '/logs/extra_%s.txt' % tag, 'w')
n = 0
for line in open(cf):
    line = line.strip()
    if not line: continue
    rg, cfg = line.split('|'); pairs = ','.join(cfg.split())
    margin = 'free' if rg == 'all' else 'F' + rg
    p = subprocess.run([D + '/bin/lk', 'classify', 'cyl:%dx%d' % (W, H), pairs, margin], capture_output=True, text=True)
    cnt = collections.Counter(); nd = 0
    for l in p.stdout.splitlines():
        m = re.match(r'  (\S.*?)\s{2,}(\d+)\s+e\.g\.', l)
        if m: cnt[m.group(1).strip()] += int(m.group(2))
        m = re.match(r'distinct other signatures: (\d+)', l)
        if m: nd = int(m.group(1))
    n += 1
    for k, v in cnt.items(): tot[k] += v
    out.write('%s | %s | %s | other-sigs %d\n' % (rg, cfg, dict(cnt), nd)); out.flush()
out.write('TOTAL configs %d: %s\n' % (n, dict(tot))); out.close()
print(tag, 'configs', n, dict(tot))
