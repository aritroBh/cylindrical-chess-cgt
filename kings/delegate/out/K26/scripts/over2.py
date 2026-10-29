#!/usr/bin/env python3
"""K26 final: GENERALISED exact over/under search (supersedes the "exactly one non-losing freezer move" condition of search.py --type t1).

  over2.py --board cyl:8x6 --nw 2 --nb 2 [--nf 3] [--shard i/n] [--batch 100000] [--tag NAME]

Setting (the "under" orientation; "over" is its colour mirror, obtained with (nw, nb) swapped): White's king shuttles on an adjacent pair z (K1);
Black's king stands on one safe square b0 (K1, K2 against both z squares); <= nw White and <= nb Black pawns on F_Z ranks 2..H-1; 4 roots
(z0 or z1) x (White or Black to move).

Definition (exact under, "mutual"; every condition is a statement about the P model):
  (U1) at both White-to-move roots every non-shuttle White move loses at once (value L), and the shuttle move is legal and unique;
  (U2) at both Black-to-move roots Black has at least one legal move that does not lose at once ("freeze"), and EVERY such move m leads to a
       position q_m (no promotion, a legal position) with
         (U3) White to move at q_m: at least one legal move and every legal move loses at once (value L), and
         (U4) Black to move at q_m (same board, side flipped; legal): at least one legal move and every legal move loses at once (value W).
  Then q_m is a mutual zugzwang (a zero), and the group is {shuttle on z | freeze to 0}: the D-game under = {under | 0} mirrored.
Loose (no (U4)) is reported as 'under_loose'.  Old 'over_exact' of search.py = loose with exactly one freezing move.

Stage A: roots (z0, b0) with both sides to move, kpp --moves: keep if White leaks = 0 and Black has >= 1 non-losing move and every non-losing Black move has value L
         (a zero q has White-to-move value L).  Stage B: all 4 roots.  Stage C: q_m for every freezing move at the two Black-to-move roots (kpp).
Output: logs/over2_<tag>.json (counts, every exact and loose group listed with its freezing moves).
"""
import argparse, collections, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *

safe_nice()
ap = argparse.ArgumentParser()
ap.add_argument('--board', required=True)
ap.add_argument('--nw', type=int, required=True)
ap.add_argument('--nb', type=int, required=True)
ap.add_argument('--nf', type=int, default=3)
ap.add_argument('--shard', default='0/1')
ap.add_argument('--batch', type=int, default=100000)
ap.add_argument('--tag', default=None)
ap.add_argument('--no-u4', action='store_true', help='test mode: drop condition (U4); the survivors are then the LOOSE class (compare with search.py over_exact when exactly one freezing move)')
args = ap.parse_args()
kind, dims = args.board.split(':')
BW, BH = map(int, dims.split('x'))
geo = Geo(BH, args.nf)
SH_I, SH_N = map(int, args.shard.split('/'))
tag = args.tag or 'over2_%s_%s_%d%d' % (kind, dims, args.nw, args.nb)
if args.nf != 3:
    tag += '_nf%d' % args.nf
if SH_N > 1:
    tag += '_s%dof%d' % (SH_I, SH_N)
LOG = os.path.join(OUT, 'logs')
t0 = time.time()


def log(*a):
    print('[%7.1fs]' % (time.time() - t0), *a, file=sys.stderr, flush=True)


cfgs = geo.configs(args.nw, args.nb)
pairs = geo.pairs
pname = [(geo.name[a], geo.name[b]) for (a, b) in pairs]
log('board', args.board, 'limits', args.nw, args.nb, 'nf', args.nf, 'configs', len(cfgs))


def cand_iter():
    for ci, cfg in enumerate(cfgs):
        if ci * SH_N // len(cfgs) != SH_I:
            continue
        for (p, s) in geo.t1(cfg):
            yield (ci, p, s)


def batches(it, n):
    b = []
    for c in it:
        b.append(c)
        if len(b) >= n:
            yield b
            b = []
    if b:
        yield b


def lines_for(cands, roots):
    L = []
    for (ci, p, s) in cands:
        cfg = cfgs[ci]
        z = pairs[p]
        for (a, st) in roots:
            L.append(pos_str(geo, cfg, z[a], s, 'w' if st == 0 else 'b'))
    return L


def eval_roots(cands, res, roots):
    out = []
    k = len(roots)
    for i, (ci, p, s) in enumerate(cands):
        info = []
        bad = False
        for j, (a, st) in enumerate(roots):
            stm, val, mv = parse_line(res[i * k + j])
            if val == 'X':
                bad = True
                break
            if st == 0:
                nsh, shv, nn, leaks = classify_moves('w', mv, set(pname[p]))
                if nsh != 1:
                    bad = True
                    break
                info.append({'stm': 'w', 'val': val, 'wleaks': len(leaks)})
            else:
                nl = [(nm, v) for nm, v in mv if v != 'W']
                info.append({'stm': 'b', 'val': val, 'bcount': len(mv), 'nonlosing': nl})
        out.append(None if bad else info)
    return out


def apply_move(cfg, wk, bk, name):
    """Black move 'name' (as printed by kpp) from a root; returns (pawn strings, (wks, bks, ep)) or (None, 'promo')"""
    if '=' in name:
        return None, 'promo'
    wps = {geo.name[i] for i in cfg[0]}
    bps = {geo.name[i] for i in cfg[1]}
    wks, bks = geo.name[wk], geo.name[bk]
    frm, to = name[1:3], name[3:5]
    ep = '-'
    if name[0] == 'K':
        bks = to
        wps.discard(to)
    else:
        bps.discard(frm)
        if frm[0] != to[0]:
            wps.discard(to)
        bps.add(to)
        if int(frm[1]) - int(to[1]) == 2:
            adjw = [chr(ord(to[0]) + d) + to[1] for d in (-1, 1)]
            if any(x in wps for x in adjw):
                ep = frm[0] + str(int(frm[1]) - 1)
    sq = lambda s: (int(s[1:]), ord(s[0]))
    ps = ['P' + x for x in sorted(wps, key=sq)] + ['p' + x for x in sorted(bps, key=sq)]
    return ps, (wks, bks, ep)


ROOT_1 = [(0, 0), (0, 1)]
ROOT_4 = [(a, st) for a in (0, 1) for st in (0, 1)]
hist = collections.Counter()
survA = []
ncand = nbad = 0
for bi, b in enumerate(batches(cand_iter(), args.batch)):
    res, err = run_solver(lines_for(b, ROOT_1), args.board, 'kpp')
    ev = eval_roots(b, res, ROOT_1)
    for c, e in zip(b, ev):
        ncand += 1
        if e is None:
            nbad += 1
            continue
        w, bl = e
        nl = bl['nonlosing']
        key = (min(w['wleaks'], 3), min(len(nl), 3), all(v == 'L' for _, v in nl))
        hist[key] += 1
        if w['wleaks'] == 0 and nl and all(v == 'L' for _, v in nl):
            survA.append(c)
    log('stage A batch', bi, 'cands', ncand, 'survivors', len(survA))

# stage B
survB = []
for b in batches(iter(survA), 20000):
    res, err = run_solver(lines_for(b, ROOT_4), args.board, 'kpp')
    ev = eval_roots(b, res, ROOT_4)
    for c, e in zip(b, ev):
        if e is None:
            continue
        ok = True
        for x in e:
            if x['stm'] == 'w' and x['wleaks'] != 0:
                ok = False
            if x['stm'] == 'b' and not (x['nonlosing'] and all(v == 'L' for _, v in x['nonlosing'])):
                ok = False
        if ok:
            survB.append((c, e))
log('stage B survivors', len(survB))

# stage C (rounds: round r tests the r-th freezing move of each Black-to-move root of every candidate still alive; a failing candidate is dropped)
alive = {c: e for (c, e) in survB}
fail = collections.Counter()
maxn = 0
rnd = 0
while alive:
    q_lines, q_meta = [], []
    done = []
    for c, e in list(alive.items()):
        ci, p, s_ = c
        cfg = cfgs[ci]
        z = pairs[p]
        used = False
        dropped = False
        for a in (0, 1):
            bx = [x for x in e if x['stm'] == 'b'][a]
            if rnd >= len(bx['nonlosing']):
                continue
            used = True
            nm, v = bx['nonlosing'][rnd]
            ps, info = apply_move(cfg, z[a], s_, nm)
            if ps is None:
                fail['promotion'] += 1
                del alive[c]
                dropped = True
                break
            wks, bks, ep = info
            base = 'K%s k%s %s' % (wks, bks, ' '.join(ps))
            q_lines.append(base + ' w ' + ep)
            q_lines.append(base + ' b -')
            q_meta.append(c)
        if not used and not dropped:
            done.append(c)
    maxn = max(maxn, rnd)
    qres = []
    for b in batches(iter(q_lines), 40000):
        res, err = run_solver(b, args.board, 'kpp')
        qres.extend(res)
    for k, c in enumerate(q_meta):
        if c not in alive:
            continue
        stm1, val1, mv1 = parse_line(qres[2 * k])
        stm2, val2, mv2 = parse_line(qres[2 * k + 1])
        s_ok = val1 != 'X' and len(mv1) >= 1 and all(v == 'L' for _, v in mv1)
        f_ok = val2 != 'X' and len(mv2) >= 1 and all(v == 'W' for _, v in mv2)
        if not s_ok:
            fail['U3'] += 1
            del alive[c]
        elif not f_ok and not args.no_u4:
            fail['U4'] += 1
            del alive[c]
    log('stage C round', rnd, 'q positions', len(q_lines), 'alive', len(alive), 'failures so far', dict(fail))
    for c in done:
        pass
    # candidates with no freezing move left to test at this round are complete (they passed all earlier rounds)
    finished = [c for c in alive if all(rnd + 1 >= len([x for x in alive[c] if x['stm'] == 'b'][a]['nonlosing']) for a in (0, 1))]
    for c in finished:
        done.append(c)
    # keep finished ones aside
    for c in set(done):
        if c in alive:
            mutual_list = globals().setdefault('MUTUAL', [])
            mutual_list.append((c, alive.pop(c)))
    rnd += 1
MUTUAL = globals().get('MUTUAL', [])
classes = collections.Counter()
recs = []
for (c, e) in MUTUAL:
    ci, p, s_ = c
    cfg = cfgs[ci]
    classes['under_mutual' if not args.no_u4 else 'under_loose'] += 1
    nfreeze = max(len([x for x in e if x['stm'] == 'b'][a]['nonlosing']) for a in (0, 1))
    if nfreeze >= 2:
        classes['with_2plus_freezing_moves'] += 1
    else:
        classes['with_exactly_1_freezing_move_at_every_root'] += 1
    recs.append({'W': [geo.name[x] for x in pairs[p]], 'b0': geo.name[s_], 'wp': [geo.name[x] for x in cfg[0]], 'bp': [geo.name[x] for x in cfg[1]],
                 'passW': cfg[5], 'passB': cfg[6], 'nonlosing_per_root': [x.get('nonlosing') for x in e if x['stm'] == 'b'], 'root_values': [x['val'] for x in e]})
classes['stageB_survivors_dropped_by_stageC_first_failure:' + 'U3'] = fail['U3']
classes['stageB_survivors_dropped_by_stageC_first_failure:' + 'U4'] = fail['U4']
classes['stageB_survivors_dropped_by_stageC_first_failure:promotion'] = fail['promotion']
out = {'board': args.board, 'limits': [args.nw, args.nb], 'nf': args.nf, 'shard': args.shard, 'configs': len(cfgs), 'candidates': ncand, 'illegal': nbad,
       'stageA_hist_(wleaks<=3, n_nonlosing<=3, all_nonlosing_L)': {str(k): v for k, v in sorted(hist.items())},
       'stageA_survivors': len(survA), 'stageB_survivors': len(survB), 'classes': dict(classes), 'groups': recs, 'seconds': round(time.time() - t0, 1)}
json.dump(out, open(os.path.join(LOG, tag + '.json'), 'w'), indent=1)
log('DONE', json.dumps({k: out[k] for k in ('candidates', 'stageA_survivors', 'stageB_survivors', 'classes')}))
