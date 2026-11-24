"""K62 referee: Lambda_N against small D-games (Theorem 4.22).

Usage (from the repository root):
  .venv/bin/python kings/delegate/out/K62/verify/src/lam62.py named
  .venv/bin/python kings/delegate/out/K62/verify/src/lam62.py exhaust NPOS MODE      MODE: unreduced | reduced | single
  .venv/bin/python kings/delegate/out/K62/verify/src/lam62.py random SEED COUNT
For every D-game T and every Lambda_N (N = 1..NMAX) it records: full (the results of omega at both roots, both sides,
every position, and of 0_D at both q-states) and C ((C) at the bad move, every position); full == C is Theorem 4.18(b).
"""
import itertools
import random
import sys
import time

from ref62 import (DG, WHITE, BLACK, W_, D_, L_, exact, x_of, sum_values, dg_values, dsum, over, under, ladder,
                   chain)
import fam62

NMAX = 5


def lam_ctx(N):
    G, (r, m) = fam62.lam(N)
    ok, info = exact(G, 'strict', True)
    assert ok, info
    return G, x_of(G, r, m), sorted(info['qstates'])


CTX = None


def ctxs():
    global CTX
    if CTX is None:
        CTX = [lam_ctx(N) for N in range(1, NMAX + 1)]
    return CTX


def compare(T, cs=None):
    cs = cs or ctxs()
    ov = dg_values(dsum(over(), T))
    tv = dg_values(T)
    n = T.n
    out = []
    for G, x, qs in cs:
        v = sum_values(G, T)
        full = True
        for t in range(n):
            for s in (0, 1):
                o = ov[t * 2 + s]
                for rt in (0, 1):
                    if v[G.si(rt, 0, s) * n + t] != o:
                        full = False
            for qi in qs:
                if v[qi * n + t] != tv[t * 2 + (qi & 1)]:
                    full = False
        C = all(v[x * n + t] >= ov[t * 2 + 1] for t in range(n))
        out.append((full, C))
    return out


def root_vals(T, t, N):
    G, x, qs = lam_ctx(N)
    v = sum_values(G, T)
    ov = dg_values(dsum(over(), T))
    return v[G.si(0, 0, BLACK) * T.n + t], ov[t * 2 + 1], v[x * T.n + t]


VN = {W_: 'W', D_: 'D', L_: 'L'}


def named():
    print('Lambda_N beside ladders, chains and under_D (A = root A, Black to move; omega with Black to move)')
    for N in range(1, 7):
        cs = [lam_ctx(N)]
        lad = []
        for n in range(0, 9):
            full, C = compare(ladder(n), cs)[0]
            assert full == C
            lad.append('T%d:%s' % (n, 'pass' if full else 'FAIL'))
        ch = []
        for k in range(1, 9):
            T = chain(k)
            full, C = compare(T, cs)[0]
            assert full == C
            a, o, xv = root_vals(T, k, N)
            ch.append('C%d:%s(A=%s,w=%s)' % (k, 'pass' if full else 'FAIL', VN[a], VN[o]))
        a, o, xv = root_vals(ladder(N + 1), 0, N)
        full, C = compare(under(), cs)[0]
        print('Lambda_%d: %s' % (N, ' '.join(lad)))
        print('          %s' % ' '.join(ch))
        print('          beside T_%d at u_0: A=%s omega=%s x=%s; beside under_D: %s'
              % (N + 1, VN[a], VN[o], VN[xv], 'pass' if full else 'FAIL'))


# ---------------------------------------------------------------- enumeration
def slot_choices(n, side, mode):
    """Option sets of one side at one position, as bitmasks: bit i < n position i, bit n 'W', bit n+1 'B'."""
    WIN = 1 << (n if side == WHITE else n + 1)
    if mode == 'unreduced':
        return list(range(1 << (n + 2)))
    if mode == 'reduced':
        return [WIN] + list(range(1 << n))
    if mode == 'single':
        return [0, WIN] + [1 << i for i in range(n)]
    raise ValueError(mode)


def mask_to_opts(mask, n):
    o = [i for i in range(n) if mask >> i & 1]
    if mask >> n & 1:
        o.append('W')
    if mask >> (n + 1) & 1:
        o.append('B')
    return o


def exhaust(npos, mode):
    n = npos
    perms = list(itertools.permutations(range(n)))
    nm = 1 << (n + 2)
    mmap = []
    for p in perms:
        tab = []
        for mask in range(nm):
            r = mask & (3 << n)
            for i in range(n):
                if mask >> i & 1:
                    r |= 1 << p[i]
            tab.append(r)
        mmap.append(tab)
    chW = slot_choices(n, WHITE, mode)
    chB = slot_choices(n, BLACK, mode)
    cs = ctxs()
    fails = [0] * len(cs)
    first = [None] * len(cs)
    disagree = 0
    games = 0
    t0 = time.time()
    for Ls in itertools.product(chW, repeat=n):
        for Rs in itertools.product(chB, repeat=n):
            enc = Ls + Rs
            canon = True
            for pi, p in enumerate(perms[1:], 1):
                tab = mmap[pi]
                newL = [0] * n
                newR = [0] * n
                for i in range(n):
                    newL[p[i]] = tab[Ls[i]]
                    newR[p[i]] = tab[Rs[i]]
                if tuple(newL + newR) < enc:
                    canon = False
                    break
            if not canon:
                continue
            games += 1
            T = DG(n, [mask_to_opts(m, n) for m in Ls], [mask_to_opts(m, n) for m in Rs])
            res = compare(T, cs)
            for k, (full, C) in enumerate(res):
                if full != C:
                    disagree += 1
                if not full:
                    fails[k] += 1
                    if first[k] is None:
                        first[k] = (T.L, T.R)
                    if k + 1 >= n:
                        print('SEPARATION with |T| <= N: Lambda_%d' % (k + 1), T.L, T.R)
    print('exhaust n=%d mode=%s: %d games up to relabelling; full != (C): %d; %.0f s'
          % (n, mode, games, disagree, time.time() - t0))
    for k in range(len(cs)):
        print('  Lambda_%d fails %d%s' % (k + 1, fails[k], ('; first: L=%s R=%s' % first[k]) if first[k] else ''))


def rand_game(rng, n, style):
    L, R = [], []
    for t in range(n):
        for side, out in ((WHITE, L), (BLACK, R)):
            o = []
            if style == 'chain':
                # White steps down a chain, Black jumps; a few terminals
                if side == WHITE and t > 0 and rng.random() < 0.9:
                    o.append(rng.randrange(t))
                if side == BLACK and rng.random() < 0.8:
                    o.append(rng.randrange(n))
                if rng.random() < 0.08:
                    o.append(rng.choice('WB'))
            else:
                for u in range(n):
                    if rng.random() < 0.3:
                        o.append(u)
                if rng.random() < 0.12:
                    o.append('W')
                if rng.random() < 0.12:
                    o.append('B')
            out.append(o)
    return DG(n, L, R)


def random_run(seed, count):
    rng = random.Random(seed)
    global NMAX
    NMAX = 9
    cs = ctxs()
    t0 = time.time()
    sep_ok = [0] * NMAX     # games with |T| <= N tested against Lambda_N
    sep_bad = [0] * NMAX    # ... that separate (must stay 0)
    big_fail = [0] * NMAX   # games with |T| > N that separate Lambda_N
    big_tot = [0] * NMAX
    disagree = 0
    sizes = {}
    for i in range(count):
        n = rng.randint(2, 9)
        style = 'chain' if rng.random() < 0.5 else 'any'
        T = rand_game(rng, n, style)
        sizes[n] = sizes.get(n, 0) + 1
        res = compare(T, cs)
        for k, (full, C) in enumerate(res):
            N = k + 1
            if full != C:
                disagree += 1
            if n <= N:
                sep_ok[k] += 1
                if not full:
                    sep_bad[k] += 1
                    print('SEPARATION with |T| <= N: Lambda_%d' % N, T.L, T.R)
            else:
                big_tot[k] += 1
                big_fail[k] += not full
    print('random seed %d: %d loopy games (sizes %s); full != (C): %d; %.0f s'
          % (seed, count, dict(sorted(sizes.items())), disagree, time.time() - t0))
    for k in range(NMAX):
        print('  Lambda_%d: %d games with |T| <= %d, %d separate; %d games with |T| > %d, %d separate'
              % (k + 1, sep_ok[k], k + 1, sep_bad[k], big_tot[k], k + 1, big_fail[k]))


def rand_fixed(seed, count, npos):
    """Random reduced games with exactly npos positions (option density drawn per game) against Lambda_1..5."""
    rng = random.Random(seed)
    cs = ctxs()
    fails = [0] * len(cs)
    disagree = 0
    t0 = time.time()
    for _ in range(count):
        dens = rng.choice([0.2, 0.35, 0.5, 0.7])
        pt = rng.choice([0.0, 0.1, 0.25])
        L, R = [], []
        for t in range(npos):
            for side, out in ((WHITE, L), (BLACK, R)):
                if rng.random() < pt:
                    out.append(['W' if side == WHITE else 'B'])
                else:
                    out.append([u for u in range(npos) if rng.random() < dens])
        T = DG(npos, L, R)
        for k, (full, C) in enumerate(compare(T, cs)):
            disagree += full != C
            if not full:
                fails[k] += 1
                if k + 1 >= npos:
                    print('SEPARATION with |T| <= N: Lambda_%d' % (k + 1), T.L, T.R)
    print('random reduced games with %d positions, seed %d: %d games; full != (C): %d; %.0f s'
          % (npos, seed, count, disagree, time.time() - t0))
    for k in range(len(cs)):
        print('  Lambda_%d fails %d' % (k + 1, fails[k]))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'named':
        named()
    elif cmd == 'exhaust':
        exhaust(int(sys.argv[2]), sys.argv[3])
    elif cmd == 'random':
        random_run(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == 'randfixed':
        rand_fixed(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
