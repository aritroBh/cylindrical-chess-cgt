"""K8: where is the spare move spent, and how does the win end?  Normal play and chess rule side by side.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/pv_stats.py flat:3x4 cyl:4x4 ...

For each rule (normal play: stalemate loses for both; chess: stalemate draws for both) this solves x (+) T for T = 0, +1, -1 with
a FIFO retrograde solver that also records the length of every decided state (plies), and reports

 1. strict-zugzwang nodes of the whole chess graph (the mover is not in check and does strictly worse than if the other side
    moved, at T = 0), split by whether the position still has a pawn, and the number of K+P vs K placements that contain one;
 2. (normal play only; explain.py does the chess rule, where forced passes need their own nodes) mask tests: x (+) +1 and x (+) -1 re-solved with the spare move allowed ONLY at some of those nodes, compared with the
    unrestricted result at every quiet placement (number of quiet placements that differ):
        'zugzwang nodes with a pawn'  /  'zugzwang nodes without a pawn'  /  'all zugzwang nodes'  /  'no spare move'
    Under normal play a spare move can never hurt, so 'all zugzwang nodes' must reproduce the full result exactly;
 3. for every position (placement with either side to move) where White wins with one spare move but not without it: the shortest
    winning line (the loser resists as long as possible), the type of the position at which White spends the spare move, and how the
    line ends (Black stalemated / Black checkmated).

The solver here is asserted to equal product.solve_product (normal play: stalemate_draw=False; chess: True) for n = -3..3.
Writes pvstats_<board>.json.
"""
import collections
import json
import os
import sys
import time
from collections import deque

import graph
import testgames as tg
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
RANK = {2: 0, 0: 1, 1: 2}
RULES = {'normal play': (False, False), 'chess rule': (True, True)}


def mover_value(code, s):
    return RANK[code] if s == 0 else 2 - RANK[code]


def solve_gen(cg, tgm, draws, mask=None):
    """res (0 = D, 1 = W, 2 = L, White's view) and dep (plies) of x (+) T; the T move is allowed at node c only if mask is None or mask[c]."""
    n, nt = cg.n, tgm.n
    stm, flip, incheck = cg.stm, cg.flip, cg.incheck
    soff, pred_off, pred = cg.succ_off, cg.pred_off, cg.pred
    tpred = (tgm.lpred, tgm.rpred)
    topts = (tgm.lopts, tgm.ropts)
    res = bytearray(n * nt)
    cnt = bytearray(n * nt)
    dep = [0] * (n * nt)
    q = deque()
    for c in range(n):
        s = stm[c]
        dchess = soff[c + 1] - soff[c]
        can = flip[c] >= 0 and (mask is None or mask[c])
        base = c * nt
        for t in range(nt):
            d = dchess + (len(topts[s][t]) if can else 0)
            u = base + t
            if d == 0:
                if draws[s] and not incheck[c]:
                    continue
                res[u] = 2 if s == 0 else 1
                q.append(u)
            else:
                cnt[u] = d
    while q:
        v = q.popleft()
        c2, t2 = divmod(v, nt)
        s = 1 - stm[c2]
        win_val, lose_val = s + 1, 2 - s
        good = res[v] == win_val
        dv = dep[v] + 1
        for k in range(pred_off[c2], pred_off[c2 + 1]):
            u = pred[k] * nt + t2
            if res[u]:
                continue
            if good:
                res[u] = win_val
                dep[u] = dv
                q.append(u)
            else:
                cnt[u] -= 1
                if cnt[u] == 0:
                    res[u] = lose_val
                    dep[u] = dv
                    q.append(u)
        c = flip[c2]
        if c >= 0 and (mask is None or mask[c]):
            base = c * nt
            for t in tpred[s][t2]:
                u = base + t
                if res[u]:
                    continue
                if good:
                    res[u] = win_val
                    dep[u] = dv
                    q.append(u)
                else:
                    cnt[u] -= 1
                    if cnt[u] == 0:
                        res[u] = lose_val
                        dep[u] = dv
                        q.append(u)
    return res, dep


def line_of(cg, T, res, dep, u, limit=100):
    nt = T.n
    line = [(u // nt, 'start')]
    while dep[u] > 0 and len(line) < limit:
        c, t = divmod(u, nt)
        s = cg.stm[c]
        nxt = None
        for k in range(cg.succ_off[c], cg.succ_off[c + 1]):
            v = cg.succ[k] * nt + t
            if res[v] == res[u] and dep[v] == dep[u] - 1:
                nxt = (v, 'move')
                break
        if nxt is None and cg.flip[c] >= 0:
            for t2 in T.opts(s)[t]:
                v = cg.flip[c] * nt + t2
                if res[v] == res[u] and dep[v] == dep[u] - 1:
                    nxt = (v, 'PASS')
                    break
        assert nxt is not None
        u = nxt[0]
        line.append((u // nt, nxt[1]))
    return line


def analyse(cg, rule, draws):
    kpk = set(cg.kpk)
    T0, TP, TM = tg.GAMES['0'], tg.integer(1), tg.integer(-1)
    full = {}
    for n in range(-3, 4):                       # regression against product.py
        T = tg.integer(n)
        r, d = solve_gen(cg, T, draws)
        assert r == solve_product(cg, T, stalemate_draw=draws[0]), (rule, n)
        full[n] = (r, d)
    res0 = full[0][0]
    haspawn = lambda c: bool(cg.pos[c][4])
    zug = [c for c in range(cg.n) if cg.flip[c] >= 0 and
           mover_value(res0[cg.flip[c]], cg.stm[c]) > mover_value(res0[c], cg.stm[c])]
    zset = set(zug)
    out = dict(
        zugzwang_nodes=dict(total=len(zug), with_pawn=sum(1 for c in zug if haspawn(c)),
                            without_pawn=sum(1 for c in zug if not haspawn(c)),
                            kpk_placements=sum(1 for cw, cb in cg.quiet_kpk if cw in zset)))
    masks = {
        'all zugzwang nodes': lambda c: c in zset,
        'zugzwang nodes with a pawn': lambda c: c in zset and haspawn(c),
        'zugzwang nodes without a pawn': lambda c: c in zset and not haspawn(c),
        'no spare move': lambda c: False,
    }
    mt = {}
    for sign, T, side in ((('+1', TP, 0), ('-1', TM, 1)) if not any(draws) else ()):    # chess rule: see explain.py (forced passes)
        rf = full[1 if sign == '+1' else -1][0]
        for name, f in masks.items():
            mask = bytearray(1 if (f(c) and cg.stm[c] == side) else 0 for c in range(cg.n))
            rm, _ = solve_gen(cg, T, draws, mask)
            diff = sum(1 for cw, cb in cg.quiet_kpk
                       if rm[cw * T.n + T.start] != rf[cw * T.n + T.start] or rm[cb * T.n + T.start] != rf[cb * T.n + T.start])
            mt.setdefault(name, {})['n=' + sign] = diff
    out['mask_tests_quiet_placements_that_differ_from_the_full_result'] = mt
    # principal variations: White wins with the spare move but not without it
    rP, dP = full[1]
    first = collections.Counter()
    end = collections.Counter()
    combo = collections.Counter()
    before = collections.Counter()
    examples = collections.defaultdict(list)
    states = 0
    for cw, cb in cg.quiet_kpk:
        for stm_name, c in (('W', cw), ('B', cb)):
            u = c * TP.n + TP.start
            if rP[u] != 1 or res0[c] == 1:
                continue
            states += 1
            line = line_of(cg, TP, rP, dP, u)
            passes = [i for i, (_, how) in enumerate(line) if how == 'PASS']
            if passes:
                pc = line[passes[0] - 1][0]
                ftype = ('zugzwang node' if pc in zset else 'other node') + (' with a pawn' if haspawn(pc) else ' without a pawn')
                before[passes[0] - 1] += 1
            else:
                ftype = 'no pass in the longest line'
            last = line[-1][0]
            assert cg.stm[last] == 1
            etype = ('Black checkmated' if cg.incheck[last] else 'Black stalemated') if \
                cg.succ_off[last + 1] == cg.succ_off[last] else 'Black captured/other'
            first[ftype] += 1
            end[etype] += 1
            combo[(ftype, etype)] += 1
            key = (ftype, etype)
            if len(examples[key]) < 2:
                examples[key].append(dict(
                    placement=cg.placement(cw), start='%s to move' % stm_name, plies=dP[u],
                    line=[('PASS ' if how == 'PASS' else '') + cg.kp_line(nc) for nc, how in line]))
    out['spare_move_wins'] = dict(
        states=states, where_the_spare_move_is_spent=dict(first), how_the_win_ends=dict(end),
        plies_before_the_pass=dict(sorted(before.items())),
        examples={'%s / %s' % k: v for k, v in examples.items()})
    return out


def run(board):
    t0 = time.time()
    tag = board.replace(':', '_')
    cg = graph.ChessGraph(board)
    res = dict(label='COMPUTED-1', board=board, quiet=len(cg.quiet_kpk))
    for rule, draws in RULES.items():
        res[rule] = analyse(cg, rule, draws)
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(HERE, 'pvstats_%s.json' % tag), 'w'), indent=1, ensure_ascii=False)
    short = {k: ({kk: {a: b for a, b in vv.items() if a != 'examples'} if isinstance(vv, dict) else vv for kk, vv in v.items()}
                 if isinstance(v, dict) else v) for k, v in res.items()}
    print(json.dumps(short, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        run(b)
