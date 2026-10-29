#!/usr/bin/env python3
"""agentB/analyze.py : join Phase A/B results (data/A_*.txt, data/B_*.txt, data/screen_cyl7x6_f3.txt), the sortie tables
(agentB/sorties_*.txt) and the mechanism files (agentB/mech_*.txt).  Prints (1) per configuration the counts pass/fail/pending and the
failure mechanisms, (2) the features of every passing group, (3) a test of two predictors of failure."""
import re, os, collections, sys
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
cfg = [l.split() for l in open(D + 'scripts/configs.txt') if l.strip() and not l.startswith('#')]
def rd_R(fn):
    d = {}
    if not os.path.exists(fn): return d
    for l in open(fn):
        m = re.match(r'R (.*?) \| contexts_checked (\d+) differ (\d+) parking_mismatch (\d+) \| first fail:(.*)', l)
        if m: d[m.group(1)] = (int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5).strip())
    return d
def rd_sort(fn):
    d = {}
    if not os.path.exists(fn): return d
    for l in open(fn):
        z, stm, mv = l.rstrip('\n').split(' | ')
        d.setdefault(z, {})[stm] = [tuple(x.split(':')) for x in mv.split()]
    return d
def feats(z, S):
    f = {}
    for s in 'wb':
        mv = S.get(z, {}).get(s, [])
        Ls = [int(x[2]) for x in mv if x[2].isdigit()]; LB = [int(x[2]) for x in mv if x[1] == 'B' and x[2].isdigit()]
        f[s] = dict(n=len(mv), nB=sum(x[1] == 'B' for x in mv), nZ=sum(x[1] == 'Z' for x in mv), nP=sum(x[1] == 'P' for x in mv),
                    exitonly=bool(mv) and all(x[1] == 'B' for x in mv), Lmax=max(Ls) if Ls else 0, LB=max(LB) if LB else 0)
    return f
rows = []
for name, board, zs, fz, dmin, rep in cfg:
    A = rd_R(D + ('data/screen_cyl7x6_f3.txt' if name == 'cyl7x6_f3' else 'data/A_%s.txt' % name)); B = rd_R(D + 'data/B_%s.txt' % name)
    S = rd_sort(D + 'agentB/sorties_%s.txt' % rep); M = {}
    mf = D + 'agentB/mech_%s.txt' % name
    if os.path.exists(mf):
        for l in open(mf):
            p = l.rstrip('\n').split(' | ')
            if len(p) >= 5: M.setdefault(p[0], []).append(p)
    cnt = collections.Counter(); mech = collections.Counter()
    for z, (n, d, pm, ff) in A.items():
        if d: st = 'fail'
        elif z in B: st = 'fail-B' if B[z][1] else 'pass'
        else: st = 'pass' if n < 300 or name == 'cyl7x6_f3' else 'pending'
        cnt[st] += 1
        mk = '-'
        if st == 'fail' and z in M:
            mk = '+'.join(sorted(set((p[4].split()[0] + ':' + p[5]) if p[4].startswith('A') else p[4] for p in M[z])))
            mech[mk] += 1
        rows.append((name, z, st, feats(z, S), mk, ff if st == 'fail' else ''))
    print('CONFIG %-18s classes %3d  %s' % (name, len(A), dict(cnt)))
    for k, v in mech.most_common(): print('        mechanism %-40s %d' % (k, v))
print()
print('PASSING groups (pass or pending):')
for r in rows:
    if r[2] in ('pass', 'pending'):
        f = r[3]
        print('%-18s %-8s %-28s w:n%d B%d Lmax%d LB%d b:n%d B%d Lmax%d LB%d' % (r[0], r[2], r[1], f['w']['n'], f['w']['nB'], f['w']['Lmax'], f['w']['LB'], f['b']['n'], f['b']['nB'], f['b']['Lmax'], f['b']['LB']))
