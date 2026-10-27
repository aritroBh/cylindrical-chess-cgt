#!/usr/bin/env python3
"""K14: brute-force check of the D-model statements of Proposition 3.2' (two-sided shuttle) on random short
D-games G and several Z, by generic least-fixed-point solving of the explicit sum G (+) Z (Definition 1.3).

A D-game is a dict: position -> (list of Left options, list of Right options); an option is a position name or
the terminals '+' (White has won) and '-' (Black has won).  Sum positions are tuples; any move to a terminal ends the
whole game; a player with no option (in any coordinate) loses (normal play).

Checks (all comparisons are of the pair r(.,White to move), r(.,Black to move), order L<D<W):
  EQ   Z satisfying T1-T4 (extra suicides allowed)              : r(G+Z) == r(G+dud) at all four states, all x
  GE   T1,T2,T4 and extra White options of any kind             : r(G+Z) >= r(G+dud)
  LE   T1,T2,T3 and extra Black options of any kind             : r(G+Z) <= r(G+dud)
  HALF T2,T4 at the z-slice only, anything else arbitrary       : r(G+dud)=W  ==>  r(G+Z)=W at (z,w),(z,w')
  NEG  drop one shuttle arrow (8 variants)                      : count how often the result differs from dud
usage: prop_check.py [number of random G]"""
import random, sys, itertools

ORD = {'L': 0, 'D': 1, 'W': 2}


def solve(game, start_positions):
    """game: dict pos -> (Lopts, Ropts); positions may be tuples. returns r[(pos, side)] for all reachable."""
    opts = {}
    stack = [(p, s) for p in start_positions for s in (0, 1)]
    while stack:
        st = stack.pop()
        if st in opts: continue
        p, s = st
        lo, ro = game[p]
        o = []
        for t in (lo if s == 0 else ro):
            if t in ('+', '-'): o.append(('T', 0 if t == '+' else 1))
            else: o.append(('S', (t, 1 - s)))
        opts[st] = o
        for k, v in o:
            if k == 'S': stack.append(v)
    win = {0: set(), 1: set()}
    for sg in (0, 1):
        Wn = win[sg]; ch = True
        while ch:
            ch = False
            for st, o in opts.items():
                if st in Wn: continue
                if st[1] == sg: ok = any((k == 'T' and v == sg) or (k == 'S' and v in Wn) for k, v in o)
                else: ok = all((k == 'T' and v == sg) or (k == 'S' and v in Wn) for k, v in o)   # empty o: loses (normal play)
                if ok: Wn.add(st); ch = True
    return {st: ('W' if st in win[0] else 'L' if st in win[1] else 'D') for st in opts}


def summ(G, Z):
    """disjunctive sum with game-ending terminals."""
    game = {}
    for x, (gl, gr) in G.items():
        for c, (zl, zr) in Z.items():
            def mv(opts_g, opts_z):
                out = []
                for t in opts_g: out.append(t if t in ('+', '-') else (t, c))
                for t in opts_z: out.append(t if t in ('+', '-') else (x, t))
                return out
            game[(x, c)] = (mv(gl, zl), mv(gr, zr))
    return game


def rand_G(rng, n):
    names = ['g%d' % i for i in range(n)]
    G = {}
    for i, nm in enumerate(names):          # options only to higher-numbered positions (acyclic) or terminals
        def ro():
            k = rng.choice([0, 0, 1, 1, 2])
            pool = names[i + 1:] + ['+', '-']
            return [rng.choice(pool) for _ in range(k)] if pool else []
        G[nm] = (ro(), ro())
    return G


S4 = [('z', 'w'), ('z', 'W'), ('Z', 'w'), ('Z', 'W')]    # (z,z') -> 'z','Z' ; (w,w') -> 'w','W'
def flip(a): return {'z': 'Z', 'Z': 'z', 'w': 'W', 'W': 'w'}[a]
def sname(a, b): return 'z' + a + b


def make_Z(rng, kind):
    """kind: eq | ge | le | half | neg<i>.  returns (Z dict, dud dict)"""
    Z = {}
    extra = ['u0', 'u1']
    for a, b in S4:
        L = [sname(flip(a), b)]; R = [sname(a, flip(b))]
        if kind == 'eq' or kind == 'le':
            for _ in range(rng.choice([0, 1, 2])): L.append('-')
        if kind == 'eq' or kind == 'ge':
            for _ in range(rng.choice([0, 1, 2])): R.append('+')
        if kind == 'ge':
            for _ in range(rng.choice([1, 2])): L.append(rng.choice(['+', '-', 'u0', 'u1', sname(*rng.choice(S4))]))
        if kind == 'le':
            for _ in range(rng.choice([1, 2])): R.append(rng.choice(['+', '-', 'u0', 'u1', sname(*rng.choice(S4))]))
        Z[sname(a, b)] = (L, R)
    for u in extra: Z[u] = ([rng.choice(['+', '-', 'u0', 'u1', sname(*rng.choice(S4))]) for _ in range(rng.choice([0, 1]))],
                            [rng.choice(['+', '-', 'u0', 'u1', sname(*rng.choice(S4))]) for _ in range(rng.choice([0, 1]))])
    return Z


def dud(): return {'w0': (['w0'], ['w0'])}


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = random.Random(1414)
    stats = {}
    def bump(k, ok): stats.setdefault(k, [0, 0]); stats[k][0 if ok else 1] += 1
    for it in range(N):
        G = rand_G(rng, rng.choice([3, 4, 5, 6]))
        # reference: G + dud
        gd = summ(G, dud()); rd = solve(gd, [(x, 'w0') for x in G])
        for kind in ('eq', 'ge', 'le'):
            for rep in range(3):
                Z = make_Z(rng, kind)
                gz = summ(G, Z); rz = solve(gz, [(x, sname(a, b)) for x in G for a, b in S4])
                for x in G:
                    for a, b in S4:
                        for s in (0, 1):
                            ref = rd[((x, 'w0'), s)]; got = rz[((x, sname(a, b)), s)]
                            if kind == 'eq': bump('EQ', ref == got)
                            if kind == 'ge': bump('GE', ORD[got] >= ORD[ref])
                            if kind == 'le': bump('LE', ORD[got] <= ORD[ref])
        # HALF: T2,T4 at the z-slice ((z,w),(z,W)) only; everything else random
        for rep in range(3):
            Z = {}
            for a, b in S4:
                if a == 'z':
                    L = [rng.choice(['+', '-', 'u0', sname(*rng.choice(S4))]) for _ in range(rng.choice([0, 1, 2]))]
                    R = [sname(a, flip(b))] + ['+'] * rng.choice([0, 1])
                else:
                    L = [rng.choice(['+', '-', 'u0', sname(*rng.choice(S4))]) for _ in range(rng.choice([0, 1, 2]))]
                    R = [rng.choice(['+', '-', 'u0', sname(*rng.choice(S4))]) for _ in range(rng.choice([0, 1, 2]))]
                Z[sname(a, b)] = (L, R)
            Z['u0'] = ([rng.choice(['+', '-', sname(*rng.choice(S4))])], [rng.choice(['+', '-', sname(*rng.choice(S4))])])
            gz = summ(G, Z); rz = solve(gz, [(x, sname(a, b)) for x in G for a, b in S4 if a == 'z'])
            for x in G:
                for b in ('w', 'W'):
                    for s in (0, 1):
                        if rd[((x, 'w0'), s)] == 'W': bump('HALF', rz[((x, sname('z', b)), s)] == 'W')
        # NEG: drop one of the 8 shuttle arrows from an otherwise exact Z (suicides present)
        for i in range(8):
            Z = {}
            for j, (a, b) in enumerate(S4):
                L = [sname(flip(a), b)] + ['-']; R = [sname(a, flip(b))] + ['+']
                if i == 2 * j: L = ['-']
                if i == 2 * j + 1: R = ['+']
                Z[sname(a, b)] = (L, R)
            gz = summ(G, Z); rz = solve(gz, [(x, sname(a, b)) for x in G for a, b in S4])
            for x in G:
                for a, b in S4:
                    for s in (0, 1):
                        bump('NEG%d-differs' % i, rz[((x, sname(a, b)), s)] != rd[((x, 'w0'), s)])
    for k in sorted(stats): print(k, 'agree/hold' if not k.startswith('NEG') else 'same/differ', stats[k])
    # explicit small counterexamples with G = empty game (a single position with no options)
    G0 = {'e': ([], [])}
    rd0 = solve(summ(G0, dud()), [('e', 'w0')])
    print('G=0, dud     :', rd0[(('e', 'w0'), 0)], rd0[(('e', 'w0'), 1)])
    # opposition: the diagonal state (Z,W) missing
    Zopp = {'zzw': (['zZw', '-'], ['zzW', '+']), 'zZw': (['zzw', '-'], ['+']), 'zzW': (['-'], ['zzw', '+'])}
    ro = solve(summ(G0, Zopp), [('e', 'zzw')])
    print('G=0, opposition (3 states) at (z,w):', ro[(('e', 'zzw'), 0)], ro[(('e', 'zzw'), 1)])
    # one Black arrow missing at (z',w)
    Zm = {sname(a, b): ([sname(flip(a), b), '-'], [sname(a, flip(b)), '+']) for a, b in S4}
    Zm['zZw'] = (['zzw', '-'], ['+'])
    rm = solve(summ(G0, Zm), [('e', 'zzw')])
    print('G=0, Black shuttle missing at (z\',w):', rm[(('e', 'zzw'), 0)], rm[(('e', 'zzw'), 1)])


main()
