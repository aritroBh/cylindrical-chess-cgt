"""Brute-force check of paper Theorem 8 (= LOOPY Thm 3.4) on random short D-games.
A D-game: nodes 0..n-1 (acyclic: options go to larger indices), each node has Left options and Right options,
each option a node or the terminal PLUS (White has won) / MINUS (Black has won); 'no option' loses (normal play).
Combined game G + reservoir: the reservoir lets White pass (on), Black pass (off) or both (dud).
Reference: direct retrograde (attractor) computation on states (node, side to move) of the combined loopy graph,
infinite play = draw.  Claim: closed forms of the theorem.
Run: python3 thm8_check.py [N_games] [seed]
"""
import random, sys

def solve(n, L, R, passW, passB):
    # states (x, s) s in 'LR'; result W/L/D from White's view by least fixed point (attractor).
    win = {}   # (x,s) -> 'W' or 'B'
    changed = True
    def opts(x, s):
        o = list(L[x] if s == 'L' else R[x])
        if s == 'L' and passW: o.append(('N', x, 'R'))
        if s == 'R' and passB: o.append(('N', x, 'L'))
        return o
    def val(o, s):
        # value of moving along o, for the mover s: returns 'W','B' or None (unknown)
        if o == 'PLUS': return 'W'
        if o == 'MINUS': return 'B'
        if isinstance(o, tuple):
            return win.get((o[1], o[2]))
        return win.get((o, 'R' if s == 'L' else 'L'))
    while changed:
        changed = False
        for x in range(n):
            for s in 'LR':
                if (x, s) in win: continue
                me = 'W' if s == 'L' else 'B'
                os = opts(x, s)
                if not os:
                    win[(x, s)] = 'B' if s == 'L' else 'W'; changed = True; continue
                vals = [val(o, s) for o in os]
                if me in vals:
                    win[(x, s)] = me; changed = True
                elif all(v is not None and v != me for v in vals):
                    win[(x, s)] = 'B' if me == 'W' else 'W'; changed = True
    return win

def closed_form(n, L, R, mode):
    """Theorem: returns dict (x,s)->'W'/'B'/'D' using the paper's/LOOPY's recursions."""
    from functools import lru_cache
    sys.setrecursionlimit(10000)
    if mode == 'dud':
        @lru_cache(None)
        def LamL(x):   # White wins with White to move
            return any(o == 'PLUS' or (o not in ('PLUS', 'MINUS') and LamR(o)) for o in L[x])
        @lru_cache(None)
        def LamR(x):   # White wins with Black to move
            return LamL(x) and all(o == 'PLUS' or (o != 'MINUS' and LamL(o)) for o in R[x])
        @lru_cache(None)
        def RhoR(x):
            return any(o == 'MINUS' or (o not in ('PLUS', 'MINUS') and RhoL(o)) for o in R[x])
        @lru_cache(None)
        def RhoL(x):
            return RhoR(x) and all(o == 'MINUS' or (o != 'PLUS' and RhoR(o)) for o in L[x])
        out = {}
        for x in range(n):
            for s in 'LR':
                w = LamL(x) if s == 'L' else LamR(x)
                b = RhoL(x) if s == 'L' else RhoR(x)
                assert not (w and b)
                out[(x, s)] = 'W' if w else ('B' if b else 'D')
        return out
    if mode == 'on':      # only White passes: Black wins iff it forces a Black-favourable decisive event vs passing White
        @lru_cache(None)
        def PR(x):
            return any(o == 'MINUS' or (o not in ('PLUS', 'MINUS') and PL(o)) for o in R[x])
        @lru_cache(None)
        def PL(x):
            return PR(x) and all(o == 'MINUS' or (o != 'PLUS' and PR(o)) for o in L[x])
        return {(x, s): ('B' if (PL(x) if s == 'L' else PR(x)) else 'W') for x in range(n) for s in 'LR'}
    if mode == 'off':     # mirror
        @lru_cache(None)
        def QL(x):
            return any(o == 'PLUS' or (o not in ('PLUS', 'MINUS') and QR(o)) for o in L[x])
        @lru_cache(None)
        def QR(x):
            return QL(x) and all(o == 'PLUS' or (o != 'MINUS' and QL(o)) for o in R[x])
        return {(x, s): ('W' if (QL(x) if s == 'L' else QR(x)) else 'B') for x in range(n) for s in 'LR'}

def rand_game(rng):
    n = rng.randint(1, 9)
    L, R = [], []
    for x in range(n):
        def opts():
            k = rng.choice([0, 1, 1, 2, 3])
            o = []
            for _ in range(k):
                c = rng.random()
                if c < .2: o.append('PLUS')
                elif c < .4: o.append('MINUS')
                elif x + 1 < n: o.append(rng.randint(x + 1, n - 1))
            return list(dict.fromkeys(o))
        L.append(opts()); R.append(opts())
    return n, L, R

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    bad = 0; draws = 0
    for _ in range(N):
        n, L, R = rand_game(rng)
        for mode, pw, pb in (('dud', True, True), ('on', True, False), ('off', False, True)):
            ref = solve(n, L, R, pw, pb)
            cf = closed_form(n, [tuple(l) for l in L], [tuple(r) for r in R], mode)
            for x in range(n):
                for s in 'LR':
                    r = ref.get((x, s), 'D')
                    if r == 'D': draws += 1
                    if r != cf[(x, s)]:
                        bad += 1
                        if bad < 5: print("MISMATCH", mode, n, L, R, x, s, r, cf[(x, s)])
    print(f"games={N} mismatches={bad} draw-states-seen={draws}")
