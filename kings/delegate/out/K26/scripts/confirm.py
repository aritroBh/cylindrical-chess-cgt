#!/usr/bin/env python3
"""K26 part 4a: confirm root values and complete move lists of selected groups with ref3m (independent) against kpp.

  confirm.py groups.json out.json

groups.json: list of {"id","board","class","H","wk":[...],"bk":[...],"wp":[...],"bp":[...]}.
Each group is checked in both orientations (as given and colour-flipped: rank r -> H+1-r, colours swapped), at every root
(king states x side to move).  A root is CHECKED-2 when kpp --pmodel --moves and ref3m --moves agree on the root value and
on the multiset of (move, value) after normalising promotions (kpp prints one entry per promotion piece, ref3m 'promo').
Also checks the colour-flip symmetry of kpp: the value at a root of the flipped group is the negation of the value at the
corresponding root of the original group.
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *

safe_nice()
gfile, ofile = sys.argv[1], sys.argv[2]
CHESS = '--chess' in sys.argv[3:]
groups = json.load(open(gfile))


def sqparse(s):
    return (FILES.index(s[0]) + 1, int(s[1:]))


def sqname(f, r):
    return FILES[f - 1] + str(r)


def flip_sq(s, H):
    f, r = sqparse(s)
    return sqname(f, H + 1 - r)


def flip_group(g):
    H = g['H']
    fl = lambda lst: [flip_sq(s, H) for s in lst]
    return {'id': g['id'] + '~', 'board': g['board'], 'class': g.get('class', '') + '~', 'H': H,
            'wk': fl(g['bk']), 'bk': fl(g['wk']), 'wp': fl(g['bp']), 'bp': fl(g['wp'])}


def roots(g):
    out = []
    for wk in g['wk']:
        for bk in g['bk']:
            for s in 'wb':
                out.append(' '.join(['K' + wk, 'k' + bk] + ['P' + x for x in g['wp']] + ['p' + x for x in g['bp']] + [s, '-']))
    return out


def norm_kpp(moves):
    seen = set()
    out = []
    for nm, v in moves:
        if '=' in nm:
            key = ('promo', nm[1:5], v)
            if key in seen:
                continue
            seen.add(key)
            out.append(('promo', v))
        else:
            out.append((nm, v))
    return sorted(out)


def norm_ref(moves):
    return sorted(moves)


def parse_ref(line):
    parts = line.split(' | ')
    toks = parts[1].split()
    val = toks[0]
    mv = []
    for t in toks[1:]:
        nm, v = t.rsplit(':', 1)
        mv.append((nm, v))
    return val, mv


rep = []
tot_roots = tot_ok = 0
for g in groups:
    flg = flip_group(g)
    res = {}
    for gg in (g, flg):
        L = roots(gg)
        a, _ = run_solver(L, gg['board'], 'kpp', moves=True)
        b, _ = run_solver(L, gg['board'], 'ref3m', moves=True)
        c = run_solver(L, gg['board'], 'kp', moves=False)[0] if CHESS else ['x | ?'] * len(L)   # chess, cap 1: lower and upper bound (--chess)
        res[gg['id']] = (L, a, b, c)
    entry = {'id': g['id'], 'board': g['board'], 'class': g.get('class'), 'roots': [], 'all_agree': True}
    for gg in (g, flg):
        L, a, b, c = res[gg['id']]
        for pos, la, lb, lc in zip(L, a, b, c):
            stm, v1, mv1 = parse_line(la)
            v2, mv2 = parse_ref(lb)
            ok_val = v1 == v2
            ok_mv = norm_kpp(mv1) == norm_ref(mv2)
            tot_roots += 1
            tot_ok += ok_val and ok_mv
            entry['all_agree'] &= ok_val and ok_mv
            entry['roots'].append({'pos': pos, 'value': v1, 'chess_cap1_bounds': lc.split(' | ')[1].strip() if CHESS else None,
                                   'moves': ' '.join('%s:%s' % m for m in mv1),
                                   'value_agree': ok_val, 'moves_agree': ok_mv})
    # colour-flip symmetry of the solver
    L0, a0, _, _ = res[g['id']]
    L1, a1, _, _ = res[flg['id']]
    neg = {'W': 'L', 'L': 'W', 'D': 'D', 'X': 'X'}
    sym = 0
    for pos, la in zip(L0, a0):
        # flipped position string: swap case, flip ranks, swap side
        toks = pos.split()
        H = g['H']
        ft = []
        for t in toks[:-2]:
            c = t[0]
            c2 = c.lower() if c.isupper() else c.upper()
            ft.append(c2 + flip_sq(t[1:], H))
        ft = sorted(ft, key=lambda x: (0 if x[0] == 'K' else 1 if x[0] == 'k' else 2 if x[0] == 'P' else 3, x))
        fpos = ' '.join(['K' + [x for x in ft if x[0] == 'K'][0][1:], 'k' + [x for x in ft if x[0] == 'k'][0][1:]] +
                        [x for x in ft if x[0] in 'Pp'] + ['b' if toks[-2] == 'w' else 'w', '-'])
        # find it in L1 (order of pawns may differ: compare as sets)
        key = lambda p: (frozenset(p.split()[:-2]), p.split()[-2])
        idx = [i for i, p in enumerate(L1) if key(p) == key(fpos)]
        if idx:
            v0 = parse_line(la)[1]
            v1 = parse_line(a1[idx[0]])[1]
            sym += (neg[v0] == v1)
    entry['flip_symmetry_ok_roots'] = sym
    entry['roots_per_orientation'] = len(L0)
    rep.append(entry)
    print(g['id'], 'agree' if entry['all_agree'] else 'DISAGREE', 'flip-sym', sym, '/', len(L0), file=sys.stderr, flush=True)
json.dump({'total_roots': tot_roots, 'roots_fully_agreeing': tot_ok, 'groups': rep}, open(ofile, 'w'), indent=1)
print('roots', tot_roots, 'fully agreeing', tot_ok, file=sys.stderr)
