"""Verifier A, module 3: the product x (+) T and its least-fixed-point result (own retrograde code).

State (x, t) with x a chess-graph node (it carries the side to move s) and t a node of the game T.
  moves of s:  chess move x -> y (state (y, t));  T move t -> t' in s-options (state (flip x, t'))
               allowed only if s is not in check in x.
  normal play: no move at all = the mover loses.   Infinite play = draw.
Left (White) wins at a state iff it is in the least set WL with
   mover = White:  some successor in WL;   mover = Black: every successor in WL (none counts).
Right (Black) wins symmetrically (set WR).  Result 'W' if in WL, 'L' if in WR, else 'D'.
"""
from collections import deque


def lfp(nstate, stm, succ_count, preds, player):
    """Least fixed point of 'player wins in finitely many moves'.  Returns a bytearray."""
    win = bytearray(nstate)
    cnt = list(succ_count)
    q = deque()
    for u in range(nstate):
        if stm[u] != player and cnt[u] == 0:
            win[u] = 1
            q.append(u)
    while q:
        u = q.popleft()
        for p in preds(u):
            if win[p]:
                continue
            if stm[p] == player:
                win[p] = 1
                q.append(p)
            else:
                cnt[p] -= 1
                if cnt[p] == 0:
                    win[p] = 1
                    q.append(p)
    return win


def solve(G, game):
    """Solve G (+) game.  Returns res with res[x*ng + t] in 'W','D','L'."""
    lo, ro = game
    ng = len(lo)
    n = G.n
    nst = n * ng
    stm = [G.stm[st // ng] for st in range(nst)]
    opts = (lo, ro)
    # predecessor option lists: tpred[side][t2] = [t with t2 in options(side, t)]
    tpred = ([[] for _ in range(ng)], [[] for _ in range(ng)])
    for side in (0, 1):
        for t in range(ng):
            for t2 in opts[side][t]:
                tpred[side][t2].append(t)
    succ_count = [0] * nst
    for x in range(n):
        s = G.stm[x]
        base = len(G.succ[x])
        for t in range(ng):
            c = base
            if not G.incheck[x]:
                c += len(opts[s][t])
            succ_count[x * ng + t] = c

    def preds(u):
        y, t = divmod(u, ng)
        for x in G.pred[y]:
            yield x * ng + t
        x = G.flip_pred[y]
        if x >= 0:                       # x -> flip x = y by a T move of x's mover
            s = G.stm[x]
            for t0 in tpred[s][t]:
                yield x * ng + t0

    wl = lfp(nst, stm, succ_count, preds, 0)
    wr = lfp(nst, stm, succ_count, preds, 1)
    res = []
    for u in range(nst):
        if wl[u] and wr[u]:
            raise AssertionError('both sides win at %d' % u)
        res.append('W' if wl[u] else 'L' if wr[u] else 'D')
    return res


class PureGraph:
    """A chess-free graph: two nodes, 'White to move' and 'Black to move', no chess moves."""
    n = 2
    stm = [0, 1]
    succ = [[], []]
    incheck = [False, False]
    flip = [1, 0]
    flip_pred = [1, 0]
    pred = [[], []]


def solve_pure(game):
    """Results of the pure game: returns (White starts, Black starts) characters."""
    res = solve(PureGraph, game)
    ng = len(game[0])
    return res[0 * ng + 0], res[1 * ng + 0]
