import random, sys
board, f0, f1, mw, mb, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
random.seed(seed)
W, H = map(int, board.split(':')[1].split('x'))
cyl = board.startswith('cyl')
def nm(f, r): return 'abcdefghi'[f] + str(r + 1)
win = [(f, r) for f in range(f0, f1 + 1) for r in range(1, H - 1)]
out = []
while len(out) < n:
    k = random.sample(win, random.randint(0, mw) + random.randint(0, mb))
    nw = random.randint(0, min(mw, len(k)))
    wp, bp = k[:nw], k[nw:nw + mb]
    occ = set(wp) | set(bp)
    free = [(f, r) for f in range(W) for r in range(H) if (f, r) not in occ]
    wk, bk = random.sample(free, 2)
    stm = random.choice('wb')
    ep = '-'
    # occasionally make an e.p. flag consistent with a double step just played
    if random.random() < 0.3:
        if stm == 'b':
            c = [(f, r) for (f, r) in wp if r == 3 and (f, 2) not in occ and (f, 1) not in occ and (f, 2) not in (wk, bk) and (f, 1) not in (wk, bk)]
            if c: f, r = random.choice(c); ep = nm(f, 2)
        else:
            c = [(f, r) for (f, r) in bp if r == H - 4 and (f, H - 3) not in occ and (f, H - 2) not in occ and (f, H - 3) not in (wk, bk) and (f, H - 2) not in (wk, bk)]
            if c: f, r = random.choice(c); ep = nm(f, H - 3)
    toks = ['K' + nm(*wk), 'k' + nm(*bk)] + ['P' + nm(*s) for s in wp] + ['p' + nm(*s) for s in bp]
    out.append(' '.join(toks) + ' ' + stm + ' ' + ep)
print('\n'.join(out))
