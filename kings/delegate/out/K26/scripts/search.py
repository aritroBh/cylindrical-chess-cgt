#!/usr/bin/env python3
"""K26 exhaustive search for king groups on files a-c (no move-count cut-off).

  search.py --board flat:7x6 --nw 2 --nb 2 --type t2   [--tmax 6] [--batch 100000] [--tag NAME]
  search.py --board flat:7x6 --nw 2 --nb 2 --type t1   (White shuttles, Black king on a single square)

type t2: both kings shuttle on an adjacent pair (K1, K2 hold at all four combined king states).
         stage 1 = roots (z0,w0) with either side to move; stage 2 = all 8 roots for every candidate whose stage-1 leak
         count is <= T; T grows (0,1,2,...) until the minimum total leak count found is <= T, so the minimum over
         ALL candidates is exact.  Exact dud = total leaks 0 at all 8 roots.
type t1: White shuttles (pair z), Black king on a single safe square b0 (K1, K2).  4 roots.  Classes:
         on_strong (exact on): White zero leaks, every Black move loses at once (and Black has a move), at all 4 roots;
         on_weak: only the Black condition (Proposition 3.2: r >= r(G + on_D));
         over: White (the shuttler) zero leaks at the roots, Black has exactly one non-losing move m at every Black-to-move
               root, and after m (stage 3) the shuttler has >= 1 move and all of them lose at once ("over_exact");
               over_mutual: additionally the side to move flipped is also in zugzwang (all its moves lose at once).
         Black-shuttler versions are the colour mirror: they are obtained with (nw, nb) swapped.
Everything is streamed through pipes to kpp (P model); output only in <K26>/logs/.
"""
import argparse, collections, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *

safe_nice()
ap = argparse.ArgumentParser()
ap.add_argument('--board', required=True)
ap.add_argument('--nw', type=int, required=True)
ap.add_argument('--nb', type=int, required=True)
ap.add_argument('--type', required=True, choices=['t2', 't1'])
ap.add_argument('--tmax', type=int, default=6)
ap.add_argument('--batch', type=int, default=100000)
ap.add_argument('--tag', default=None)
ap.add_argument('--solver', default='kpp')
ap.add_argument('--shard', default='0/1')
ap.add_argument('--nf', type=int, default=3, help='number of files of F_Z (3 = a-c; 4 = a-d for the wider over search)')
args = ap.parse_args()
kind, dims = args.board.split(':')
BW, BH = map(int, dims.split('x'))
geo = Geo(BH, args.nf)
SH_I, SH_N = map(int, args.shard.split('/'))
tag = args.tag or '%s_%s_%d%d_%s' % (kind, dims, args.nw, args.nb, args.type)
if args.nf != 3:
    tag += '_nf%d' % args.nf
if SH_N > 1:
    tag += '_s%dof%d' % (SH_I, SH_N)
LOG = os.path.join(OUT, 'logs')
os.makedirs(LOG, exist_ok=True)
t0 = time.time()


def log(*a):
    print('[%7.1fs]' % (time.time() - t0), *a, file=sys.stderr, flush=True)


cfgs = geo.configs(args.nw, args.nb)
log('board', args.board, 'limits', args.nw, args.nb, 'configs', len(cfgs), 'type', args.type)
pairs = geo.pairs
pname = [(geo.name[a], geo.name[b]) for (a, b) in pairs]


def cand_iter():
    gen = geo.t2 if args.type == 't2' else geo.t1
    for ci, cfg in enumerate(cfgs):
        if ci * SH_N // len(cfgs) != SH_I:
            continue
        for (x, y) in gen(cfg):
            yield (ci, x, y)


def batches(it, n):
    b = []
    for c in it:
        b.append(c)
        if len(b) >= n:
            yield b
            b = []
    if b:
        yield b


def cfg_counts(ci):
    c = cfgs[ci]
    return (len(c[0]), len(c[1]))


# ---------------------------------------------------------------------------------------------------------------
if args.type == 't2':
    def lines_for(cands, roots):
        L = []
        for (ci, p, q) in cands:
            cfg = cfgs[ci]
            z = pairs[p]
            w = pairs[q]
            for (a, b, s) in roots:
                L.append(pos_str(geo, cfg, z[a], w[b], 'w' if s == 0 else 'b'))
        return L

    ROOT1 = [(0, 0, 0), (0, 0, 1)]
    ROOT8 = [(a, b, s) for a in (0, 1) for b in (0, 1) for s in (0, 1)]

    def eval_roots(cands, res, roots):
        """returns list per candidate of (total_leaks, per-root info) or None if illegal"""
        out = []
        k = len(roots)
        for i, (ci, p, q) in enumerate(cands):
            tot = 0
            info = []
            bad = False
            for j, (a, b, s) in enumerate(roots):
                stm, val, mv = parse_line(res[i * k + j])
                if val == 'X':
                    bad = True
                    break
                sh = set(pname[p]) if s == 0 else set(pname[q])
                nsh, shv, nn, leaks = classify_moves(stm, mv, sh)
                if nsh != 1:
                    bad = True
                    break
                tot += len(leaks)
                info.append((val, len(leaks), shv[0], leaks))
            out.append(None if bad else (tot, info))
        return out

    # stage 1
    hist1 = collections.Counter()
    hist1_by = collections.defaultdict(collections.Counter)
    byleak = collections.defaultdict(list)
    ncand = 0
    nbad = 0
    for bi, b in enumerate(batches(cand_iter(), args.batch)):
        L = lines_for(b, ROOT1)
        res, err = run_solver(L, args.board, args.solver)
        ev = eval_roots(b, res, ROOT1)
        for c, e in zip(b, ev):
            ncand += 1
            if e is None:
                nbad += 1
                continue
            t = e[0]
            hist1[t] += 1
            hist1_by[cfg_counts(c[0])][t] += 1
            if t <= args.tmax:
                byleak[t].append(c)
        log('stage1 batch', bi, 'cands so far', ncand, 'illegal', nbad, 'solver:', err.strip().split('\n')[-1][:100])
    log('stage1 histogram', dict(sorted(hist1.items())[:12]))

    # stage 2, adaptive T
    results = {}   # candidate -> (total, info)
    done_levels = -1
    best = None
    T = 0
    while True:
        todo = byleak.get(T, [])
        for bi, b in enumerate(batches(iter(todo), 15000)):
            L = lines_for(b, ROOT8)
            res, err = run_solver(L, args.board, args.solver)
            ev = eval_roots(b, res, ROOT8)
            for c, e in zip(b, ev):
                if e is None:
                    continue
                results[c] = e
            log('stage2 T', T, 'batch', bi, 'size', len(b))
        tots = [e[0] for e in results.values()]
        best = min(tots) if tots else None
        log('after T =', T, 'candidates evaluated', len(results), 'min total leaks', best)
        if (best is not None and best <= T and T >= 2) or T >= args.tmax:   # T >= 2: counts of total leaks 0,1,2 are complete
            break
        T += 1
    exact_min_known = best is not None and best <= T

    hist2 = collections.Counter(e[0] for e in results.values())
    # write all candidates with total <= min(best+1, 3) and every exact dud
    outf = open(os.path.join(LOG, tag + '_groups.jsonl'), 'w')
    summ = collections.Counter()
    summ_nopass = collections.Counter()
    by_pawns = collections.defaultdict(collections.Counter)
    for c, (tot, info) in results.items():
        ci, p, q = c
        cfg = cfgs[ci]
        if tot <= max(best + 1, 2) or tot == 0:
            rec = {'W': [geo.name[x] for x in pairs[p]], 'B': [geo.name[x] for x in pairs[q]],
                   'wp': [geo.name[x] for x in cfg[0]], 'bp': [geo.name[x] for x in cfg[1]],
                   'passW': cfg[5], 'passB': cfg[6], 'total': tot,
                   'roots': [(i[0], i[1], i[2]) for i in info],
                   'leaks': [i[3] for i in info if i[3]][:3]}
            outf.write(json.dumps(rec) + '\n')
        if tot == 0:
            summ['dud'] += 1
            by_pawns[cfg_counts(ci)]['dud'] += 1
            if not (cfg[5] or cfg[6]):
                summ_nopass['dud'] += 1
            if not all(i[0] == 'D' for i in info):
                summ['dud_not_all_D'] += 1
    outf.close()
    out = {'board': args.board, 'type': 't2', 'limits': [args.nw, args.nb], 'configs': len(cfgs), 'candidates': ncand,
           'illegal_candidates': nbad, 'stage1_hist_total_leaks_at_roots_z0w0': dict(sorted(hist1.items())),
           'stage1_hist_by_pawns': {'%d+%d' % k: dict(sorted(v.items())) for k, v in hist1_by.items()},
           'stage2_hist_total_leaks_8roots': dict(sorted(hist2.items())), 'stage2_T_reached': T,
           'min_total_leaks_8roots': best, 'min_is_exact_over_all_candidates': exact_min_known,
           'exact_dud': summ['dud'], 'exact_dud_no_passer_filter_applied_to_value': summ_nopass['dud'],
           'exact_dud_not_all_root_values_D': summ['dud_not_all_D'],
           'dud_by_pawns': {'%d+%d' % k: dict(v) for k, v in by_pawns.items()},
           'seconds': round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(LOG, tag + '_summary.json'), 'w'), indent=1)
    log('DONE', json.dumps({k: out[k] for k in ('candidates', 'min_total_leaks_8roots', 'exact_dud', 'exact_dud_no_passer_filter_applied_to_value')}))

# ---------------------------------------------------------------------------------------------------------------
else:
    def lines_for(cands, roots):
        L = []
        for (ci, p, s) in cands:
            cfg = cfgs[ci]
            z = pairs[p]
            for (a, st) in roots:
                L.append(pos_str(geo, cfg, z[a], s, 'w' if st == 0 else 'b'))
        return L

    ROOT_1 = [(0, 0), (0, 1)]
    ROOT_4 = [(a, st) for a in (0, 1) for st in (0, 1)]

    def eval_roots(cands, res, roots):
        """per candidate: None if illegal, else list per root of dict"""
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
                    info.append({'stm': 'w', 'val': val, 'wleaks': len(leaks), 'shv': shv[0], 'leaks': leaks, 'n': len(mv)})
                else:
                    nl = [(nm, v) for nm, v in mv if v != 'W']
                    info.append({'stm': 'b', 'val': val, 'bcount': len(mv), 'bleaks': len(nl), 'nonlosing': nl})
            out.append(None if bad else info)
        return out

    def stage1_keep(info, T):
        w, b = info
        wl, bl, bc = w['wleaks'], b['bleaks'], b['bcount']
        return (bl == 0 and bc >= 1) or (bl == 1 and wl == 0) or (wl + bl <= T)

    hist1 = collections.Counter()
    survivors = []
    ncand = 0
    nbad = 0
    for bi, b in enumerate(batches(cand_iter(), args.batch)):
        L = lines_for(b, ROOT_1)
        res, err = run_solver(L, args.board, args.solver)
        ev = eval_roots(b, res, ROOT_1)
        for c, e in zip(b, ev):
            ncand += 1
            if e is None:
                nbad += 1
                continue
            wl, bl, bc = e[0]['wleaks'], e[1]['bleaks'], e[1]['bcount']
            hist1[(min(wl, 9), min(bl, 9), min(bc, 9))] += 1
            if stage1_keep(e, args.tmax // 2):
                survivors.append(c)
        log('stage1 batch', bi, 'cands so far', ncand, 'survivors', len(survivors), 'solver:', err.strip().split('\n')[-1][:100])

    # stage 2 on all 4 roots
    classes = collections.Counter()
    classes_nopass = collections.Counter()
    by_pawns = collections.defaultdict(collections.Counter)
    min_on_miss = None
    onmiss_examples = []
    over_pre = []
    outf = open(os.path.join(LOG, tag + '_groups.jsonl'), 'w')

    def rec_of(c, infos, extra=None):
        ci, p, s = c
        cfg = cfgs[ci]
        r = {'W': [geo.name[x] for x in pairs[p]], 'b0': geo.name[s],
             'wp': [geo.name[x] for x in cfg[0]], 'bp': [geo.name[x] for x in cfg[1]],
             'passW': cfg[5], 'passB': cfg[6],
             'roots': [{k: v for k, v in i.items() if k in ('stm', 'val', 'wleaks', 'bcount', 'bleaks', 'nonlosing')} for i in infos]}
        if extra:
            r.update(extra)
        return r

    for bi, b in enumerate(batches(iter(survivors), 20000)):
        L = lines_for(b, ROOT_4)
        res, err = run_solver(L, args.board, args.solver)
        ev = eval_roots(b, res, ROOT_4)
        for c, e in zip(b, ev):
            if e is None:
                continue
            ws = [x for x in e if x['stm'] == 'w']
            bs = [x for x in e if x['stm'] == 'b']
            wl = sum(x['wleaks'] for x in ws)
            bl = sum(x['bleaks'] for x in bs)
            allbc = all(x['bcount'] >= 1 for x in bs)
            nb0 = sum(1 for x in bs if x['bcount'] == 0)
            miss = wl + bl + nb0
            if min_on_miss is None or miss < min_on_miss:
                min_on_miss = miss
                onmiss_examples = []
            if miss == min_on_miss and len(onmiss_examples) < 5:
                onmiss_examples.append(rec_of(c, e, {'miss': miss}))
            cfg = cfgs[c[0]]
            np_ = not (cfg[5] or cfg[6])
            cl = []
            on_weak = bl == 0 and allbc
            on_strong = on_weak and wl == 0
            over_p = wl == 0 and all(x['bleaks'] == 1 for x in bs)
            if on_weak:
                cl.append('on_weak')
            if on_strong:
                cl.append('on_strong')
            if over_p:
                cl.append('over_pre')
                over_pre.append((c, e))
            for k_ in cl:
                classes[k_] += 1
                by_pawns[cfg_counts(c[0])][k_] += 1
                if np_:
                    classes_nopass[k_] += 1
            if on_strong:
                outf.write(json.dumps(rec_of(c, e, {'class': 'on_strong'})) + '\n')
        log('stage2 batch', bi, 'size', len(b), 'classes so far', dict(classes))

    # stage 3: over candidates
    def apply_move(cfg, wk, bk, mover, name):
        """black (mover 'b') or white move 'name' (from kpp) applied to a root; returns (position string, kind)"""
        wps = {geo.name[i] for i in cfg[0]}
        bps = {geo.name[i] for i in cfg[1]}
        wks, bks = geo.name[wk], geo.name[bk]
        if '=' in name:
            return None, 'promo'
        frm, to = name[1:3], name[3:5]
        ep = '-'
        if name[0] == 'K':
            if mover == 'b':
                bks = to
                wps.discard(to)
            else:
                wks = to
                bps.discard(to)
        else:
            if mover == 'b':
                bps.discard(frm)
                if frm[0] != to[0]:
                    wps.discard(to)
                bps.add(to)
                if int(frm[1]) - int(to[1]) == 2:
                    land = to
                    adjw = [chr(ord(land[0]) + d) + land[1] for d in (-1, 1)]
                    if any(x in wps for x in adjw):
                        ep = frm[0] + str(int(frm[1]) - 1)
            else:
                wps.discard(frm)
                if frm[0] != to[0]:
                    bps.discard(to)
                wps.add(to)
                if int(to[1]) - int(frm[1]) == 2:
                    adjb = [chr(ord(to[0]) + d) + to[1] for d in (-1, 1)]
                    if any(x in bps for x in adjb):
                        ep = frm[0] + str(int(frm[1]) + 1)
        sq = lambda s: (int(s[1:]), ord(s[0]))
        ps = ['P' + x for x in sorted(wps, key=sq)] + ['p' + x for x in sorted(bps, key=sq)]
        return ps, (wks, bks, ep)

    exact_over = []
    nover_pre = len(over_pre)
    over_fail = collections.Counter()
    q_lines = []
    q_meta = []
    for (c, e) in over_pre:
        ci, p, s = c
        cfg = cfgs[ci]
        z = pairs[p]
        for a in (0, 1):
            bx = [x for x in e if x['stm'] == 'b'][a]
            (nm, v) = bx['nonlosing'][0]
            ps, info = apply_move(cfg, z[a], s, 'b', nm)
            if ps is None:
                q_meta.append((c, a, nm, None, v))
                continue
            wks, bks, ep = info
            base = 'K%s k%s %s' % (wks, bks, ' '.join(ps))
            q_lines.append(base + ' w ' + ep)       # shuttler (White) to move
            q_lines.append(base + ' b -')           # flipped: the freezer (Black) to move
            q_meta.append((c, a, nm, True, v))
    if q_lines:
        pass
    qres = []
    for bi, b in enumerate(batches(iter(q_lines), 40000)):
        res, err = run_solver(b, args.board, args.solver)
        qres.extend(res)
    qi = 0
    verdict = {}
    apply_mismatch = 0
    for (c, a, nm, ok, vexp) in q_meta:
        d = verdict.setdefault(c, {'exact': True, 'mutual': True, 'notes': []})
        if ok is None:
            d['exact'] = d['mutual'] = False
            d['notes'].append('promo:' + nm)
            continue
        stm1, val1, mv1 = parse_line(qres[qi])
        stm2, val2, mv2 = parse_line(qres[qi + 1])
        qi += 2
        if val1 != vexp:          # the position built by apply_move must have the value the root move was listed with
            apply_mismatch += 1
        s_ok = val1 != 'X' and len(mv1) >= 1 and all(v == 'L' for _, v in mv1)
        f_ok = val2 != 'X' and len(mv2) >= 1 and all(v == 'W' for _, v in mv2)
        if not s_ok:
            d['exact'] = d['mutual'] = False
            d['notes'].append('S-move fails at q after %s: %s %s' % (nm, val1, mv1[:4]))
        elif not f_ok:
            d['mutual'] = False
            d['notes'].append('flip fails at q after %s: %s %s' % (nm, val2, mv2[:4]))
    for (c, e) in over_pre:
        v = verdict.get(c)
        cfg = cfgs[c[0]]
        np_ = not (cfg[5] or cfg[6])
        if v and v['exact']:
            classes['over_exact'] += 1
            by_pawns[cfg_counts(c[0])]['over_exact'] += 1
            if np_:
                classes_nopass['over_exact'] += 1
            if v['mutual']:
                classes['over_mutual'] += 1
                by_pawns[cfg_counts(c[0])]['over_mutual'] += 1
                if np_:
                    classes_nopass['over_mutual'] += 1
            outf.write(json.dumps(rec_of(c, e, {'class': 'over_mutual' if v['mutual'] else 'over_exact',
                                                'qnotes': v['notes']})) + '\n')
        else:
            classes['over_pre_failed_stage3'] += 1
            if classes['over_pre_failed_stage3'] <= 8 and v:
                outf.write(json.dumps(rec_of(c, e, {'class': 'over_pre_failed', 'qnotes': v['notes'][:2]})) + '\n')
    outf.close()
    out = {'board': args.board, 'type': 't1', 'limits': [args.nw, args.nb], 'configs': len(cfgs), 'candidates': ncand,
           'illegal_candidates': nbad, 'stage1_survivors': len(survivors),
           'stage1_hist_(wleaks,bleaks,bcount)': {str(k): v for k, v in sorted(hist1.items())},
           'classes': dict(classes), 'classes_no_passer_in_group': dict(classes_nopass),
           'classes_by_pawns': {'%d+%d' % k: dict(v) for k, v in by_pawns.items()},
           'min_on_strong_miss_over_survivors': min_on_miss, 'on_miss_examples': onmiss_examples,
           'over_pre': nover_pre, 'q_apply_mismatch': apply_mismatch, 'seconds': round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(LOG, tag + '_summary.json'), 'w'), indent=1)
    log('DONE', json.dumps({k: out[k] for k in ('candidates', 'classes', 'min_on_strong_miss_over_survivors', 'over_pre')}))
