import sys, random, time
from mylocal import Game
from myenum_lib import attacked_count
board, W, H, fzhi, wmax, bmax, Tmax, budget, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), float(sys.argv[8]), int(sys.argv[9])
random.seed(seed)
g = Game(board, W, H, fzhi, True)
Fs = list(range(fzhi + 1)); allsq = [(f, r) for f in Fs for r in range(2, H)]
t0 = time.time(); roots = {0: 0, 1: 0, 2: 0}; wins = {0: 0, 1: 0, 2: 0}; bad = []
while time.time() - t0 < budget:
    f = random.choice(Fs); nw = random.randint(1, wmax)
    wr = random.sample(range(2, H), min(nw, H - 2)); wp = frozenset((f, r) for r in wr)
    kr = random.randint(max(wr) + 1, H); bk = (f, kr)
    free = [s for s in allsq if s not in wp and s != bk]
    # bias toward adjacent files to get attacked pawns
    nb = random.randint(0, bmax); bp = frozenset(random.sample(free, min(nb, len(free))))
    wk = (random.choice(Fs), random.randint(1, H))
    if wk in wp or wk in bp or wk == bk or wk in g.kn[bk] or g.att_by_black(wk, bp, bk): continue
    a = min(attacked_count(board, W, wp, bp), 2); roots[a] += 1
    T = g.minT(wp, bp, wk, bk, tmax=Tmax)
    if T:
        wins[a] += 1
        if a < 2: bad.append((sorted(wp), sorted(bp), wk, bk, T))
    if len(g.memo) > 2000000: g.memo.clear()
print(board, W, H, 'fz<=%d' % fzhi, 'wmax', wmax, 'bmax', bmax, 'roots(0,1,2+)', roots, 'wins', wins, 'B1-violations', bad[:3], flush=True)
