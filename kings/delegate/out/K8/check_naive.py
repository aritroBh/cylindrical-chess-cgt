"""Internal cross-check for K8: a second, naive solver for x (+) n against product.solve_product.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/check_naive.py flat:3x4 cyl:4x4 ...

solve_product uses counting retrograde analysis on the product with an explicit test-game graph (testgames.integer).
This script does not use testgames or product at all.  A state is (chess node, White's spare moves, Black's spare
moves) and it is solved by repeated sweeps to the least fixed point:
    mover wins    if some move reaches a state that is lost for the next mover;
    mover loses   if every move reaches a state that is won for the next mover, or has no move
                  (under the chess rule: has no move, is not in check -> draw instead);
    otherwise draw (infinite play).
A spare move is a move that keeps the placement and gives the move to the other side; it needs a mover who is
not in check.  Compares x (+) n for n = -4..4 at every quiet placement, under both rules, with solve_product.
It uses the same chess graph (graph.py), which check 1 compares with kpsolve.
"""
import sys
import time

import graph
import testgames as tg
from product import solve_product


def naive(cg, ws, bs, stalemate_draw):
    """Returns res[c] (White's view: 0 = D, 1 = W, 2 = L) for every chess node, with ws/bs spare moves each side."""
    n = cg.n
    S = [(a, b) for a in range(ws + 1) for b in range(bs + 1)]
    idx = {s: i for i, s in enumerate(S)}
    win = [bytearray(n) for _ in S]        # win[state][c]: the mover of c wins
    lose = [bytearray(n) for _ in S]
    # successors of (c, state): chess moves and, if allowed, the spare move
    def succs(c, a, b):
        out = [(m, idx[(a, b)]) for m in cg.succ[cg.succ_off[c]:cg.succ_off[c + 1]]]
        if not cg.incheck[c]:
            if cg.stm[c] == 0 and a > 0:
                out.append((cg.flip[c], idx[(a - 1, b)]))
            if cg.stm[c] == 1 and b > 0:
                out.append((cg.flip[c], idx[(a, b - 1)]))
        return out
    moves = {(c, i): succs(c, a, b) for i, (a, b) in enumerate(S) for c in range(n)}
    changed = True
    while changed:
        changed = False
        for i in range(len(S)):
            for c in range(n):
                if win[i][c] or lose[i][c]:
                    continue
                mv = moves[(c, i)]
                if not mv:
                    if stalemate_draw and not cg.incheck[c]:
                        continue
                    lose[i][c] = 1
                    changed = True
                    continue
                if any(lose[j][m] for m, j in mv):
                    win[i][c] = 1
                    changed = True
                elif all(win[j][m] for m, j in mv):
                    lose[i][c] = 1
                    changed = True
    top = idx[(ws, bs)]
    res = bytearray(n)
    for c in range(n):
        mover = cg.stm[c]
        if win[top][c]:
            res[c] = 1 if mover == 0 else 2
        elif lose[top][c]:
            res[c] = 2 if mover == 0 else 1
    return res


def main(boards):
    for board in boards:
        t0 = time.time()
        cg = graph.ChessGraph(board)
        bad = checked = 0
        for sd in (True, False):
            for n in range(-4, 5):
                T = tg.integer(n)
                a = solve_product(cg, T, stalemate_draw=sd)
                b = naive(cg, max(n, 0), max(-n, 0), sd)
                for c in range(cg.n):
                    checked += 1
                    if a[c * T.n + T.start] != b[c]:
                        bad += 1
                        if bad <= 5:
                            print('DIFF', board, sd, n, cg.kp_line(c), a[c * T.n + T.start], b[c])
        print('%s: %d node results compared (chess + normal rule, n = -4..4, all nodes), %d differences, %.0fs' %
              (board, checked, bad, time.time() - t0), flush=True)
        if bad:
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
