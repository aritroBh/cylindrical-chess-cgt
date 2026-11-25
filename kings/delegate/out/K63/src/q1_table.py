"""K63 question 1: table of chess (model C) bounds at cap 1 for one group: kpsolve (plain), kp39 --refine, own39 bounds A
and B with refinement.  Checks that kp39 --refine and own39 agree on every position and move value (CHECKED-2), and that
the plain bounds are never tighter than the refined ones.  Values White's view; a pair (A, B) with A = B is exact.
usage: python3 q1_table.py <tag>   (reads logs/<tag>_kp.out, <tag>_kp39r.out, <tag>_own_A.out, <tag>_own_B.out)"""
import sys

tag = sys.argv[1]
ORDER = {'W': 2, 'D': 1, 'L': 0}


def kp(fn):
    out = {}
    for line in open(fn):
        if ' | ' not in line:
            continue
        parts = [x.strip() for x in line.rstrip('\n').split(' | ')]
        a, b = parts[1].split()
        mv = {}
        for p in parts[2:]:
            t = p.split()
            if not t:
                continue
            if t[0] in ('A:', 'B:'):
                bound, toks = t[0][0], t[1:]
            else:
                bound, toks = 'S', t
            for m in toks:
                k, v = m.rsplit(':', 1)
                mv.setdefault(k, {})[bound] = v
        out[parts[0]] = ((a, b), mv)
    return out


def own(fa, fb):
    out = {}
    for fn, bound in ((fa, 'A'), (fb, 'B')):
        for line in open(fn):
            if ' | ' not in line:
                continue
            parts = [x.strip() for x in line.rstrip('\n').split(' | ')]
            pos, v = parts[0], parts[1]
            e = out.setdefault(pos, [{}, {}])
            e[0][bound] = v
            for m in (parts[2].split() if len(parts) > 2 else []):
                k, x = m.rsplit(':', 1)
                e[1].setdefault(k, {})[bound] = x
    return {p: ((e[0]['A'], e[0]['B']), e[1]) for p, e in out.items()}


def norm(name):  # kpsolve and own39 write moves the same way (e.g. Kc4d4, Pb2b4); keep as is
    return name


def kpmoves(mv):
    res = {}
    for k, d in mv.items():
        if 'A' in d or 'B' in d:
            res[k] = (d.get('A'), d.get('B'))
        else:  # single list (bounds equal)
            v = list(d.values())[0]
            res[k] = (v, v)
    return res


import os
ow = own('logs/%s_own_A.out' % tag, 'logs/%s_own_B.out' % tag)
ONLY_OWN = not (os.path.exists('logs/%s_kp39r.out' % tag) and os.path.getsize('logs/%s_kp39r.out' % tag) > 0)
ref = ow if ONLY_OWN else kp('logs/%s_kp39r.out' % tag)
plain = kp('logs/%s_kp.out' % tag) if os.path.exists('logs/%s_kp.out' % tag) else {p: (('?', '?'), {}) for p in ow}
if ONLY_OWN:
    print('# NOTE: kp39 --refine output missing: own39 only (COMPUTED-1); "kp39r = own39" below compares own39 with itself')


def fmt(ab):
    a, b = ab
    return a if a == b else '(%s,%s)' % (a, b)


ndiff = nlooser = 0; nmoves = nexact = 0
print('# %s: chess at cap 1. Position value and every move value as bounds (A, B), White\'s view; one letter = exact.' % tag)
print('# columns: refined (kp39 --refine = own39 with refinement, CHECKED-2 when "agree") | plain kpsolve')
for pos in ref:
    rv, rm = ref[pos]; ov, om = ow[pos]; pv, pm = plain[pos]
    rm = {k: (d['A'], d['B']) for k, d in rm.items()} if ONLY_OWN else kpmoves(rm)
    pm = kpmoves(pm)
    om = {k: (d['A'], d['B']) for k, d in om.items()}
    agree = rv == ov and rm == om
    if not agree:
        ndiff += 1
    print('%-32s value %-6s (plain %-6s) %s' % (pos, fmt(rv), fmt(pv), 'kp39r = own39' if agree else 'DISAGREE kp39r %s own39 %s' % (rm, om)))
    for k in sorted(rm):
        nmoves += 1
        nexact += rm[k][0] == rm[k][1]
        a, b = rm[k]; pa, pb = pm.get(k, ('?', '?'))
        if pa != '?' and (ORDER[pa] < ORDER[a] or ORDER[pb] > ORDER[b]):
            nlooser += 1
        print('      %-8s %-7s (plain %s)' % (k, fmt(rm[k]), fmt(pm.get(k, ('?', '?')))))
print('# positions where kp39 --refine and own39 disagree: %d; moves %d, exact (refined) %d; plain tighter than refined: %d'
      % (ndiff, nmoves, nexact, nlooser))
