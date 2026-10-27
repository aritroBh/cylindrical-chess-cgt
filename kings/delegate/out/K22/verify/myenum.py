# Referee enumeration: roots with all white (s-bar) pawns on one file f, black (s) king on f above them, s to move,
# black pawns anywhere on F_Z. Uses mylocal.Game (my own solver) and my own strategy model-check.
import sys, itertools, time
from mylocal import Game
board, W, H, fzhi, wmax, bmax, Tmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
flist = [int(x) for x in sys.argv[8].split(',')] if len(sys.argv) > 8 else list(range(fzhi + 1))
dostrat = (len(sys.argv) > 9 and sys.argv[9] == 'strat')
g = Game(board, W, H, fzhi, True); gp = Game(board, W, H, fzhi, False)
def nf(f):
    return f % W if board == 'cyl' else (f if 0 <= f < W else None)
def attacked_count(wp, bp):
    n = 0
    for (f, x) in wp:
        for df in (-1, 1):
            h = nf(f + df)
            if h is not None and (h, x + 1) in bp: n += 1; break
    return n
def strat_check(g, st):
    """s strategy: capture an attacked s-bar pawn, else pass; explore all white replies. Return violation string or None."""
    seen = set(); stack = [st]
    while stack:
        s0 = stack.pop()   # black to move
        if s0 in seen: continue
        seen.add(s0)
        wp, bp, wk, bk, ep = s0
        ms, incheck = g.black_moves(s0)
        if incheck: return 'black in check (mate risk)'
        # attacked pawns -> capture moves (pawn captures of white pawns)
        capt = []
        for m in ms:
            if m != 'PROMO' and m[0] != wp and m[3] == bk and len(m[1]) == len(bp) and m[0] < wp:  # a white pawn removed by a black pawn capture
                if len(m[0]) == len(wp) - 1 and m[2] == wk: capt.append(m)
        passm = (wp, bp, wk, bk, None)
        if capt:
            nxt = capt[0]   # any capture is allowed by the strategy; test every one
            choices = capt
        else:
            choices = [passm]
        for c in choices:
            # after black move, white to move: all white moves; promotion = violation
            wms = g.white_moves(c)
            for m in wms:
                if m in ('WIN', 'LOSE'): return 'white promotes'
                stack.append(m)
    return None
tot = {}
t0 = time.time()
wins_by = {0: 0, 1: 0, 2: 0}; roots_by = {0: 0, 1: 0, 2: 0}; viol = []; strat_roots = 0; stratviol = []; maxT = 0
Fs = list(range(fzhi + 1))
allsq = [(ff, r) for ff in Fs for r in range(2, H)]
for f in flist:
    for nw in range(1, wmax + 1):
        for wranks in itertools.combinations(range(2, H), nw):
            wp = frozenset((f, r) for r in wranks)
            top = max(wranks)
            for kr in range(top + 1, H + 1):
                bk = (f, kr)
                if bk in wp: continue
                free = [s for s in allsq if s not in wp and s != bk]
                for nb in range(0, bmax + 1):
                    for bps in itertools.combinations(free, nb):
                        bp = frozenset(bps)
                        a = min(attacked_count(wp, bp), 2)
                        for wkf in Fs:
                            for wkr in range(1, H + 1):
                                wk = (wkf, wkr)
                                if wk in wp or wk in bp or wk == bk: continue
                                if wk in g.kn[bk]: continue
                                if g.att_by_black(wk, bp, bk): continue
                                st = (wp, bp, wk, bk, None)
                                roots_by[a] += 1
                                T = g.minT(wp, bp, wk, bk, tmax=Tmax)
                                if T:
                                    wins_by[a] += 1; maxT = max(maxT, T)
                                    if a < 2: viol.append((sorted(wp), sorted(bp), wk, bk, T))
                                if gp is not g and a < 2 and gp.minT(wp, bp, wk, bk, tmax=Tmax): viol.append(('P-noqc', sorted(wp), sorted(bp), wk, bk))
                                if dostrat and a < 2:
                                    strat_roots += 1
                                    v = strat_check(g, st)
                                    if v: stratviol.append((sorted(wp), sorted(bp), wk, bk, v))
    print('f=%d done %.0fs memo=%d' % (f, time.time() - t0, len(g.memo)), flush=True)
    if len(g.memo) > 3000000: g.memo.clear(); gp.memo.clear()
print('RESULT', board, W, H, 'fz=0..%d' % fzhi, 'wmax', wmax, 'bmax', bmax, 'Tmax', Tmax, 'f', flist)
print(' roots by #attacked (0,1,2+):', roots_by); print(' white wins by #attacked:', wins_by, 'max T', maxT)
print(' wins with <=1 attacked (violations of B1 lemma):', len(viol), viol[:5])
if dostrat: print(' strategy check roots', strat_roots, 'violations', len(stratviol), stratviol[:5])
