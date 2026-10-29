#!/usr/bin/env python3
"""K26 final (copy of ctxtest.py with one addition): also writes, for every context with a disagreement, all its roots (king state, side, P value, D-model value).

K26 part 4: test groups in small pawn contexts.

  ctxtest.py groups.json out.json [--nctx 40] [--seed 1] [--checker ref3]

groups.json: list of {"id", "board", "class", "H", "wk": [squares], "bk": [squares], "wp": [...], "bp": [...]}
  wk / bk have 2 squares for a shuttling king and 1 for a fixed king.
For each group and each orientation (as given, and colour-flipped: rank r -> H+1-r, colours swapped) the reservoir is
  both shuttle                     -> dud            (Theorem 3.4(a))
  White shuttles, Black frozen     -> on             (Theorem 3.4(b));  mirrored: off
  White shuttles, Black freezes    -> under          (Proposition 4.6 mirrored); flipped: over (Proposition 4.6 literally)
The context pawns stand on two files at distance >= 2 from F_Z (f,g on flat boards and cyl:8xH, e,f on cyl:7xH), at most
2 White + 2 Black pawns on ranks 2..H-1, no e.p. right at the root.  For each context, every root (king states x both sides
to move) is solved in the P model by kpp and (values only) by ref3; the result is compared with the D-model prediction
r(G + Z) of dmodel.py.  Contexts: all <=2+2 configurations are scored by the D-model first; the sample is
(i) the empty context, (ii) --nctx uniformly random ones, (iii) --nctx random ones among those whose D-prediction is
decisive for some side or differs between the two sides to move.
"""
import json, os, random, sys, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k26lib import *
import dmodel

args = sys.argv[1:]
gfile, ofile = args[0], args[1]
nbase = 60
nflip = 20
ncheck = 24
seed = 1
checker = 'ref3'
FILES_OVERRIDE = None
i = 2
while i < len(args):
    if args[i] == '--nbase':
        nbase = int(args[i + 1]); i += 2
    elif args[i] == '--ncheck':
        ncheck = int(args[i + 1]); i += 2
    elif args[i] == '--nflip':
        nflip = int(args[i + 1]); i += 2
    elif args[i] == '--seed':
        seed = int(args[i + 1]); i += 2
    elif args[i] == '--checker':
        checker = args[i + 1]; i += 2
    elif args[i] == '--files':       # override the context files, two letters, e.g. ef
        FILES_OVERRIDE = tuple(FILES.index(ch) + 1 for ch in args[i + 1]); i += 2
    else:
        raise SystemExit('bad arg ' + args[i])

safe_nice()


def sqparse(s):
    return (FILES.index(s[0]) + 1, int(s[1:]))


def sqname(f, r):
    return FILES[f - 1] + str(r)


def flip_group(g):
    H = g['H']
    fl = lambda lst: [sqname(*(lambda t: (t[0], H + 1 - t[1]))(sqparse(s))) for s in lst]
    return {'id': g['id'] + '~', 'board': g['board'], 'class': g.get('class', '') + '~', 'H': H,
            'wk': fl(g['bk']), 'bk': fl(g['wk']), 'wp': fl(g['bp']), 'bp': fl(g['wp'])}


def reservoir_of(g):
    sw, sb = len(g['wk']) == 2, len(g['bk']) == 2
    if sw and sb:
        return 'dud'
    cls = g['class'].rstrip('~')
    flipped = g['class'].endswith('~')
    if sw and not sb:
        return ('under' if cls.startswith('over') or cls.startswith('under') else 'on')
    if sb and not sw:
        return ('over' if cls.startswith('over') or cls.startswith('under') else 'off')
    raise ValueError('group without shuttle')


def ctx_files(board):
    if FILES_OVERRIDE:
        return FILES_OVERRIDE
    kind, dims = board.split(':')
    W = int(dims.split('x')[0])
    if kind == 'cyl' and W == 7:
        return (5, 6)   # e, f  (d and g are buffer files)
    return (6, 7)       # f, g


def all_contexts(files, H):
    sqs = [(f, r) for f in files for r in range(2, H)]
    out = []
    for kw in range(3):
        for wp in itertools.combinations(sqs, kw):
            for kb in range(3):
                for bp in itertools.combinations(sqs, kb):
                    if set(wp) & set(bp):
                        continue
                    out.append((frozenset(wp), frozenset(bp)))
    return out


def pos_line(g, wk, bk, wp, bp, stm, ctx_wp, ctx_bp):
    parts = ['K' + wk, 'k' + bk] + ['P' + s for s in g['wp']] + ['p' + s for s in g['bp']]
    parts += ['P' + sqname(*s) for s in sorted(ctx_wp)] + ['p' + sqname(*s) for s in sorted(ctx_bp)]
    return ' '.join(parts) + ' %s -' % stm


groups = json.load(open(gfile))
todo = []
for g in groups:
    todo.append(g)
    todo.append(flip_group(g))

report = []
for g in todo:
    res = reservoir_of(g)
    H = g['H']
    files = ctx_files(g['board'])
    ctxs = all_contexts(files, H)
    rnd = random.Random(seed * 1000003 + sum(map(ord, g['id'])))
    # D-model predictions for every context (both sides to move)
    roots = [(w, b, None, s) for (w, b) in ctxs for s in (0, 1)]
    pred = dmodel.solve(roots, res, H)
    gal = dmodel.solve(roots, 'none', H)   # G alone, for the premise of Proposition 4.6
    def decisive(c):
        return any(pred[(c[0], c[1], None, s)] != 'D' for s in (0, 1)) or pred[(c[0], c[1], None, 0)] != pred[(c[0], c[1], None, 1)]
    empty = (frozenset(), frozenset())
    ntarget = nflip if g['id'].endswith('~') else nbase
    sel = [empty]
    for lo, hi, frac in ((0, 2, 0.35), (3, 3, 0.40), (4, 4, 0.25)):
        pool = [c for c in ctxs if lo <= len(c[0]) + len(c[1]) <= hi and c != empty]
        k = max(1, round(ntarget * frac / 2))
        sel += rnd.sample(pool, min(k, len(pool)))
        dpool = [c for c in pool if decisive(c)]
        sel += rnd.sample(dpool, min(k, len(dpool)))
    seen = set()
    sel = [c for c in sel if not (c in seen or seen.add(c))]
    # positions
    lines, meta = [], []
    for c in sel:
        for wk in g['wk']:
            for bk in g['bk']:
                for s in (0, 1):
                    lines.append(pos_line(g, wk, bk, None, None, 'w' if s == 0 else 'b', c[0], c[1]))
                    meta.append((c, wk, bk, s))
    r1, r2 = [], []
    CH = 12 * len(g['wk']) * len(g['bk']) * 2   # 12 contexts per solver call
    for lo in range(0, len(lines), CH):
        a_, _ = run_solver(lines[lo:lo + CH], g['board'], 'kpp', moves=False)
        r1 += a_
        if lo < ncheck * len(g['wk']) * len(g['bk']) * 2:     # the checker (ref3) is run on the first ncheck contexts only
            b_, _ = run_solver(lines[lo:lo + CH], g['board'], checker, moves=False)
            r2 += b_
        else:
            r2 += [None] * len(a_)
    v1 = [x.rsplit('|', 1)[1].split()[0] for x in r1]
    v2 = [x.rsplit('|', 1)[1].split()[0] if x else None for x in r2]
    nchk = sum(1 for b in v2 if b is not None)
    nchk_dis = sum(1 for a, b in zip(v1, v2) if b is not None and a != b)
    agree = dis = 0
    prop_tested = prop_ok = 0
    ex = []
    percontext_bad = set()
    kings_differ = 0
    byctx = collections.defaultdict(set)
    detail = collections.defaultdict(list)
    for (c, wk, bk, s), v in zip(meta, v1):
        p = pred[(c[0], c[1], None, s)]
        byctx[(c, s)].add(v)
        detail[c].append((wk, bk, 'w' if s == 0 else 'b', v, p))
        if v == 'X':
            dis += 1
            ex.append(('ILLEGAL', pos_line(g, wk, bk, None, None, 'w' if s == 0 else 'b', c[0], c[1])))
            percontext_bad.add(c)
            continue
        if v == p:
            agree += 1
        else:
            dis += 1
            percontext_bad.add(c)
            if len(ex) < 6:
                ex.append((pos_line(g, wk, bk, None, None, 'w' if s == 0 else 'b', c[0], c[1]), 'P=' + v, 'D-model=' + p))
        # Proposition 4.6 (premise reading)
        if res == 'over':
            prem = gal[(c[0], c[1], None, 1)] == 'W'    # White wins G moving second
            want = 'W'
        elif res == 'under':
            prem = gal[(c[0], c[1], None, 0)] == 'L'    # Black wins G moving second
            want = 'L'
        else:
            prem = False
        if prem:
            prop_tested += 1
            if v == want:
                prop_ok += 1
    kings_differ = sum(1 for k, vs in byctx.items() if len(vs) > 1)
    rep = {'id': g['id'], 'board': g['board'], 'reservoir': res, 'class': g['class'],
           'wk': g['wk'], 'bk': g['bk'], 'wp': g['wp'], 'bp': g['bp'],
           'context_files': ''.join(FILES[f - 1] for f in files), 'contexts': len(sel), 'roots': len(lines),
           'roots_agree_with_D_model': agree, 'roots_disagree': dis,
           'contexts_with_a_disagreement': len(percontext_bad),
           'contexts_where_P_result_depends_on_king_state': kings_differ,
           'roots_checked_by_checker': nchk, 'kpp_vs_checker_value_mismatches': nchk_dis, 'checker': checker,
           'prop46_premise_roots': prop_tested, 'prop46_conclusion_holds': prop_ok,
           'D_values_seen': dict(collections.Counter(pred[(c[0], c[1], None, s)] for c in sel for s in (0, 1))),
           'P_values_seen': dict(collections.Counter(v1)),
           'disagreement_examples': ex,
           'mismatch_contexts': [{'W': sorted(sqname(*q) for q in c[0]), 'B': sorted(sqname(*q) for q in c[1]), 'roots': detail[c]} for c in sorted(percontext_bad, key=lambda c: (sorted(c[0]), sorted(c[1])))],
           'all_contexts': [{'W': sorted(sqname(*q) for q in c[0]), 'B': sorted(sqname(*q) for q in c[1]), 'bad': c in percontext_bad} for c in sel]}
    report.append(rep)
    print(g['id'], res, 'contexts', len(sel), 'roots', len(lines), 'agree', agree, 'dis', dis, 'checked', nchk, 'chk-mismatch', nchk_dis,
          'prop46', prop_ok, '/', prop_tested, file=sys.stderr, flush=True)
json.dump(report, open(ofile, 'w'), indent=1)
