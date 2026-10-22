"""Retrograde solver for the sum  x (+) T  of a chess graph and a test game (K4).

State u = (c, t): chess node c (its stm is the side to move s) and test-game node t.
Moves of s from u:
  * every chess move c -> c'          (state (c', t)),
  * if s is not in check in c: every s-option t -> t' of T   (state (flip(c), t')),
    where flip(c) is the same placement with the other side to move.
Normal play: s with no move at all loses.  Infinite play is a draw.  The result is the least
fixed point (Definition 1.2 of kings/theory/LOOPY.md), computed by counting retrograde analysis.

Result codes (White's view): 0 = D, 1 = W (White wins), 2 = L (Black wins).
stalemate_draw=True gives the chess variant: a mover with no move who is NOT in check draws
(only meaningful with T = 0; used for check 1 against kpsolve).
"""

D, W, L = 0, 1, 2


def solve_product(cg, tg, stalemate_draw=False):
    n, nt = cg.n, tg.n
    stm, flip, incheck = cg.stm, cg.flip, cg.incheck
    soff, pred_off, pred = cg.succ_off, cg.pred_off, cg.pred
    tpred = (tg.lpred, tg.rpred)
    topts = (tg.lopts, tg.ropts)
    N = n * nt
    res = bytearray(N)
    cnt = bytearray(N)                  # number of moves not yet known to lose for the mover
    stack = []
    for c in range(n):
        s = stm[c]
        dchess = soff[c + 1] - soff[c]
        can_pass = flip[c] >= 0
        base = c * nt
        for t in range(nt):
            d = dchess + (len(topts[s][t]) if can_pass else 0)
            u = base + t
            if d == 0:
                if stalemate_draw and not incheck[c]:
                    continue                    # stalemate: draw (stays 0)
                res[u] = L if s == 0 else W     # mover loses
                stack.append(u)
            else:
                assert d < 256
                cnt[u] = d
    while stack:
        v = stack.pop()
        c2, t2 = divmod(v, nt)
        s = 1 - stm[c2]                         # mover of every predecessor of v
        win_val = s + 1                         # White's-view result when s wins (W=1 if s=0, L=2 if s=1)
        lose_val = 2 - s
        v_good = res[v] == win_val              # v is a win for s, so the predecessor wins
        # chess predecessors (c, t2), c -> c2
        for k in range(pred_off[c2], pred_off[c2 + 1]):
            u = pred[k] * nt + t2
            if res[u]:
                continue
            if v_good:
                res[u] = win_val
                stack.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0:
                    res[u] = lose_val
                    stack.append(u)
        # pass predecessors (flip(c2), t), t -s-> t2
        c = flip[c2]
        if c >= 0:
            base = c * nt
            for t in tpred[s][t2]:
                u = base + t
                if res[u]:
                    continue
                if v_good:
                    res[u] = win_val
                    stack.append(u)
                else:
                    cnt[u] -= 1
                    if cnt[u] == 0:
                        res[u] = lose_val
                        stack.append(u)
    return res


def pure(game):
    """Outcome of a pure CGT game: (result with White starting, result with Black starting)."""
    from graph import DummyGraph
    r = solve_product(DummyGraph, game)
    return 'DWL'[r[0 * game.n + game.start]], 'DWL'[r[1 * game.n + game.start]]
