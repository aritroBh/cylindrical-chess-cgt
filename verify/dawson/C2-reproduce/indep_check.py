"""Independent check of claim C2 (verifier, not the worker's code).

Imports nothing from dawson/ or cylcgt/.
  A. g(n) from the pin model of Dawson's chess written directly (choose a pin,
     remove it and its existing neighbours), no octal-code parsing.
  B. The 2025 paper's recurrence G(n) = mex{G(a)^G(b): a+b=n-3, a,b>=0}.
  C. Agreement counts g vs G for n=0..300, ring mismatches n=3..300.
  D. The claimed corrected recurrence, compared to A.
  E. The paper's literal 1xn rule: number of first moves from a full row.
  F. Pawn-level minimax on 3xn boards (flat and cylinder), compulsory captures,
     normal play, both colours to move first; plus sums of strips separated by
     empty files, compared with xor of g.
Run: cd <root> && PYTHONPATH=. .venv/bin/python verify/dawson/C2-reproduce/indep_check.py
"""
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)

N = 300

def mex(s):
    m = 0
    while m in s:
        m += 1
    return m

# A. pin model
g = [0] * (N + 1)
for n in range(1, N + 1):
    opts = set()
    for i in range(n):           # pin i removed with neighbours i-1, i+1 (if they exist)
        left = max(i - 1, 0)
        right = max(n - i - 2, 0)
        opts.add(g[left] ^ g[right])
    g[n] = mex(opts)

# B. paper recurrence
G = [0] * (N + 1)
for n in range(N + 1):
    G[n] = mex({G[a] ^ G[n - 3 - a] for a in range(0, n - 2)}) if n >= 3 else 0

# D. claimed corrected recurrence
h = [0] * (N + 1)
h[1] = 1
for n in range(2, N + 1):
    s = {h[n - 2]}
    for a in range(0, n - 2):
        s.add(h[a] ^ h[n - 3 - a])
    h[n] = mex(s)

print("A g(0..40):", g[:41])
print("B G(0..40):", G[:41])
print("D corrected recurrence equals pin model for n<=300:", h == g)
agree = [n for n in range(N + 1) if g[n] == G[n]]
print(f"C agreements g==G for n=0..{N}: {len(agree)} of {N+1}; disagreements {N+1-len(agree)}")
print("  agreeing n:", agree)
R = {n: int(g[n - 3] == 0) for n in range(3, N + 1)}
PR = {n: int(G[n - 3] == 0) for n in range(3, N + 1)}
rd = [n for n in range(3, N + 1) if R[n] != PR[n]]
print(f"C ring mismatches n=3..{N}: {len(rd)}; first: {rd[:10]}")
print("  correct ring wins n<=100:", [n for n in range(3, 101) if R[n]])
print("  paper ring wins n<=100:", [n for n in range(3, 101) if PR[n]])
# side: paper G vs octal 0.007 (Treblecross), computed by token-removal definition
t = [0] * (N + 1)
for n in range(1, N + 1):
    s = set()
    for i in range(0, n - 2):   # remove tokens i,i+1,i+2
        s.add(t[i] ^ t[n - i - 3])
    t[n] = mex(s)
print("side: paper G equals 0.007 (remove 3 contiguous) values:", t == G)

# E. paper's literal rule on a full 1xn row
for n in range(1, 8):
    row = [1] * n
    mv = [i for i in range(n) if row[i] and (i == 0 or not row[i - 1]) and (i == n - 1 or not row[i + 1])]
    print(f"E literal rule, full 1x{n} row: {len(mv)} legal first moves")

# F. pawn-level solver
EMPTY, WP, BP = 0, 1, 2

def make_solver(n, wrap):
    def nb(f):
        out = []
        for d in (-1, 1):
            x = f + d
            if wrap:
                x %= n
            if 0 <= x < n and x != f and x not in out:
                out.append(x)
        return out
    NB = [nb(f) for f in range(n)]
    promo = [False]

    def moves(pos, side):
        # pos: tuple of length 3n, index r*n+f, r=0 rank1, r=2 rank3
        me, op, d = (WP, BP, 1) if side == 0 else (BP, WP, -1)
        caps, pushes = [], []
        for r in range(3):
            r1 = r + d
            if not 0 <= r1 <= 2:
                continue
            for f in range(n):
                if pos[r * n + f] != me:
                    continue
                for f2 in NB[f]:
                    if pos[r1 * n + f2] == op:
                        p = list(pos); p[r * n + f] = EMPTY; p[r1 * n + f2] = me
                        caps.append(tuple(p))
                if pos[r1 * n + f] == EMPTY:
                    p = list(pos); p[r * n + f] = EMPTY; p[r1 * n + f] = me
                    pushes.append(tuple(p))
        res = caps if caps else pushes
        for p in res:
            if side == 0 and any(p[2 * n + f] == WP for f in range(n)):
                promo[0] = True
            if side == 1 and any(p[f] == BP for f in range(n)):
                promo[0] = True
        return res

    @lru_cache(maxsize=None)
    def win(pos, side):
        return any(not win(q, 1 - side) for q in moves(pos, side))
    return win, promo

def board(n, empty_files=()):
    pos = [EMPTY] * (3 * n)
    for f in range(n):
        if f in empty_files:
            continue
        pos[f] = WP
        pos[2 * n + f] = BP
    return tuple(pos)

maxflat = int(sys.argv[1]) if len(sys.argv) > 1 else 12
maxcyl = int(sys.argv[2]) if len(sys.argv) > 2 else 12
bad = 0
anypromo = False
for n in range(1, maxflat + 1):
    win, promo = make_solver(n, False)
    s = board(n)
    w0, w1 = win(s, 0), win(s, 1)
    pred = g[n] != 0
    ok = (w0 == pred and w1 == pred)
    bad += not ok
    anypromo |= promo[0]
    print(f"F flat n={n:2d}: first-player win (W first, B first) = ({w0},{w1}); g={g[n]}; paper G={G[n]}; ok={ok}; promo={promo[0]}")
for n in range(3, maxcyl + 1):
    win, promo = make_solver(n, True)
    s = board(n)
    w0, w1 = win(s, 0), win(s, 1)
    pred = R[n] == 1
    ok = (w0 == pred and w1 == pred)
    bad += not ok
    anypromo |= promo[0]
    print(f"F cyl  n={n:2d}: first-player win (W,B) = ({w0},{w1}); correct R={R[n]}; paper Ring={PR[n]}; ok={ok}; promo={promo[0]}")
# sums of two strips separated by one empty file on a flat board, and three strips
sum_bad = 0; sum_cnt = 0
maxsum = int(sys.argv[3]) if len(sys.argv) > 3 else 12
for tot in range(3, maxsum + 1):
    win, promo = make_solver(tot, False)
    for a in range(1, tot - 1):
        b = tot - 1 - a
        if b < 1 or b < a:
            continue
        s = board(tot, empty_files=(a,))
        pred = (g[a] ^ g[b]) != 0
        for side in (0, 1):
            sum_cnt += 1
            if win(s, side) != pred:
                sum_bad += 1
                print("  SUM MISMATCH", a, b, side)
    for a in range(1, tot):
        for b in range(1, tot):
            c = tot - 2 - a - b
            if c < 1:
                continue
            s = board(tot, empty_files=(a, a + 1 + b))
            pred = (g[a] ^ g[b] ^ g[c]) != 0
            sum_cnt += 1
            if win(s, 0) != pred:
                sum_bad += 1
                print("  SUM3 MISMATCH", a, b, c)
    anypromo |= promo[0]
# cylinder with one empty file = strip of n-1
for n in range(3, maxcyl + 1):
    win, promo = make_solver(n, True)
    s = board(n, empty_files=(0,))
    pred = g[n - 1] != 0
    sum_cnt += 2
    for side in (0, 1):
        if win(s, side) != pred:
            sum_bad += 1
            print("  CYL-EMPTY MISMATCH", n, side)
print(f"F start-position mismatches: {bad}; sum/variant tests: {sum_cnt}, mismatches: {sum_bad}; promotion ever reached: {anypromo}")
