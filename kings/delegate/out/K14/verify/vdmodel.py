#!/usr/bin/env python3
"""Referee's own D-model checker (independent of K14/scripts).  Retrograde (counter-based) least fixed point on an
explicit product graph.  Tests Proposition 3.2' (a), (b), (c), (d) on random D-games, short and loopy.

A D-game: dict pos -> (Lopts, Ropts) where an option is an int position, or 'P' (White has won) or 'M' (Black has won).
Sum G (+) Z: product positions (x, z); a move changes one coordinate; a terminal option of either coordinate ends play.
State = (pos, side), side 0 = White (Left) to move.  A player with no option loses (normal play).
"""
import random, sys, itertools
from collections import defaultdict, deque


def solve_sum(G, Z):
    """returns dict (x,z,side) -> 'W'|'D'|'L'. G, Z: dict pos -> (L, R)."""
    states = [(x, z, s) for x in G for z in Z for s in (0, 1)]
    def opts(st):
        x, z, s = st
        out = []
        for o in G[x][s]:
            out.append(o if o in ('P', 'M') else (o, z, 1 - s))
        for o in Z[z][s]:
            out.append(o if o in ('P', 'M') else (x, o, 1 - s))
        return out
    O = {st: opts(st) for st in states}
    pred = defaultdict(list)
    for st, os_ in O.items():
        for o in os_:
            if o not in ('P', 'M'):
                pred[o].append(st)
    res = {st: 'D' for st in states}
    for sigma, name in ((0, 'W'), (1, 'L')):
        term = 'P' if sigma == 0 else 'M'
        win = set()
        cnt = {}
        q = deque()
        for st in states:
            s = st[2]
            if s == sigma:
                if any(o == term for o in O[st]):
                    win.add(st); q.append(st)
            else:
                # sigma-bar to move: needs all options good (non-terminal-of-sigma-bar)
                if all((o == term) for o in O[st]):  # includes the empty case
                    win.add(st); q.append(st)
                else:
                    cnt[st] = sum(1 for o in O[st] if o != term)
                    if any(o != term and o not in ('P', 'M') for o in O[st]) is False:
                        pass
        # for sigma-bar nodes, an own-terminal option (o not term and in P/M) is never good => never wins
        bad = set()
        for st in states:
            if st[2] != sigma and any((o in ('P', 'M')) and o != term for o in O[st]):
                bad.add(st)
        remaining = {}
        for st in states:
            if st[2] != sigma and st not in win and st not in bad:
                remaining[st] = sum(1 for o in O[st] if o not in ('P', 'M'))
        while q:
            u = q.popleft()
            for p in pred[u]:
                if p in win:
                    continue
                if p[2] == sigma:
                    win.add(p); q.append(p)
                elif p not in bad:
                    remaining[p] -= 1
                    # count distinct option occurrences; duplicates handled by counting occurrences
                    if remaining[p] == 0:
                        win.add(p); q.append(p)
        for st in win:
            res[st] = name
    return res


def pred_fix(G, Z):
    """pred lists contain a predecessor once per option occurrence; make that explicit (options are lists, so
    duplicates would double count both in remaining and pred - consistent)."""
    return None


def rnd_G(rng, n, short, pterm=0.25):
    G = {}
    for x in range(n):
        L, R = [], []
        for side, lst in ((0, L), (1, R)):
            k = rng.choice([0, 1, 1, 2, 3])
            for _ in range(k):
                u = rng.random()
                if u < pterm / 2:
                    lst.append('P')
                elif u < pterm:
                    lst.append('M')
                else:
                    if short:
                        if x + 1 < n:
                            lst.append(rng.randrange(x + 1, n))
                    else:
                        lst.append(rng.randrange(n))
        G[x] = (L, R)
    return G


def dud():
    return {0: ([0], [0])}


def mkZ(rng, kind, extra=0):
    """positions 0..3 = (a,b) with idx 2a+b (a: White king z/z', b: Black king w/w'), 4.. extra.
    kinds: exact, geq (T1,T2,T4 + arbitrary White extras), leq, """
    Z = {}
    allp = list(range(4 + extra))
    for a in (0, 1):
        for b in (0, 1):
            i = 2 * a + b
            L = [2 * (1 - a) + b]
            R = [2 * a + (1 - b)]
            Z[i] = (L, R)
    for e in range(4, 4 + extra):
        Z[e] = ([], [])
    def rand_opt(side, sui=True):
        u = rng.random()
        if u < 0.3:
            return 'P'
        if u < 0.6:
            return 'M'
        return rng.choice(allp)
    for i in range(4):
        L, R = Z[i]
        if kind == 'exact':
            for _ in range(rng.choice([0, 1, 2])):
                L.append('M')
            for _ in range(rng.choice([0, 1, 2])):
                R.append('P')
        elif kind == 'geq':
            for _ in range(rng.choice([0, 1, 2])):
                L.append(rand_opt(0))
            for _ in range(rng.choice([0, 1])):
                R.append('P')
        elif kind == 'leq':
            for _ in range(rng.choice([0, 1])):
                L.append('M')
            for _ in range(rng.choice([0, 1, 2])):
                R.append(rand_opt(1))
    for e in range(4, 4 + extra):
        L, R = Z[e]
        for _ in range(rng.choice([0, 1, 2])):
            L.append(rand_opt(0))
        for _ in range(rng.choice([0, 1, 2])):
            R.append(rand_opt(1))
    return Z


def mkZ_half(rng, extra, which):
    """which='W': T2,T4 at states 0,1 (White king at z); rest arbitrary.
       which='B': T1,T3 at states 0,2 (Black king at w); rest arbitrary."""
    Z = mkZ(rng, 'exact', extra)
    allp = list(range(4 + extra))
    def rand_opt():
        u = rng.random()
        return 'P' if u < .3 else 'M' if u < .6 else rng.choice(allp)
    # scramble everything outside the guarantee
    for i in range(4 + extra):
        a, b = (i >> 1, i & 1) if i < 4 else (None, None)
        L, R = Z[i]
        keepL = (which == 'B' and i < 4 and b == 0)
        keepR = (which == 'W' and i < 4 and a == 0)
        if which == 'W':
            # White-king-at-z states keep T2,T4: R = [shuttle]+ P's ; L arbitrary
            if keepR:
                R[:] = [2 * a + (1 - b)] + ['P'] * rng.choice([0, 1])
                L[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
            else:
                L[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
                R[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
        else:
            if keepL:
                L[:] = [2 * (1 - a) + b] + ['M'] * rng.choice([0, 1])
                R[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
            else:
                L[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
                R[:] = [rand_opt() for _ in range(rng.choice([0, 1, 2, 3]))]
    return Z


ORD = {'L': 0, 'D': 1, 'W': 2}


def main(ngames=300, seed=12345):
    rng = random.Random(seed)
    stats = defaultdict(lambda: [0, 0])  # name -> [ok, fail]
    first_fail = {}
    for it in range(ngames):
        short = (it % 2 == 0)
        n = rng.randint(2, 6)
        G = rnd_G(rng, n, short)
        base = solve_sum(G, dud())
        def b(x, s):
            return base[(x, 0, s)]
        for rep in range(6):
            extra = rng.choice([0, 0, 1, 2])
            # (a)
            Z = mkZ(rng, 'exact', extra)
            r = solve_sum(G, Z)
            for x in G:
                for st in range(4):
                    for s in (0, 1):
                        ok = r[(x, st, s)] == b(x, s)
                        stats['EQ_short' if short else 'EQ_loopy'][0 if ok else 1] += 1
                        if not ok: first_fail.setdefault('EQ', (G, Z, x, st, s))
            # (b)
            Z = mkZ(rng, 'geq', extra)
            r = solve_sum(G, Z)
            for x in G:
                for st in range(4):
                    for s in (0, 1):
                        ok = ORD[r[(x, st, s)]] >= ORD[b(x, s)]
                        stats['GE'][0 if ok else 1] += 1
                        if not ok: first_fail.setdefault('GE', (G, Z, x, st, s))
            Z = mkZ(rng, 'leq', extra)
            r = solve_sum(G, Z)
            for x in G:
                for st in range(4):
                    for s in (0, 1):
                        ok = ORD[r[(x, st, s)]] <= ORD[b(x, s)]
                        stats['LE'][0 if ok else 1] += 1
                        if not ok: first_fail.setdefault('LE', (G, Z, x, st, s))
            # (c)
            for which in ('W', 'B'):
                Z = mkZ_half(rng, extra, which)
                r = solve_sum(G, Z)
                states = (0, 1) if which == 'W' else (0, 2)
                tgt = 'W' if which == 'W' else 'L'
                for x in G:
                    for s in (0, 1):
                        if b(x, s) == tgt:
                            for st in states:
                                ok = r[(x, st, s)] == tgt
                                stats['HALF_' + which][0 if ok else 1] += 1
                                if not ok: first_fail.setdefault('HALF' + which, (G, Z, x, st, s))
            # (d) delete each arrow from an exact Z; with G arbitrary count differences
            for arrow in range(8):
                Z = mkZ(rng, 'exact', 0)
                # arrow k<4: White shuttle at state k ; k>=4: Black shuttle at state k-4
                st = arrow % 4
                if arrow < 4:
                    Z[st][0].remove(2 * (1 - (st >> 1)) + (st & 1))
                else:
                    Z[st][1].remove(2 * (st >> 1) + (1 - (st & 1)))
                r = solve_sum(G, Z)
                for x in G:
                    for s in (0, 1):
                        same = r[(x, st, s)] == b(x, s)
                        stats['NEG_same' if same else 'NEG_differ'][0] += 1
                        for st2 in range(4):
                            same2 = r[(x, st2, s)] == b(x, s)
                            stats['NEGall_same' if same2 else 'NEGall_differ'][0] += 1
    return stats, first_fail


def small_checks():
    G0 = {0: ([], [])}
    # exact
    Z = {}
    for a in (0, 1):
        for b in (0, 1):
            Z[2 * a + b] = ([2 * (1 - a) + b], [2 * a + 1 - b])
    r = solve_sum(G0, dud()); print('dud      ', r[(0, 0, 0)], r[(0, 0, 1)])
    r = solve_sum(G0, Z);     print('exact Z  ', [(r[(0, i, 0)], r[(0, i, 1)]) for i in range(4)])
    # opposition: delete diagonal state 3=(z',w'); suicides: others get 'M' for L, 'P' for R
    Zo = {0: ([2], [1]), 1: ([], []), 2: ([0], []), }
    # state0=(z,w): L->(z',w)=2, R->(z,w')=1 ; state1=(z,w'): L->(z',w') deleted ; R->(z,w)=0 ; state2=(z',w): L->(z,w)=0, R->(z',w') deleted
    Zo = {0: ([2, 'M'], [1, 'P']), 1: (['M'], [0, 'P']), 2: ([0, 'M'], ['P'])}
    r = solve_sum(G0, Zo); print('opposition', (r[(0, 0, 0)], r[(0, 0, 1)]), 'states1,2', (r[(0, 1, 0)], r[(0, 1, 1)]), (r[(0, 2, 0)], r[(0, 2, 1)]))
    # one arrow: Black shuttle missing at (z',w)=2
    Z1 = {i: (list(v[0]) + ['M'], list(v[1]) + ['P']) for i, v in Z.items()}
    Z1[2] = (Z1[2][0], ['P'])
    r = solve_sum(G0, Z1); print('one arrow  ', (r[(0, 0, 0)], r[(0, 0, 1)]))


if __name__ == '__main__':
    small_checks()
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 12345
    st, ff = main(n, seed)
    for k in sorted(st):
        print(k, st[k])
    print('first failures:', {k: 'x' for k in ff} if ff else 'none')
