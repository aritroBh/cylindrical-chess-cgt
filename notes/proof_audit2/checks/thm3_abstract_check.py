"""Abstract check of the engine of paper Theorem 3 (LOOPY Thm 1.14(i) + Lemma 1.7) on random short D-sums.
Components: random DAGs whose options are nodes or the terminals PLUS/MINUS (a decisive event ends the whole game).
'Chess-like' game: same sum, plus a king group Z in which EVERY move is a suicide (Z-move by White gives MINUS, by Black PLUS)
and each side always has at least that Z-move (so nobody is ever stalemated).
Claim (Theorem 3): result of the chess-like game = normal-play result of the sum with Z deleted (a side with no option loses).
Run: python3 thm3_abstract_check.py [N] [seed]
"""
import random, sys
from functools import lru_cache
sys.setrecursionlimit(100000)
def rand_comp(rng):
    n = rng.randint(1, 5)
    L, R = [], []
    for x in range(n):
        def opts():
            o = []
            for _ in range(rng.choice([0, 1, 1, 2])):
                c = rng.random()
                if c < .15: o.append('PLUS')
                elif c < .3: o.append('MINUS')
                elif x + 1 < n: o.append(rng.randint(x + 1, n - 1))
            return tuple(dict.fromkeys(o))
        L.append(opts()); R.append(opts())
    return n, L, R
def check(rng):
    comps = [rand_comp(rng) for _ in range(rng.randint(1, 3))]
    @lru_cache(None)
    def win(state, side, withZ):    # True iff `side` to move wins
        for i, (n, L, R) in enumerate(comps):
            for o in (L[state[i]] if side == 'W' else R[state[i]]):
                if o == ('PLUS' if side == 'W' else 'MINUS'):
                    return True
                if o in ('PLUS', 'MINUS'):
                    continue           # a suicide (own move into the opponent's terminal): never wins
                ns = state[:i] + (o,) + state[i + 1:]
                if not win(ns, 'B' if side == 'W' else 'W', withZ):
                    return True
        return False                   # no winning option; with Z the side must play the (losing) Z-move; without Z it has lost
    s0 = tuple(0 for _ in comps)
    a = [win(s0, s, True) for s in 'WB']
    return a
rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
# The two games coincide by construction in this encoding (a suicide / Z-move is never winning and never needed);
# the point of the check is the non-trivial bookkeeping below: explicit chess-like search INCLUDING the Z-move as a real option.
def explicit(rng):
    comps = [rand_comp(rng) for _ in range(rng.randint(1, 3))]
    def moves(state, side):
        out = []
        for i, (n, L, R) in enumerate(comps):
            for o in (L[state[i]] if side == 'W' else R[state[i]]):
                out.append(('T', o) if o in ('PLUS', 'MINUS') else ('S', state[:i] + (o,) + state[i + 1:]))
        return out
    @lru_cache(None)
    def chess(state, side):        # with Z-move available to both sides: Z-move = terminal for the opponent
        opts = moves(state, side) + [('T', 'MINUS' if side == 'W' else 'PLUS')]
        for kind, v in opts:
            if kind == 'T':
                if v == ('PLUS' if side == 'W' else 'MINUS'): return True
            elif not chess(v, 'B' if side == 'W' else 'W'): return True
        return False
    @lru_cache(None)
    def normal(state, side):       # Z deleted, normal play: no option = loss; terminals end the game
        opts = moves(state, side)
        for kind, v in opts:
            if kind == 'T':
                if v == ('PLUS' if side == 'W' else 'MINUS'): return True
            elif not normal(v, 'B' if side == 'W' else 'W'): return True
        return False
    s0 = tuple(0 for _ in comps)
    return [chess(s0, s) for s in 'WB'], [normal(s0, s) for s in 'WB']
bad = 0
for _ in range(N):
    a, b = explicit(rng)
    if a != b: bad += 1; print("MISMATCH", a, b)
print("random D-sums:", N, "mismatches:", bad)
