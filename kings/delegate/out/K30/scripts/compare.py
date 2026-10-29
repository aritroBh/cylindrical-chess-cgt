#!/usr/bin/env python3
"""compare.py -- K30 step 2d: values of every position the checkers visit, from three implementations:
   own kpm.py (SPEC.md only), K24's mine.c (SPEC.md only; models p, bb = EPW, bw = EPB), K7's kp_p.c --pmodel (P only).
usage: compare.py cyl:8x8|flat:8x8"""
import sys, subprocess, collections, os
sys.path.insert(0, '.')
from k30lib import *
spec = sys.argv[1]
B = Board(spec)
BIN = os.path.abspath('../bin')
pos = set()
# (1) all of S and every White-to-move position after a Black move from S
S = all_S(B)
pairs, wst, stats = check_S_closure(B, S)
pos |= set(S) | wst
SET_S = set(S) | wst
# (2) the root, its children and grandchildren
X = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
pos.add(X)
after = []
for lab, k, t in gen(B, X):
    pos.add(t)
    for l2, k2, t2 in gen(B, t):
        if k2 == 'n':
            pos.add(t2)
        if l2 == 'd8d7x':
            after.append(t2)
# (3) the positions of the tau check (check_A): White any move, Black tau-style king moves (all king moves here)
seenW = set(after); dq = collections.deque(after)
while dq:
    w = dq.popleft()
    for l3, k3, nt in gen(B, w):
        if nt[4] == (): continue
        pos.add(nt)
        for l4, k4, u in gen(B, nt):
            if k4 == 'n' and u[4] == nt[4] and u not in seenW:
                seenW.add(u); dq.append(u)
pos |= seenW
SET_TAU = set(seenW)
for w in list(seenW):
    for l3, k3, nt in gen(B, w):
        if nt[4] != (): SET_TAU.add(nt)
# (4) the Kf7 e5 line (Black pushes, White any move), deduplicated
f7 = [t for l, k, t in gen(B, X) if l == 'e6f7'][0]
fr = {[t for l, k, t in gen(B, f7) if l == 'e7e5'][0]}
pos |= fr
for it in range(5):
    nf = set()
    for t in fr:
        for l, k, x in gen(B, t):
            if k != 'n': continue
            pos.add(x)
            for l2, k2, y in gen(B, x):
                if k2 == 'n' and l2[0] == 'e' and l2[2] == 'e':
                    pos.add(y); nf.add(y)
    fr = nf
# (5) sigma states for the three sorties
X0, sigma = make_sigma(B)
SET_SIG = set()
for sortie in (B.sq('e5'), B.sq('d5'), B.sq('f5')):
    dq = collections.deque([X0]); sW = {X0}; sB = set()
    while dq:
        p = dq.popleft()
        for t in sigma(p, sortie):
            if t[3] == () and t[4] == (): continue
            if t in sB: continue
            sB.add(t)
            for lab, k, nt in gen(B, t):
                if nt[3] == () and nt[4] == (): continue
                if nt not in sW:
                    sW.add(nt); dq.append(nt)
    pos |= sW | sB
    SET_SIG |= sW | sB
pos = [p for p in pos if legal(B, p)]
pos.sort(key=lambda p: fmt(B, p))
lines = [fmt(B, p) for p in pos]
print(spec, len(lines), 'positions', flush=True)
assert len(lines) < 400000
open('../logs/compare_positions_%s.txt' % spec.replace(':', '_'), 'w').write('\n'.join(lines) + '\n')

def run(cmd, text, chunk=4000):
    """mine.c reads at most 4096 query lines per run, so feed it in chunks"""
    out = {}
    ls = text.splitlines()
    for i in range(0, len(ls), chunk):
        r = subprocess.run(cmd, input='\n'.join(ls[i:i + chunk]) + '\n', capture_output=True, text=True)
        for ln in r.stdout.splitlines():
            if ln.startswith('#') or ln.startswith('[') or ' | ' not in ln:
                continue
            a, b = ln.split(' | ', 1)
            out[a] = b.split()[0]
    return out

text = '\n'.join(lines) + '\n'
nice = ['nice', '-n', '15']
res = {}
res[('mine', 'P')] = run(nice + [BIN + '/mine', '--board', spec, '--model', 'p'], text)
res[('mine', 'EPW')] = run(nice + [BIN + '/mine', '--board', spec, '--model', 'bb'], text)
res[('mine', 'EPB')] = run(nice + [BIN + '/mine', '--board', spec, '--model', 'bw'], text)
res[('kpp', 'P')] = run(nice + [BIN + '/kpp', '--pmodel', '--board', spec, '--ep', 'on', '--cap', '1'], text)
for model in ('P', 'EPW', 'EPB'):
    idx, pl, val, mv = solve(B, model, pos)
    own = {fmt(B, p): val[idx[p]] for p in pos}
    cnt = collections.Counter(own.values())
    if model in ('P', 'EPB'):
        bad = [p for p in SET_S if val[idx[p]] != 'D']
        bad2 = [p for p in SET_SIG if val[idx[p]] == 'L']
        print('%s model %s: all %d positions of S and their White-to-move successors are D: %s; the %d positions of sigma are never L: %s' % (spec, model, len(SET_S), not bad, len(SET_SIG), not bad2), flush=True)
        assert not bad and not bad2
    if model == 'EPW':
        bad = [p for p in SET_TAU if val[idx[p]] == 'W']
        print('%s model EPW: the %d positions of the tau check are never W: %s' % (spec, len(SET_TAU), not bad), flush=True)
        assert not bad
    for impl in ('mine', 'kpp'):
        if (impl, model) not in res:
            continue
        o = res[(impl, model)]
        miss = [l for l in lines if l not in o]
        diff = [l for l in lines if l in o and o[l] != own[l]]
        print('%s model %s: own kpm vs %s: %d positions compared (own values %s), %d missing, %d differ' % (spec, model, impl, len(lines) - len(miss), dict(cnt), len(miss), len(diff)), flush=True)
        for l in (miss + diff)[:5]:
            print('    ', l, own[l], o.get(l))
print('done')
