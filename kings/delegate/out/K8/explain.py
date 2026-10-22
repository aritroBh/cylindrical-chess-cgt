"""K8 Task 2 follow-up: where is a spare move actually spent?  (chess stalemate rule)

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/explain.py flat:3x4 cyl:5x6 ...

Question.  A mutual zugzwang is sensitive to one spare move at its own placement (proof in REPORT.md).  Most placements that are
sensitive at n = +-1 are not zugzwangs themselves.  Why are they sensitive?

Nodes of the chess graph (any position, also with officers) are sorted into
  * zugzwang node : the mover is not in check, has a chess move, and does strictly worse than if the other side moved
                    (T = 0, chess rule, from the product solver, which check 1 compares with kpsolve);
  * forced-pass node : the mover is not in check and has no chess move, so with a spare move he MUST pass (without one it is
                    a stalemate, a draw);
  * other node    : the mover is not in check and prefers to keep the move or is indifferent (a pass can only help or be forced
                    at the other two kinds).
Test 1 (mask).  Solve x (+) 1 (White's one spare move) with the pass allowed ONLY at White's zugzwang and forced-pass nodes, and x (+) -1
with the pass allowed only at Black's.  Compare with the unrestricted solutions at every node.  Equality means that a spare move
never has to be spent anywhere else.  (It must hold because a pass at an 'other' node leads to a value that is not better for
the mover than the node's own value; the test checks this and the implementation.)
Test 2 (principal variation).  For every placement that is sensitive at n = +1 because White wins with the spare move but not without
it, a breadth-first retrograde solution gives the winning line of shortest length (loser delays as long as possible); the first
pass in that line is classified.  Writes explain_<board>.json with counts and example lines.

The solver here (solve_depth) is product.solve_product with a FIFO queue, depth bookkeeping and an optional pass mask; with no mask
it is asserted to equal product.solve_product for T = 0, +1, -1.
"""
import collections
import json
import os
import sys
import time
from collections import deque

import graph
import testgames as tg
from ablation import solve as ablation_solve
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
RANK = {2: 0, 0: 1, 1: 2}                      # result code (D = 0, W = 1, L = 2) -> rank in White's view, L < D < W


def mover_value(code, s):
    return RANK[code] if s == 0 else 2 - RANK[code]


def solve_depth(cg, tgm, mask=None, blind=False):
    """Chess rule (stalemate draws).  mask: None or a bytearray over chess nodes; the test-game move is allowed at node c only
    if mask[c].  blind=True: a mover with no CHESS move who is not in check may still spend a spare move if that wins, but is never
    forced to (so stalemate stays available as a draw; this is ablation.py's 'blind' rule).  Returns (res, dep): res as in
    product.solve_product, dep = plies to the end for decided states."""
    n, nt = cg.n, tgm.n
    stm, flip, incheck = cg.stm, cg.flip, cg.incheck
    soff, pred_off, pred = cg.succ_off, cg.pred_off, cg.pred
    tpred = (tgm.lpred, tgm.rpred)
    topts = (tgm.lopts, tgm.ropts)
    N = n * nt
    res = bytearray(N)
    cnt = bytearray(N)
    dep = [0] * N
    q = deque()
    for c in range(n):
        s = stm[c]
        dchess = soff[c + 1] - soff[c]
        can_pass = flip[c] >= 0 and (mask is None or mask[c])
        base = c * nt
        for t in range(nt):
            d = dchess + (len(topts[s][t]) if can_pass else 0)
            u = base + t
            if blind and dchess == 0 and not incheck[c]:
                cnt[u] = 255                    # stalemate stays a draw; a pass is optional
                continue
            if d == 0:
                if not incheck[c]:
                    continue                    # stalemate: draw
                res[u] = 2 if s == 0 else 1
                q.append(u)
            else:
                cnt[u] = d
    while q:
        v = q.popleft()
        c2, t2 = divmod(v, nt)
        s = 1 - stm[c2]
        win_val, lose_val = s + 1, 2 - s
        v_good = res[v] == win_val
        dv = dep[v] + 1
        for k in range(pred_off[c2], pred_off[c2 + 1]):
            u = pred[k] * nt + t2
            if res[u]:
                continue
            if v_good:
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
                if v_good:
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


def node_kinds(cg, res0, blind=False):
    """bytearray: 0 other, 1 zugzwang node (the mover strictly prefers the other side to move; with blind=True this includes
    nodes with no chess move), 2 forced-pass node (no chess move, not in check; chess rule only).  Only nodes whose mover is not in check."""
    kind = bytearray(cg.n)
    for c in range(cg.n):
        f = cg.flip[c]
        if f < 0:
            continue
        s = cg.stm[c]
        stalemated = cg.succ_off[c + 1] == cg.succ_off[c]
        if stalemated and not blind:
            kind[c] = 2
        elif mover_value(res0[f], s) > mover_value(res0[c], s):
            kind[c] = 1
    return kind


def principal_variation(cg, T, res, dep, u, mask=None, limit=80):
    """Shortest win for the winner, longest resistance for the loser.  Returns [(chess node, test node, how the state was reached)]."""
    nt = T.n
    line = [(u // nt, u % nt, 'start')]
    while dep[u] > 0 and len(line) < limit:
        c, t = divmod(u, nt)
        s = cg.stm[c]
        nxt = None
        for k in range(cg.succ_off[c], cg.succ_off[c + 1]):
            v = cg.succ[k] * nt + t
            if res[v] == res[u] and dep[v] == dep[u] - 1:
                nxt = (v, 'move')
                break
        if nxt is None and cg.flip[c] >= 0 and (mask is None or mask[c]):
            for t2 in T.opts(s)[t]:
                v = cg.flip[c] * nt + t2
                if res[v] == res[u] and dep[v] == dep[u] - 1:
                    nxt = (v, 'PASS')
                    break
        assert nxt is not None, 'no principal-variation successor'
        u = nxt[0]
        line.append((u // nt, u % nt, nxt[1]))
    return line


def explain(board):
    t0 = time.time()
    tag = board.replace(':', '_')
    cg = graph.ChessGraph(board)
    T0, TP, TM = tg.GAMES['0'], tg.integer(1), tg.integer(-1)
    res0 = solve_product(cg, T0, stalemate_draw=True)
    kind = node_kinds(cg, res0)
    # regression: the FIFO solver without a mask is the same function as product.solve_product
    full = {}
    for name, T in (('0', T0), ('+1', TP), ('-1', TM)):
        r, d = solve_depth(cg, T)
        assert r == solve_product(cg, T, stalemate_draw=True), 'solve_depth differs from product.solve_product at ' + name
        full[name] = (r, d)
    for n in range(-3, 4):                       # the blind option equals ablation.py's independent copy
        T = tg.integer(n)
        assert solve_depth(cg, T, None, True)[0] == ablation_solve(cg, T, 'blind'), 'blind rule differs from ablation.py at n=%d' % n
    out = dict(label='COMPUTED-1', board=board, nodes=cg.n, quiet=len(cg.quiet_kpk))
    kpk = set(cg.kpk)
    out['critical_nodes'] = dict(
        zugzwang_white=sum(1 for c in range(cg.n) if kind[c] == 1 and cg.stm[c] == 0),
        zugzwang_black=sum(1 for c in range(cg.n) if kind[c] == 1 and cg.stm[c] == 1),
        zugzwang_white_that_are_kpk=sum(1 for c in range(cg.n) if kind[c] == 1 and cg.stm[c] == 0 and c in kpk),
        zugzwang_black_that_are_kpk=sum(1 for c in range(cg.n) if kind[c] == 1 and cg.stm[c] == 1 and c in kpk),
        forced_pass_white=sum(1 for c in range(cg.n) if kind[c] == 2 and cg.stm[c] == 0),
        forced_pass_black=sum(1 for c in range(cg.n) if kind[c] == 2 and cg.stm[c] == 1))
    # Test 1, chess rule (forced passes) and blind rule (optional passes)
    for rule, blind in (('chess rule', False), ('optional-pass rule', True)):
        kd = node_kinds(cg, res0, blind)
        for name, T, side in (('+1', TP, 0), ('-1', TM, 1)):
            mask = bytearray(1 if (kd[c] and cg.stm[c] == side) else 0 for c in range(cg.n))
            rf = full[name][0] if not blind else solve_depth(cg, T, None, True)[0]
            rm, _ = solve_depth(cg, T, mask, blind)
            diff_nodes = sum(1 for u in range(len(rf)) if rf[u] != rm[u])
            diff_quiet = sum(1 for cw, cb in cg.quiet_kpk
                             if rf[cw * T.n + T.start] != rm[cw * T.n + T.start] or rf[cb * T.n + T.start] != rm[cb * T.n + T.start])
            out['mask_test %s n=%s' % (rule, name)] = dict(
                pass_allowed_at_nodes=int(sum(mask)), states_that_differ=diff_nodes, quiet_placements_that_differ=diff_quiet)
    # Test 2
    rP, dP = full['+1']
    r0 = res0
    cats = collections.Counter()
    first_pass_dist = collections.Counter()
    examples = collections.defaultdict(list)
    pm1_gain = 0
    for cw, cb in cg.quiet_kpk:
        w0, b0 = r0[cw], r0[cb]
        for stm_name, c, r_n0 in (('W', cw, w0), ('B', cb, b0)):
            u = c * TP.n + TP.start
            if rP[u] == 1 and r_n0 != 1:            # White wins with the spare move but not without it
                line = principal_variation(cg, TP, rP, dP, u)
                npass = [i for i, (_, _, how) in enumerate(line) if how == 'PASS']
                assert len(npass) <= 1, 'the spare move is used at most once'
                pl = cg.placement(cw)
                if not npass:
                    # the longest-resisting line wins without the pass; another Black reply needs it
                    typ, i = 'no pass in the longest line', len(line)
                else:
                    i = npass[0]
                    pc = line[i - 1][0]              # node from which White passes
                    k = int(kind[pc])
                    typ = ('zugzwang' if k == 1 else 'forced-pass' if k == 2 else 'other') + \
                          ('/KPK' if pc in kpk else '/officer')
                    first_pass_dist[i - 1] += 1
                cats[typ] += 1
                if len(examples[typ]) < 3 and (cw, cb) not in [(e['_c'], e['_cb']) for e in examples[typ]]:
                    examples[typ].append(dict(
                        _c=cw, _cb=cb, placement=pl, start='%s to move' % stm_name, kpsolve=''.join('DWL'[x] for x in (r0[cw], r0[cb])),
                        plies_to_win_with_spare=dP[u], plies_before_the_pass=(i - 1 if npass else None),
                        line=['%s%s' % ('PASS ' if how == 'PASS' else '', cg.kp_line(nc)) for nc, nt_, how in line[:i + 3]]))
    for ex in examples.values():
        for e in ex:
            del e['_c'], e['_cb']
    out['spare_move_for_White_turns_non_win_into_win'] = dict(
        placements_states=sum(cats.values()), first_pass_node_type=dict(cats),
        plies_before_the_pass=dict(sorted(first_pass_dist.items())), examples={k: v for k, v in examples.items()})
    out['seconds'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(HERE, 'explain_%s.json' % tag), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != 'spare_move_for_White_turns_non_win_into_win'}), flush=True)
    s = out['spare_move_for_White_turns_non_win_into_win']
    print(json.dumps({k: v for k, v in s.items() if k != 'examples'}), flush=True)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        explain(b)
