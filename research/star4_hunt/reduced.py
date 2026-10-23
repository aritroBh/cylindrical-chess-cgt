"""Reduced (safe-move) game of a pawn position: delete every move after which the opponent has an immediate terminal win."""
import sys
from functools import lru_cache
from cylcgt import pawns, cgt

def make_board(files, wrap=False):
    return pawns.Board(files, 8, wrap, True)

def decided(board, pos):
    wp, bp = pawns.passed(board, pos, 'W'), pawns.passed(board, pos, 'B')
    return wp, bp

def opp(s): return 'B' if s == 'W' else 'W'

def child_status(board, pos, mover):
    """returns ('win', mover) if the move creates a decisive position for someone, else None"""
    wp, bp = decided(board, pos)
    if wp and bp:
        # race rule
        other = opp(mover)
        winner = other if pawns.promote_distance(board, pos, other) <= pawns.promote_distance(board, pos, mover) else mover
        return winner
    if wp: return 'W'
    if bp: return 'B'
    return None

def reduced_graph(board, pos, maxnodes=200000):
    nodes = {}
    order = []
    def key(p): return (p.white, p.black, p.ep)
    stack = [pos]
    nodes[key(pos)] = None
    edges = {}
    while stack:
        p = stack.pop()
        k = key(p)
        res = {}
        for side in 'WB':
            lp = Pos_noep(p, side)
            outs = []
            for c in pawns.moves(board, lp, side):
                st = child_status(board, c, side)
                if st is not None:
                    outs.append(('T', st))
                    continue
                # does the opponent have an immediate terminal win from c?
                bad = False
                lc = Pos_noep(c, opp(side))
                for c2 in pawns.moves(board, lc, opp(side)):
                    st2 = child_status(board, c2, opp(side))
                    if st2 == opp(side):
                        bad = True; break
                if bad:
                    outs.append(('P', c))   # poisoned
                else:
                    outs.append(('S', c))
            res[side] = outs
        edges[k] = res
        for side in 'WB':
            for kind, c in res[side]:
                if kind == 'S' and key(c) not in nodes:
                    nodes[key(c)] = None
                    stack.append(c)
        if len(nodes) > maxnodes:
            raise RuntimeError('too many nodes')
    return edges

def Pos_noep(p, side):
    # the e.p. right survives only for the opponent's immediate move
    if p.ep and p.ep[2] != side:
        return pawns.Pos(p.white, p.black, None)
    return p

if __name__ == '__main__':
    files = int(sys.argv[1]); text = sys.argv[2]
    board = make_board(files)
    pos = pawns.Pos.parse(text)
    e = reduced_graph(board, pos)
    print('nodes', len(e))
    nS = sum(1 for k in e for s in 'WB' for t, c in e[k][s] if t == 'S')
    nP = sum(1 for k in e for s in 'WB' for t, c in e[k][s] if t == 'P')
    nT = sum(1 for k in e for s in 'WB' for t, c in e[k][s] if t == 'T')
    print('safe edges', nS, 'poisoned', nP, 'terminal', nT)
