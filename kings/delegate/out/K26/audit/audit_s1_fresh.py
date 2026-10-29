#!/usr/bin/env python3
"""(attempt 5 copy: fresh build, output in logs/f/audit)  K26 audit of the exhaustive two-shuttle search with a second enumerator (enum2.py) and a second solver (ref3m).

  audit_s1.py --board flat:7x6 --nw 2 --nb 2 [--shard i/n] [--T 2]

For every placement of enum2 (independent of k26lib.Geo):
  stage 1: the two roots (z0, w0), White and Black to move, are solved with kpp (--pmodel --moves) AND with ref3m (--moves);
           both full move lists are compared (value of the root and multiset of (move, value), promotions normalised);
           the leak count of each solver is computed (non-shuttle legal moves of the mover that do not lose at once for the
           mover).
  stage 2: every placement with min(leaks_kpp, leaks_ref3m) <= T at stage 1 is solved at all 8 roots with both solvers and
           compared the same way; the histogram of the 8-root totals is reported for each solver, and the exact duds
           (total 0 at all 8 roots) are listed.
Output: logs/audit_<tag>.json  (counts, mismatches, the exact duds and the placements with total 1).
"""
import argparse, collections, itertools, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import enum2
from k26lib import run_solver, safe_nice, OUT

safe_nice()
ap = argparse.ArgumentParser()
ap.add_argument('--board', required=True)
ap.add_argument('--nw', type=int, required=True)
ap.add_argument('--nb', type=int, required=True)
ap.add_argument('--shard', default='0/1')
ap.add_argument('--T', type=int, default=2)
ap.add_argument('--batch', type=int, default=50000)
args = ap.parse_args()
kind, dims = args.board.split(':')
W, H = map(int, dims.split('x'))
si, sn = map(int, args.shard.split('/'))
tag = 'audit_%s_%s_%d%d' % (kind, dims, args.nw, args.nb) + ('_s%dof%d' % (si, sn) if sn > 1 else '')
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


def norm_ref(moves):
    return sorted(moves)


def leaks(stm, moves, sq1, sq2):
    lose = 'L' if stm == 'w' else 'W'
    n = 0
    sh = 0
    for nm, v in moves:
        if nm[0] == 'K' and len(nm) == 5 and {nm[1:3], nm[3:5]} == {sq1, sq2}:
            sh += 1
            continue
        if v != lose:
            n += 1
    return n, sh


def batches(it, n):
    b = []
    for c in it:
        b.append(c)
        if len(b) >= n:
            yield b
            b = []
    if b:
        yield b


def cand_iter():
    ci = -1
    for wp, bp in enum2.pawn_configs(H, args.nw, args.nb):
        ci += 1
        if ci % sn != si:
            continue
        ps = enum2.pawn_string(wp, bp)
        for z, w in enum2.placements_of_config(H, wp, bp):
            yield (wp, bp, z, w, ps)


def line(c, a, b, s):
    wp, bp, z, w, ps = c
    return ' '.join(['K' + enum2.name(z[a]), 'k' + enum2.name(w[b])] + ([ps] if ps else []) + ['w' if s == 0 else 'b', '-'])


ROOT1 = [(0, 0, 0), (0, 0, 1)]
ROOT8 = [(a, b, s) for a in (0, 1) for b in (0, 1) for s in (0, 1)]
mism = collections.Counter()
mism_ex = []


def evaluate(cands, roots):
    """returns per candidate: (leaks_kpp, leaks_ref, ok) with totals over the roots; compares full lists"""
    L = [line(c, a, b, s) for c in cands for (a, b, s) in roots]
    r1, _ = run_solver(L, args.board, 'kpp', moves=True)
    r2, _ = run_solver(L, args.board, 'ref3m', moves=True)
    out = []
    k = len(roots)
    for i, c in enumerate(cands):
        tk = tr = 0
        ok = True
        info = []
        for j, (a, b, s) in enumerate(roots):
            x, y = r1[i * k + j], r2[i * k + j]
            v1, m1 = parse_kpp(x)
            v2, m2 = parse_ref(y)
            mism['roots'] += 1
            if v1 != v2:
                mism['value'] += 1
                ok = False
                if len(mism_ex) < 10:
                    mism_ex.append((L[i * k + j], x, y))
            elif norm(m1) != norm_ref(m2):
                mism['moves'] += 1
                ok = False
                if len(mism_ex) < 10:
                    mism_ex.append((L[i * k + j], x, y))
            if v1 == 'X' or v2 == 'X':
                mism['illegal_root'] += 1
            sq = (enum2.name(c[2][0]), enum2.name(c[2][1])) if s == 0 else (enum2.name(c[3][0]), enum2.name(c[3][1]))
            stm = 'w' if s == 0 else 'b'
            n1, sh1 = leaks(stm, norm(m1), *sq)     # promotions: one entry per (from, to), not per piece
            n2, sh2 = leaks(stm, norm_ref(m2), *sq)
            if sh1 != 1 or sh2 != 1:
                mism['shuttle_not_exactly_once'] += 1
            tk += n1
            tr += n2
            info.append((v1, n1))
        out.append((tk, tr, ok, info))
    return out


cand_n = 0
h1k = collections.Counter()
h1r = collections.Counter()
disagree1 = 0
surv = []
for bi, b in enumerate(batches(cand_iter(), args.batch)):
    ev = evaluate(b, ROOT1)
    for c, (tk, tr, ok, info) in zip(b, ev):
        cand_n += 1
        h1k[tk] += 1
        h1r[tr] += 1
        if tk != tr:
            disagree1 += 1
        if min(tk, tr) <= args.T:
            surv.append(c)
    log('stage1 batch', bi, 'cands', cand_n, 'survivors', len(surv), 'mismatch', dict(mism))
h2k = collections.Counter()
h2r = collections.Counter()
disagree2 = 0
duds = []
ones = []
for bi, b in enumerate(batches(iter(surv), 10000)):
    ev = evaluate(b, ROOT8)
    for c, (tk, tr, ok, info) in zip(b, ev):
        h2k[tk] += 1
        h2r[tr] += 1
        if tk != tr:
            disagree2 += 1
        rec = {'wp': [enum2.name(s) for s in c[0]], 'bp': [enum2.name(s) for s in c[1]],
               'W': [enum2.name(s) for s in c[2]], 'B': [enum2.name(s) for s in c[3]], 'total_kpp': tk, 'total_ref3m': tr,
               'root_values': [i[0] for i in info]}
        if min(tk, tr) == 0:
            duds.append(rec)
        elif min(tk, tr) == 1:
            ones.append(rec)
    log('stage2 batch', bi, 'size', len(b))
out = {'board': args.board, 'limits': [args.nw, args.nb], 'shard': args.shard, 'placements': cand_n,
       'stage1_hist_kpp': dict(sorted(h1k.items())[:6]), 'stage1_hist_ref3m': dict(sorted(h1r.items())[:6]),
       'stage1_leak_count_disagreements_kpp_vs_ref3m': disagree1,
       'stage2_candidates': len(surv), 'stage2_hist_kpp': dict(sorted(h2k.items())), 'stage2_hist_ref3m': dict(sorted(h2r.items())),
       'stage2_leak_count_disagreements': disagree2, 'full_list_mismatches': dict(mism), 'mismatch_examples': mism_ex,
       'exact_duds': duds, 'total_1': ones, 'seconds': round(time.time() - t0, 1)}
json.dump(out, open(os.path.join(LOG, tag + '.json'), 'w'), indent=1)
log('DONE', json.dumps({k: out[k] for k in ('placements', 'stage1_leak_count_disagreements_kpp_vs_ref3m', 'stage2_hist_kpp', 'stage2_hist_ref3m', 'full_list_mismatches')}))
