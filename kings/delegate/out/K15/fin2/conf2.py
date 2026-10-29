#!/usr/bin/env python3
"""K15 final confirmation harness (P model, kp_p --pmodel), for dud / over / under candidates.

  gen  BOARD ZTYPE GROUPFILE OUTPREFIX [--nctx N] [--seed S] [--allstates] [--maxpawns K]
       GROUPFILE: one root per line (tab-separated, first field 'K.. k.. P.. p.. [w -]').
       For every group: translate (cylinder) so that it starts on file a; collect the king states by a BFS over the
       moves that kp_p --moves values D (the shuttles) in the empty context (--allstates; else the root only);
       beside every context G (pawns only, on one file or on two non-adjacent files, no pawn can ever capture)
       write the position with each king state and each side to move.  The prediction is r(G (+) Z_D), Z in
       {dud, over, under}, computed by confirm.solve_d (Theorem 3.4(a) / Proposition 4.6, brute force).
  cmp  OUTPREFIX KPPOUT : compare the kp_p output (A B pair, A == B means exact) with the predictions.
"""
import sys, os, json, random, subprocess, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import confirm as C
FILES = "abcdefgh"
KPP = os.path.join(HERE, 'bin', 'kpp')


def parse(pos):
    return [(t[0], FILES.index(t[1]), int(t[2:])) for t in pos.split() if len(t) >= 3 and t[0] in 'KkPp']


def fmt(p):
    return ' '.join(f"{c}{FILES[f]}{r}" for c, f, r in p)


def shift_left(p, W):
    best = None
    for tr in range(W):
        q = [(c, (f - tr) % W, r) for c, f, r in p]
        key = (max(f for _, f, _ in q), sum(f for _, f, _ in q))
        if best is None or key < best[0]: best = (key, q)
    return best[1]


def kpp_moves(board, lines):
    out = subprocess.run([KPP, '--board', board, '--ep', 'on', '--cap', '0', '--pmodel', '--moves'],
                         input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
    return [l for l in out if '|' in l]


def states_of(board, W, toks):
    """BFS over king states reachable by king moves that kp_p (empty context) values D (draw).  One kpp call per BFS wave (both sides to move)."""
    seen = {}
    frontier = [tuple(toks)]
    while frontier:
        wave = []
        for kt in frontier:
            ks = {t[0]: t for t in kt}
            key = (ks['K'], ks['k'])
            if key in seen: continue
            seen[key] = 1
            wave.append(kt)
        if not wave: break
        lines = []
        for kt in wave:
            base = ' '.join(kt)
            lines += [f"{base} w -", f"{base} b -"]
        res = {}
        for l in kpp_moves(board, lines):
            parts = l.split(' | ')
            if len(parts) >= 3: res[parts[0].strip()] = parts[2]
        frontier = []
        for kt in wave:
            base = ' '.join(kt)
            for stm in 'wb':
                mvs = res.get(f"{base} {stm} -", '')
                mover = 'K' if stm == 'w' else 'k'
                for mv in mvs.split():
                    m, v = mv.split(':')
                    if v != 'D' or m[0] != 'K': continue
                    to = m[3:5]
                    nt = [t for t in kt if t[0] != mover] + [mover + to]
                    nt = tuple(sorted(nt, key=lambda t: ('KkPp'.index(t[0]), t)))
                    frontier.append(nt)
    return list(seen.keys())


def context_list(W, H, F, seed, nctx, maxp):
    rnd = random.Random(seed)
    free = [f for f in range(W) if f >= F + 1 and f != W - 1]  # not the group files, not the buffer files F and W-1
    if not free:  # no context file at distance >= 2 from the group files (e.g. 5 files on a 7-file cylinder): only the empty context
        return {'C0_empty': ([], [])}
    named = {}
    f0 = free[0]
    X = FILES[f0]
    named['C0_empty'] = ([], [])
    named['C1_blocked'] = ([f"{X}3"], [f"{X}4"])
    named['C2_onemove'] = ([f"{X}3"], [f"{X}5"]) if H >= 6 else ([f"{X}3"], [f"{X}4"])
    named['C3_gap2'] = ([f"{X}2"], [f"{X}5"]) if H >= 6 else ([f"{X}2"], [f"{X}4"])
    ctx = dict(named)
    tries = 0
    ranks = list(range(2, H))
    while len(ctx) < nctx and tries < 5000:
        tries += 1
        nfiles = 1 if (len(free) < 3 or rnd.random() < 0.6) else 2
        fs = rnd.sample(free, nfiles)
        if nfiles == 2 and (abs(fs[0] - fs[1]) in (1, W - 1)): continue
        n = rnd.randint(1, maxp)
        sel = []
        for _ in range(n):
            sel.append(FILES[rnd.choice(fs)] + str(rnd.choice(ranks)))
        if len(set(sel)) < len(sel): continue
        wl, bl = [], []
        for s in sel:
            (wl if rnd.random() < 0.5 else bl).append(s)
        # same-file pawns must not jump: a white pawn above a black pawn on the same file cannot pass; allowed (blocked or crossed never happens)
        name = 'R_' + ''.join(sorted(wl)) + '_' + ''.join(sorted(bl))
        if name in ctx: continue
        ctx[name] = (sorted(wl), sorted(bl))
    return ctx


def cmd_gen(a):
    board, z, gfile, outp = a[:4]
    opts = a[4:]
    nctx = int(opts[opts.index('--nctx') + 1]) if '--nctx' in opts else 12
    seed = int(opts[opts.index('--seed') + 1]) if '--seed' in opts else 5
    maxp = int(opts[opts.index('--maxpawns') + 1]) if '--maxpawns' in opts else 3
    allst = '--allstates' in opts
    W, H = map(int, board.split(':')[1].split('x'))
    groups = []
    for l in open(gfile):
        l = l.strip()
        if not l or l.startswith('#'): continue
        groups.append(l.split('\t')[0])
    rows = []; lines = []
    for gi, g in enumerate(groups):
        p = shift_left(parse(g), W) if board.startswith('cyl') else parse(g)
        F = max(f for _, f, _ in p) + 1
        toks = [f"{c}{FILES[f]}{r}" for c, f, r in sorted(p, key=lambda x: ('KkPp'.index(x[0]), x[1], x[2]))]
        sts = states_of(board, W, toks) if allst else [None]
        if allst and board.startswith('cyl'):
            # the group files are those used by ANY piece in ANY state of the king closure (the kings may use more files than the pawns do)
            used = {FILES.index(t[1]) for t in toks} | {FILES.index(x[1]) for ks in sts for x in ks}
            best = min(range(W), key=lambda tr: (max((f - tr) % W for f in used), tr))
            sh = lambda t: t[0] + FILES[(FILES.index(t[1]) - best) % W] + t[2:]
            toks = [sh(t) for t in toks]; sts = [(sh(a), sh(b)) for a, b in sts]
            F = max((f - best) % W for f in used) + 1
        elif allst:
            used = {FILES.index(t[1]) for t in toks} | {FILES.index(x[1]) for ks in sts for x in ks}
            F = max(used) + 1
        ctx = context_list(W, H, F, seed + gi, nctx, maxp)
        for cname, (cw, cb) in ctx.items():
            pw, pb = C.solve_d(H, [C.sq(x) for x in cw], [C.sq(x) for x in cb], z)
            ct = [f"P{x}" for x in cw] + [f"p{x}" for x in cb]
            if sts == [None]:
                kstates = [(next(t for t in toks if t[0] == 'K'), next(t for t in toks if t[0] == 'k'))]
            else:
                kstates = sts
            for ks in kstates:
                gt = [ks[0], ks[1]] + [t for t in toks if t[0] in 'Pp']
                for stm, pred in (('w', pw), ('b', pb)):
                    pos = ' '.join(gt + ct) + f" {stm} -"
                    lines.append(pos)
                    rows.append({'gi': gi, 'group': ' '.join(toks), 'F': F, 'ctx': cname, 'stm': stm, 'pos': pos, 'z': z, 'pred': pred,
                                 'nstates': len(kstates)})
    open(outp + '.in', 'w').write('\n'.join(lines) + '\n')
    json.dump(rows, open(outp + '.rows.json', 'w'))
    print(len(groups), 'groups,', len(rows), 'positions ->', outp + '.in')


ORD = {'L': 0, 'D': 1, 'W': 2}


def cmd_cmp(a):
    outp, kout = a[:2]
    rows = json.load(open(outp + '.rows.json'))
    res = [l.rstrip('\n') for l in open(kout) if '|' in l]
    done = {}
    for l in res:
        pos, ab = l.split(' | ')[:2]
        done[pos.strip()] = ab.split()
    summ = {}
    for r in rows:
        k = r['group']
        s = summ.setdefault(k, {'agree': 0, 'DISAGREE': 0, 'inexact': 0, 'missing': 0, 'bad_ctx': set(), 'n': 0})
        s['n'] += 1
        if r['pos'] not in done: s['missing'] += 1; r['status'] = 'missing'; continue
        A, B = done[r['pos']]
        r['A'], r['B'] = A, B
        if A == B:
            if A == r['pred']: s['agree'] += 1; r['status'] = 'agree'
            else: s['DISAGREE'] += 1; r['status'] = 'DISAGREE'; s['bad_ctx'].add(r['ctx'])
        else:
            s['inexact'] += 1; r['status'] = 'inexact'
    json.dump(rows, open(outp + '.table.json', 'w'))
    for k, s in summ.items():
        print(f"{k}\tn={s['n']} agree={s['agree']} DISAGREE={s['DISAGREE']} inexact={s['inexact']} missing={s['missing']}\tbad contexts: {sorted(s['bad_ctx'])[:6]}")


if __name__ == '__main__':
    {'gen': cmd_gen, 'cmp': cmd_cmp}[sys.argv[1]](sys.argv[2:])
