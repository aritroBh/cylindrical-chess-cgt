"""Quantitative form of Theorem 2.7: for LC rows, does s-bar's guided strategy win in P within T moves against every legal real play of s?
usage: depth_check.py rows.json board FZ maxrows"""
import sys, json, random
from kb import B
from cert import Cert
rows = json.load(open(sys.argv[1]))
kind, dims = sys.argv[2].split(':'); W, H = map(int, dims.split('x')); wrap = kind == 'cyl'
FZ = [int(x) for x in sys.argv[3].split(',')]; maxrows = int(sys.argv[4])
Bd = B(W, H, wrap); C = Cert(Bd, FZ)
random.seed(1); random.shuffle(rows); rows = rows[:maxrows]
memo = {}
def sbar_wins(pos, t, sb):
    """s-bar to move with t moves left; only guided (Z-move, locally winning) moves"""
    key = ('f', pos, t)
    if key in memo: return memo[key]
    res = False
    for kind_, frm, to, promo, nxt in Bd.moves(pos):
        if kind_ == 'K' and not C.inz(to): continue
        if kind_ == 'P' and not C.inz(frm): continue
        if promo: res = True; break
        sd = 1 - sb
        mv = Bd.moves(nxt)
        if not mv:
            if Bd.check(nxt, sd): res = True; break   # mate of s
            continue                                    # stalemate of s
        if t < 2: continue
        # guided filter: projection must be locally winning with t-1 moves
        pj = C.proj(nxt)
        if not (C.lg(pj, t - 1, sb, False)): continue
        ok = True
        for k2, f2, t2, p2, n2 in mv:
            if p2: ok = False; break       # s promotes
            if not sbar_wins(n2, t - 1, sb): ok = False; break
        if ok: res = True; break
    memo[key] = res
    return res
bad = 0; tested = 0
for r in rows:
    Q = Bd.parse(r['Q']); sb = 1 - Q[4]
    for T, v in r['T'].items():
        T = int(T); h = v[0]
        m1 = r.get('m1', r.get('mu', 0))
        if not h or m1 < T + 1: continue
        # s to move at Q: all legal s moves, then s-bar guided
        mv = Bd.moves(Q); ok = True
        if not mv and not Bd.check(Q, Q[4]): ok = False   # stalemate at Q (L3 would exclude)
        for k2, f2, t2, p2, n2 in mv:
            if p2: ok = False; break
            if not sbar_wins(n2, T, sb): ok = False; break
        tested += 1
        if not ok:
            bad += 1; print("DEPTH-FAIL", r['Q'], "T", T, "mu", m1, flush=True)
    if len(memo) > 2_000_000: memo.clear(); C.lmemo.clear()
print(sys.argv[1], "rows", len(rows), "LC pairs tested", tested, "fails", bad, flush=True)
