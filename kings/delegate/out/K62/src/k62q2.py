"""K62 question 2: Lambda_N against small finite D-games. Usage (from the repository root):
  .venv/bin/python kings/delegate/out/K62/src/k62q2.py ladders NMAX
  .venv/bin/python kings/delegate/out/K62/src/k62q2.py small2 NMAX          # every D-game with <= 2 positions (unreduced)
  .venv/bin/python kings/delegate/out/K62/src/k62q2.py small3 NMAX          # every D-game with <= 3 positions (reduced)
  .venv/bin/python kings/delegate/out/K62/src/k62q2.py random SEED COUNT NMAX
'Passes T' = full results of omega beside T (both roots, both sides, every t; every q-state against 0_D).
(C) beside T is computed as well and compared with the full check (Theorem 4.18(b), game by game).
"""
import itertools
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k62lib import (W, B, exactness, x_of, value_G_T, value_over_T, results_of_omega, condC,  # noqa: E402
                    ladder, UNDER, DGame)
from k62families import lam  # noqa: E402


def groups(nmax):
    out = []
    for N in range(1, nmax + 1):
        G = lam(N)
        ok, info = exactness(G)
        assert ok, info
        x = x_of(info['bad'][0])
        assert len(info['bad']) == 1
        out.append((N, G, info, x))
    return out


def check(gs, T, rom_rz=None):
    """For each group: (passes, (C) holds). Returns list of (N, passes, C, n_viol)."""
    if rom_rz is None:
        rom_rz = value_over_T(T)
    rom, rz = rom_rz
    res = []
    for N, G, info, x in gs:
        v = value_G_T(G, T)
        viol = results_of_omega(G, info, T, v, rom, rz)
        c = condC(G, x, T, v, rom)
        res.append((N, not viol, not c, len(viol)))
    return res


def run_ladders(nmax):
    gs = groups(nmax)
    print('# Lambda_N beside T_n: passes (full results of omega) / (C); and under_D')
    bad = 0
    for n in range(0, nmax + 3):
        T = ladder(n)
        for (N, ok, c, nv) in check(gs, T):
            expect = n <= N        # Theorem 4.21: passes T_n iff n <= N (N* = N + 1)
            if ok != c or ok != expect:
                bad += 1
            print('T_%d Lambda_%d passes=%s (C)=%s violations=%d %s' % (n, N, ok, c, nv,
                                                                       '' if ok == expect else 'UNEXPECTED'))
    for (N, ok, c, nv) in check(gs, UNDER):
        print('under_D Lambda_%d passes=%s (C)=%s' % (N, ok, c))
        if not ok:
            bad += 1
    # the separating values
    for N, G, info, x in gs:
        T = ladder(N + 1)
        v = value_G_T(G, T)
        rom, _ = value_over_T(T)
        print('Lambda_%d beside T_%d at u_0: root A Black to move = %d, omega Black to move = %d, x White to move = %d'
              % (N, N + 1, v[((0, 0), 0, B)], rom[(0, B)], v[((x[0], x[1]), 0, W)]))
    print('unexpected:', bad)


OPTS_L = None


def side_options(n, term):
    """Reduced option sets for one side at one position of an n-position game: {terminal win} or a subset of
    positions (a move to one's own losing terminal never matters; a winning terminal makes the rest irrelevant)."""
    out = [[term]]
    for r in range(n + 1):
        for sub in itertools.combinations(range(n), r):
            out.append(list(sub))
    return out


def all_games(n, reduced):
    """All D-games on n positions; reduced: options per side as in side_options; unreduced: every subset of
    positions + both terminals."""
    if reduced:
        oL, oR = side_options(n, '+'), side_options(n, '-')
    else:
        elems = list(range(n)) + ['+', '-']
        allsub = [list(s) for r in range(len(elems) + 1) for s in itertools.combinations(elems, r)]
        oL = oR = allsub
    perms = list(itertools.permutations(range(n)))

    def canon(Ls, Rs):
        best = None
        for p in perms:
            inv = {p[i]: i for i in range(n)}
            # relabel position i -> p[i]
            L2 = [None] * n
            R2 = [None] * n
            for i in range(n):
                L2[p[i]] = tuple(sorted((o if isinstance(o, str) else '%d' % p[o]) for o in Ls[i]))
                R2[p[i]] = tuple(sorted((o if isinstance(o, str) else '%d' % p[o]) for o in Rs[i]))
            key = (tuple(L2), tuple(R2))
            if best is None or key < best:
                best = key
        return best

    seen = set()
    for Ls in itertools.product(oL, repeat=n):
        for Rs in itertools.product(oR, repeat=n):
            key = canon(Ls, Rs)
            if key in seen:
                continue
            seen.add(key)
            yield DGame([list(x) for x in Ls], [list(x) for x in Rs])


def run_small(nmax, npos, reduced):
    gs = groups(nmax)
    count = 0
    fails = {N: 0 for N, _, _, _ in gs}
    first = {}
    mism = 0
    for T in all_games(npos, reduced):
        count += 1
        for (N, ok, c, nv) in check(gs, T):
            if ok != c:
                mism += 1
            if not ok:
                fails[N] += 1
                if N not in first:
                    first[N] = (T.L, T.R)
    print('# D-games with %d positions (%s, up to relabelling): %d games' % (npos, 'reduced' if reduced else 'all',
                                                                           count))
    for N in sorted(fails):
        print('Lambda_%d: games not passed = %d%s' % (N, fails[N],
                                                     ('   first: L=%s R=%s' % first[N]) if N in first else ''))
    print('full check vs (C) mismatches:', mism)


def random_game(rng, n):
    L, R = [], []
    for i in range(n):
        for lst, term, bad in ((L, '+', '-'), (R, '-', '+')):
            opts = []
            for j in range(n):
                if rng.random() < 0.35:
                    opts.append(j)
            if rng.random() < 0.12:
                opts.append(term)
            if rng.random() < 0.05:
                opts.append(bad)
            lst.append(opts)
    return DGame(L, R)


def run_random(seed, count, nmax):
    rng = random.Random(seed)
    gs = groups(nmax)
    tot = viol_thm = mism = 0
    fails_big = {}
    for _ in range(count):
        n = rng.randint(2, nmax + 3)
        T = random_game(rng, n)
        tot += 1
        for (N, ok, c, nv) in check(gs, T):
            if ok != c:
                mism += 1
            if n <= N and not ok:
                viol_thm += 1
                print('VIOLATION: Lambda_%d fails a game with %d positions: L=%s R=%s' % (N, n, T.L, T.R))
            if n > N and not ok:
                fails_big[(N, n)] = fails_big.get((N, n), 0) + 1
    print('seed', seed, 'random loopy D-games', tot, 'violations of Theorem 4.21(i)', viol_thm,
          'full-vs-(C) mismatches', mism)
    print('failures with more than N positions (N, |T|): count', sorted(fails_big.items()))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ladders':
        run_ladders(int(sys.argv[2]))
    elif cmd == 'small2':
        nm = int(sys.argv[2])
        run_small(nm, 1, False)
        run_small(nm, 2, False)
    elif cmd == 'small3':
        run_small(int(sys.argv[2]), 3, True)
    elif cmd == 'random':
        run_random(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
