import sys, collections
SP = sys.argv[1]
def load(fn, col):
    d = {}
    for ln in open(fn):
        if ln.startswith('#'): continue
        p, r = ln.rstrip('\n').split('\t'); d[p] = r[col] if col is not None else r
    return d
def run(W, H):
    def sq(s): return (ord(s[0]) - 97, int(s[1:]) - 1)
    def adj(a, b):
        df = abs(a[0] - b[0]); df = min(df, W - df); return a != b and abs(a[1] - b[1]) <= 1 and df <= 1
    def qatt(q, t, wk):
        for dfl, dr in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            f, r = q
            for _ in range(2 * (W + H)):
                f = (f + dfl) % W; r += dr
                if r < 0 or r >= H or (f, r) == q: break
                if (f, r) == t: return True
                if (f, r) == wk: break
        return False
    def promo(wk, bk, q):  # 'win', 'kxq', 'stalemate'
        legal = 0
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if not df and not dr: continue
                d = ((bk[0] + df) % W, bk[1] + dr)
                if d[1] < 0 or d[1] >= H or d == bk: continue
                if d == wk or adj(d, wk): continue
                if d == q: return 'kxq'
                if qatt(q, d, wk): continue
                legal += 1
        if legal: return 'win'
        return 'win' if qatt(q, bk, wk) else 'stalemate'
    b = f'{W}x{H}'
    P = load(f'{SP}/C_{b}.txt', 12); A = load(f'{SP}/A_{b}.txt', None); N = load(f'{SP}/N_{b}.txt', None)
    def cls(r):
        if set(r) == {'W'}: return 'DEC'
        if set(r) == {'D'}: return 'DUD'
        return 'ON' if r[25] == 'W' and r[27] == 'D' else 'OTHER'
    cnt = collections.Counter()
    for p, a in A.items():
        if a == P[p]: continue
        t = p.split(); d = {x[0]: sq(x[1:]) for x in t[:3]}; s = t[3]
        wk, pp, bk = d['K'], d['P'], d['k']
        cause = 'later'
        if s == 'w':
            q = (pp[0], pp[1] + 1)
            outs = []
            if q[1] == H - 1 and q != wk and q != bk: outs.append(promo(wk, bk, q))
            if 'kxq' in outs: cause = 'kxq_now'
            elif 'stalemate' in outs: cause = 'stalemate_now'
        cnt[(s, cause, cls(N[p]))] += 1
    tot = len(A); dif = sum(1 for p in A if A[p] != P[p])
    print(b, 'diff', dif, 'of', tot, '%.2f%%' % (100 * dif / tot), dict(sorted(cnt.items())))
for H in (6, 7, 8):
    for W in range(3, 9): run(W, H)
