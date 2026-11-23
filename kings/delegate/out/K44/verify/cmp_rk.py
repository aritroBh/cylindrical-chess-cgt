#!/usr/bin/env python3
"""Compare the referee solver rk (verify/rk.cpp) with kg44's per-case signature tables (logs/fsig_new_W_R.txt.xz).
For every (configuration, region) line of cfg/cylWx6_w6_R.txt, rk classifies every full-pawn-set root; the multiset
{B34 signature: number of roots} is compared with the fsig rows of the same case (named and UNMATCHED rows alike).
usage: cmp_rk.py RKBIN W REGION   (REGION = free, m0, m1, m2)"""
import lzma, subprocess, sys, os, collections
rk, W, R = sys.argv[1], int(sys.argv[2]), sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.dirname(here)
code = {'W': '0', 'D': '1', 'L': '2'}
fs = os.path.join(base, 'logs', f'fsig_new_{W}_{R}.txt.xz')
ref = collections.defaultdict(collections.Counter)
have = os.path.exists(fs)
for line in (lzma.open(fs, 'rt') if have else []):
    if line.startswith('EX') or line.startswith('#'):
        continue
    f = line.rstrip('\n').split('|')
    # board|region|faithful|config|class...|roots|short|stopper|sig ; class may contain '|'
    sig = f[-1]; roots = int(f[-4]); key = (f[1], f[3].strip())
    ref[key][sig] += roots
cases = diff = 0; nroots = 0; allsig = set(); names = collections.Counter(); named = []
for line in open(os.path.join(base, 'cfg', f'cyl{W}x6_w6_{R}.txt')):
    reg, cfg = line.strip().split('|')
    pawns = ','.join(cfg.split())
    env = dict(os.environ, RK_ALL='1')
    out = subprocess.run([rk, f'cyl:{W}x6', reg, pawns], capture_output=True, text=True, env=env).stdout
    mine = collections.Counter()
    for l in out.splitlines():
        if l.startswith('K'):
            parts = l.split()
            sig = ''.join(code[c] for p in parts[3:] for c in p.split(':')[-1])
            mine[sig] += 1; names[parts[2]] += 1
            if parts[2] in ('over', 'under', '+1', '-1', '*', '{1|0}', '{0|-1}'): named.append((parts[2], reg, cfg, parts[0], parts[1]))
    nroots += sum(mine.values()); cases += 1
    for s_ in mine: allsig.add(s_)
    if have and mine != ref[(reg, cfg)]:
        diff += 1
        print('DIFF', W, R, reg, cfg, sum(mine.values()), sum(ref[(reg, cfg)].values()))
open(os.path.join(here, f'sigs_{W}_{R}.txt'), 'w').write(''.join(x + '\n' for x in sorted(allsig)))
print(f'W={W} {R}: compared {have}, cases {cases} roots {nroots} differing cases {diff} (fsig cases {len(ref)})')
print('  classes', dict(sorted(names.items())))
for x in named: print('  NAMED', *x)
