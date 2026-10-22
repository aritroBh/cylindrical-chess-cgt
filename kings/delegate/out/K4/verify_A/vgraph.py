"""Verifier A, module 1: the chess move graph of a board (adjacency lists over positions).

Nodes are positions (stm, wk, bk, offs, wp, bp, ep) from kings/ref/solve.py.  The node set is the
closure, from every quiet placement with either side to move, under the chess moves and under
"flip the side to move" (a move in the test game T leaves x alone and passes the turn).
"""
import sys
from collections import deque
sys.setrecursionlimit(100000)
from kings.ref.solve import make_solver, CAPPED


class ChessGraph:
    pass


def quiet_placements(solver):
    """All legal placements K P k with neither king in check; returns [(name, wk, p, bk)]."""
    g = solver.g
    out = []
    for wk in range(g.N):
        for bk in range(g.N):
            if wk == bk or (g.king_mask[wk] >> bk) & 1:
                continue
            for p in range(g.N):
                if p in (wk, bk) or g.rank[p] in (0, g.H - 1):
                    continue
                pos = (0, wk, bk, (), 1 << p, 0, -1)
                if solver.in_check(pos, 0) or solver.in_check(pos, 1):
                    continue
                name = 'K%s P%s k%s' % (g.sqname(wk), g.sqname(p), g.sqname(bk))
                out.append((name, wk, p, bk))
    return out


def flip(pos):
    stm, wk, bk, offs, wp, bp, ep = pos
    return (1 - stm, wk, bk, offs, wp, bp, -1)


def build(board, allkpk=False):
    """Build the graph for e.g. 'flat:3x4'.  Returns a ChessGraph."""
    s = make_solver(board=board, ep='on', promote='QRBN', cap=1)
    G = ChessGraph()
    G.board, G.solver = board, s
    G.places = quiet_placements(s)
    index, nodes = {}, []

    def add(pos):
        i = index.get(pos)
        if i is None:
            i = index[pos] = len(nodes)
            nodes.append(pos)
            todo.append(i)
        return i

    todo = deque()
    for _, wk, p, bk in G.places:
        for stm in (0, 1):
            add((stm, wk, bk, (), 1 << p, 0, -1))
    if allkpk:      # also seed every legal KPK position (as kpsolve would be asked about them)
        g = s.g
        for wk in range(g.N):
            for bk in range(g.N):
                if wk == bk or (g.king_mask[wk] >> bk) & 1:
                    continue
                for p in range(g.N):
                    if p in (wk, bk) or g.rank[p] in (0, g.H - 1):
                        continue
                    for stm in (0, 1):
                        pos = (stm, wk, bk, (), 1 << p, 0, -1)
                        if not s.in_check(pos, 1 - stm):
                            add(pos)
    succ, incheck, flipof = {}, {}, {}
    while todo:
        i = todo.popleft()
        pos = nodes[i]
        assert pos[6] == -1 and pos[5] == 0, 'unexpected black pawn / ep'
        nq, quiet, exits = s.moves(pos, full=True)
        assert nq == len(quiet)
        outs = set()
        for q in quiet:
            outs.add(add(q))
        for tag, y in exits:
            assert tag != CAPPED, 'capped promotion with cap 1'
            outs.add(add(y))
        succ[i] = outs
        incheck[i] = bool(s.in_check(pos))
        if not incheck[i]:
            flipof[i] = add(flip(pos))
    n = len(nodes)
    G.pos, G.index, G.n = nodes, index, n
    G.succ = [sorted(succ[i]) for i in range(n)]
    G.incheck = [incheck[i] for i in range(n)]
    G.stm = [nodes[i][0] for i in range(n)]
    # flip[i] = node with the turn passed, or -1 when i's mover is in check (T moves forbidden)
    G.flip = [flipof.get(i, -1) for i in range(n)]
    for i in range(n):          # flip must exist for the target as well: involution check
        j = G.flip[i]
        if j >= 0:
            assert G.pos[j][1:6] == G.pos[i][1:6] and G.pos[j][0] != G.pos[i][0]
    G.pred = [[] for _ in range(n)]
    for i in range(n):
        for j in G.succ[i]:
            G.pred[j].append(i)
    # in the product, a T move from x lands on flip[x]; its predecessor is x = flip^-1[y].
    G.flip_pred = [-1] * n
    for i in range(n):
        j = G.flip[i]
        if j >= 0:
            assert G.flip_pred[j] == -1
            G.flip_pred[j] = i
    G.nodecount_kpk = sum(1 for p in nodes if (p[4] or p[5]))
    return G


if __name__ == '__main__':
    G = build(sys.argv[1])
    print(G.board, 'places', len(G.places), 'nodes', G.n, 'edges', sum(map(len, G.succ)),
          'with pawn', G.nodecount_kpk)
