#!/usr/bin/env python3
"""K14: test the chess bridge (Theorem 3.2''') on a concrete group against kpsolve's P model (kpp --pmodel).

For a group (kings with shuttles z<->z', w<->w', static Z-pawns) and each context G of a list (pawn-only, flat board):
 1. enumerate the REGULAR positions: reachable from the four states x {w,b to move} by D-moves (context moves of the
    pawn-only game, e.p. flag as in kpsolve, and the two shuttles; a king move resets the e.p. flag);
 2. run kpp --pmodel --moves on every regular position and classify the legal moves: context pawn moves, the side's
    shuttle, or OTHER (any other king move, any Z-pawn move);
 3. (Pun_W) = at every regular position with White to move every OTHER move has value L (White loses);
    (Pun_B) = at every regular position with Black to move every OTHER move has value W (from White's view);
 4. compare the P value of the 8 roots with the D-model value r(G (+) dud_D) (dmodel.py) and test
      (a) Pun_B everywhere  and r_D = W  ==> P = W (both z);   Pun_W everywhere and r_D = L ==> P = L;
      (b) Pun_W and Pun_B everywhere ==> P = r_D (draws included).
Prints a per-context table and a summary; JSON lines to OUT.
usage: bridge_check.py GROUP.jsonl CONTEXTS.jsonl OUT.jsonl [max contexts]"""
import sys, json, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from dmodel import Ctx, solve
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAVY = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh'
HCMD = ['nice', '-n', '15'] if os.environ.get('K14_DIRECT') else [HEAVY]
W, H = 7, 6
def nm(s): return chr(97 + s % W) + str(s // W + 1)
def S(n): return (int(n[1:]) - 1) * W + ord(n[0]) - 97

grp = json.loads(open(sys.argv[1]).readline())
ctxs = [json.loads(l) for l in open(sys.argv[2])][:int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9]
out = open(sys.argv[3], 'w')
ctx = Ctx(W, H, True)
zK, zk = list(grp['K']), list(grp['k'])
zpawn_w, zpawn_b = list(grp['P']), list(grp['p'])
board = grp['board']
gnames = ['P' + nm(s) for s in zpawn_w] + ['p' + nm(s) for s in zpawn_b]


def posstr(a, b, wp, bp, ep, stm):
    ws = ['P' + nm(s) for s in sorted(wp)] + ['P' + nm(s) for s in zpawn_w]
    bs = ['p' + nm(s) for s in sorted(bp)] + ['p' + nm(s) for s in zpawn_b]
    return ' '.join(['K' + nm(a), 'k' + nm(b)] + ws + bs + ['w' if stm == 0 else 'b', nm(ep) if ep >= 0 else '-'])


def regular(wp0, bp0):
    """BFS over (wp,bp,ep,a,b,stm)."""
    start = [(frozenset(wp0), frozenset(bp0), -1, a, b, s) for a in zK for b in zk for s in (0, 1)]
    seen, stack = set(), list(start)
    while stack:
        st = stack.pop()
        if st in seen: continue
        seen.add(st)
        wp, bp, ep, a, b, s = st
        for kind, nx in ctx.moves(wp, bp, ep, s):
            if kind == 'mv': stack.append((nx[0], nx[1], nx[2], a, b, 1 - s))
        # shuttle (resets the e.p. flag)
        if s == 0: stack.append((wp, bp, -1, zK[1] if a == zK[0] else zK[0], b, 1))
        else: stack.append((wp, bp, -1, a, zk[1] if b == zk[0] else zk[0], 0))
    return seen, start


summary = {'ctx': 0, 'PunW': 0, 'PunB': 0, 'both': 0, 'a_checks': 0, 'a_fail': 0, 'b_checks': 0, 'b_fail': 0,
           'mismatch_ctx': 0, 'mismatch_ctx_with_pun_failure': 0, 'mismatch_roots': 0}
for cx in ctxs:
    wp0, bp0 = {S(n) for n in cx['w']}, {S(n) for n in cx['b']}
    reg, start = regular(wp0, bp0)
    states = sorted(reg, key=lambda t: (sorted(t[0]), sorted(t[1]), t[2], t[3], t[4], t[5]))
    posl = [posstr(a, b, wp, bp, ep, s) for (wp, bp, ep, a, b, s) in states]
    p = subprocess.run(HCMD + [os.path.join(D, 'bin', 'kpp'), '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel', '--moves'],
                       input='\n'.join(posl) + '\n', capture_output=True, text=True)
    res = {}
    for line in p.stdout.splitlines():
        if ' | ' not in line: continue
        parts = [x.strip() for x in line.split(' | ')]
        res[parts[0]] = (parts[1].split(), [m.split(':') for m in parts[2].split()] if len(parts) > 2 else [])
    punW = punB = True; leaks = []
    for st, pos in zip(states, posl):
        wp, bp, ep, a, b, s = st
        r = res.get(pos)
        if r is None: raise SystemExit('missing ' + pos)
        kf = a if s == 0 else b
        shut = (zK if s == 0 else zk)
        shut = shut[1] if kf == shut[0] else shut[0]
        for mv, v in r[1]:
            if mv[0] == 'K' and mv == 'K' + nm(kf) + nm(shut): continue          # the shuttle
            if mv[0] == 'P' and S(mv[1:3]) not in (set(zpawn_w) | set(zpawn_b)): continue   # a context pawn move
            # OTHER move
            if s == 0 and v != 'L': punW = False; leaks.append((pos, mv, v))
            if s == 1 and v != 'W': punB = False; leaks.append((pos, mv, v))
    dres = {0: solve(ctx, wp0, bp0, -1, 'dud')[0], 1: solve(ctx, wp0, bp0, -1, 'dud')[1]}
    mism = 0; rows = []
    for (wp, bp, ep, a, b, s) in start:
        pos = posstr(a, b, wp, bp, ep, s)
        pv = res[pos][0]; pv = pv[0] if pv[0] == pv[1] else '?'
        rows.append((nm(a), nm(b), s, dres[s], pv))
        mism += (pv != dres[s])
        if punB and dres[s] == 'W':
            summary['a_checks'] += 1; summary['a_fail'] += (pv != 'W')
        if punW and dres[s] == 'L':
            summary['a_checks'] += 1; summary['a_fail'] += (pv != 'L')
        if punW and punB:
            summary['b_checks'] += 1; summary['b_fail'] += (pv != dres[s])
    summary['ctx'] += 1; summary['PunW'] += punW; summary['PunB'] += punB; summary['both'] += (punW and punB)
    summary['mismatch_roots'] += mism; summary['mismatch_ctx'] += (mism > 0)
    summary['mismatch_ctx_with_pun_failure'] += (mism > 0 and not (punW and punB))
    rec = {'w': cx['w'], 'b': cx['b'], 'dud': cx['dud'], 'regular': len(states), 'PunW': punW, 'PunB': punB, 'mismatch_roots': mism,
           'roots': rows, 'first_leaks': leaks[:3]}
    out.write(json.dumps(rec) + '\n'); out.flush()
    print('ctx %-22s %-22s dud=%s regular=%4d PunW=%d PunB=%d mismatch_roots=%d' % (' '.join(cx['w']), ' '.join(cx['b']), ''.join(cx['dud']), len(states), punW, punB, mism), flush=True)
print(json.dumps(summary))
