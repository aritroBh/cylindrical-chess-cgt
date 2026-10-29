#!/usr/bin/env python3
"""(attempt 5 copy: fresh build, output in logs/f/audit)  K26 audit of the one-shuttle search (classes on / over-pre) with the second enumerator (enum2.py) and the second solver (ref3m).

  audit_t1.py --board flat:7x6 --nw 2 --nb 2 [--shard i/n]

Placements: a White shuttle pair z (two adjacent squares, K1) and a Black king on a single square b (K1; K2 against both z squares),
pawns as in enum2.  4 roots (z0 or z1) x (White or Black to move).  Both solvers (kpp and ref3m) are run on every root and the full
move lists compared.  Classes, from the move lists (promotions once per (from, to)):
  Wleaks(root) = non-shuttle White moves (White to move) that do not lose at once (value != L)
  Bnon(root)   = Black moves (Black to move) that do not lose at once (value != W), Bcount = number of Black moves
  on_strong : at both Black-to-move roots Bnon = 0 and Bcount >= 1, and at both White-to-move roots Wleaks = 0
  on_weak   : only the Black condition
  over_pre  : Wleaks = 0 at both White roots and Bnon = 1 at both Black roots
Stage 1 solves roots (z0, b) with both sides to move and keeps a placement when (Bnon=0, Bcount>=1) or (Bnon=1 and Wleaks=0) there;
stage 2 solves all 4 roots of the survivors.  (The exact over test of stage 3 is not repeated here.)
"""
import argparse, collections, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import enum2
from k26lib import run_solver, safe_nice, OUT

safe_nice()
ap = argparse.ArgumentParser()
ap.add_argument('--board', required=True)
ap.add_argument('--nw', type=int, required=True)
ap.add_argument('--nb', type=int, required=True)
ap.add_argument('--shard', default='0/1')
ap.add_argument('--batch', type=int, default=50000)
args = ap.parse_args()
kind, dims = args.board.split(':')
W, H = map(int, dims.split('x'))
si, sn = map(int, args.shard.split('/'))
tag = 'audit1_%s_%s_%d%d' % (kind, dims, args.nw, args.nb) + ('_s%dof%d' % (si, sn) if sn > 1 else '')
t0 = time.time()
LOG = os.path.join(OUT, 'logs', 'f', 'audit')


def log(*a):
    print('[%7.1fs]' % (time.time() - t0), *a, file=sys.stderr, flush=True)


def parse_kpp(line):
    parts = line.split(' | ')
    val = parts[1].split()[0]
    mv = []
    if len(parts) > 2:
        for tok in parts[2].split():
            nm, v = tok.rsplit(':', 1)
            mv.append((nm, v))
    return val, mv


def parse_ref(line):
    parts = line.split(' | ')
    toks = parts[1].split()
    mv = []
    for t in toks[1:]:
        nm, v = t.rsplit(':', 1)
        mv.append((nm, v))
    return toks[0], mv


def norm(moves):
    seen = set()
    out = []
    for nm, v in moves:
        if '=' in nm:
            k = ('promo', nm[1:5], v)
            if k in seen:
                continue
            seen.add(k)
            out.append(('promo', v))
        else:
            out.append((nm, v))
    return sorted(out)


def batches(it, n):
    b = []
    for c in it:
        b.append(c)
        if len(b) >= n:
            yield b
            b = []
    if b:
        yield b


def single_squares(wp, bp, z):
    sqs = [(f, r) for f in (1, 2, 3) for r in range(1, H + 1)]
    occ = set(wp) | set(bp)
    att_by_white = {(f + d, r + 1) for (f, r) in wp for d in (-1, 1)}
    return [s for s in sqs if s not in occ and s not in att_by_white and all(enum2.cheb(s, q) >= 2 for q in z)]


def cand_iter():
    ci = -1
    for wp, bp in enum2.pawn_configs(H, args.nw, args.nb):
        ci += 1
        if ci % sn != si:
            continue
        ps = enum2.pawn_string(wp, bp)
        sqs = [(f, r) for f in (1, 2, 3) for r in range(1, H + 1)]
        adj = [(a, b) for a, b in __import__('itertools').combinations(sqs, 2) if enum2.cheb(a, b) == 1]
        occ = set(wp) | set(bp)
        att_by_black = {(f + d, r - 1) for (f, r) in bp for d in (-1, 1)}
        wok = {s for s in sqs if s not in occ and s not in att_by_black}
        for z in adj:
            if z[0] in wok and z[1] in wok:
                for b in single_squares(wp, bp, z):
                    yield (wp, bp, z, b, ps)


def line(c, a, s):
    wp, bp, z, b, ps = c
    return ' '.join(['K' + enum2.name(z[a]), 'k' + enum2.name(b)] + ([ps] if ps else []) + ['w' if s == 0 else 'b', '-'])


mism = collections.Counter()
mism_ex = []


def evaluate(cands, roots):
    L = [line(c, a, s) for c in cands for (a, s) in roots]
    r1, _ = run_solver(L, args.board, 'kpp', moves=True)
    r2, _ = run_solver(L, args.board, 'ref3m', moves=True)
    k = len(roots)
    out = []
    for i, c in enumerate(cands):
        info = []
        for j, (a, s) in enumerate(roots):
            x, y = r1[i * k + j], r2[i * k + j]
            v1, m1 = parse_kpp(x)
            v2, m2 = parse_ref(y)
            mism['roots'] += 1
            if v1 != v2 or norm(m1) != sorted(m2):
                mism['value_or_moves'] += 1
                if len(mism_ex) < 10:
                    mism_ex.append((L[i * k + j], x, y))
            if v1 == 'X':
                mism['illegal_root'] += 1
            mv = norm(m1)
            if s == 0:
                sq = {enum2.name(c[2][0]), enum2.name(c[2][1])}
                sh = [1 for nm, v in m1 if nm[0] == 'K' and len(nm) == 5 and {nm[1:3], nm[3:5]} == sq]
                wl = sum(1 for nm, v in mv if not (nm[0] == 'K' and len(nm) == 5 and {nm[1:3], nm[3:5]} == sq) and v != 'L')
                if len(sh) != 1:
                    mism['shuttle_not_exactly_once'] += 1
                info.append(('w', v1, wl))
            else:
                info.append(('b', v1, sum(1 for nm, v in mv if v != 'W'), len(mv)))
        out.append(info)
    return out


ROOT1 = [(0, 0), (0, 1)]
ROOT4 = [(a, s) for a in (0, 1) for s in (0, 1)]
n = 0
surv = []
for bi, b in enumerate(batches(cand_iter(), args.batch)):
    ev = evaluate(b, ROOT1)
    for c, info in zip(b, ev):
        n += 1
        wl = info[0][2]
        bn, bc = info[1][2], info[1][3]
        if (bn == 0 and bc >= 1) or (bn == 1 and wl == 0):
            surv.append(c)
    log('stage1 batch', bi, 'placements', n, 'survivors', len(surv), dict(mism))
cl = collections.Counter()
ex = {'on_strong': []}
for bi, b in enumerate(batches(iter(surv), 20000)):
    ev = evaluate(b, ROOT4)
    for c, info in zip(b, ev):
        ws = [x for x in info if x[0] == 'w']
        bs = [x for x in info if x[0] == 'b']
        wl = sum(x[2] for x in ws)
        bn = sum(x[2] for x in bs)
        allbc = all(x[3] >= 1 for x in bs)
        on_weak = bn == 0 and allbc
        passer = any(enum2.textbook_passed(c[0], c[1], True)) or any(enum2.textbook_passed(c[1], c[0], False))
        if on_weak:
            cl['on_weak'] += 1
            if wl == 0:
                cl['on_strong'] += 1
                if not passer:
                    cl['on_strong_no_passer'] += 1
                ex['on_strong'].append({'W': [enum2.name(s) for s in c[2]], 'b': enum2.name(c[3]), 'wp': [enum2.name(s) for s in c[0]],
                                        'bp': [enum2.name(s) for s in c[1]], 'passer': passer})
        if wl == 0 and all(x[2] == 1 for x in bs):
            cl['over_pre'] += 1
            if not passer:
                cl['over_pre_no_passer'] += 1
out = {'board': args.board, 'limits': [args.nw, args.nb], 'shard': args.shard, 'placements': n, 'stage2': len(surv),
       'classes': dict(cl), 'mismatches': dict(mism), 'mismatch_examples': mism_ex, 'on_strong': ex['on_strong'],
       'seconds': round(time.time() - t0, 1)}
json.dump(out, open(os.path.join(LOG, tag + '.json'), 'w'), indent=1)
log('DONE', json.dumps({k: out[k] for k in ('placements', 'stage2', 'classes', 'mismatches')}))
