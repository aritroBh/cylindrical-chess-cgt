"""K8 ablation: which part of the chess stalemate rule produces the parity tails (and the n = +-1 effects)?

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/ablation.py flat:3x4 cyl:4x4 ...

Rules compared on the same placements (all with checkmate = loss, in-check moves in T illegal, infinite play = draw):
  normal  stalemate loses                                  (K4/K6; product.solve_product default)
  chess   the mover has no move IN THE WHOLE SUM and is not in check -> draw   (product.solve_product, stalemate_draw=True)
  blind   the mover has no CHESS move and is not in check -> draw, even if T still offers a move
          ("spare-blind stalemate": a spare move can no longer cancel a stalemate, so no pass is ever forced)
`blind` is not a rule of the task; it is an experiment.  solve() below is product.solve_product with one extra
mode; with mode 'chess' it must (and is asserted to) give the same result as product.solve_product for n = -3..3.
The `chess` and `normal` counts are read from tempo_detail_<board>.json written by chess_scan.py.
Writes ablation_<board>.json.
"""
import collections
import json
import os
import sys

import graph
import testgames as tg
from names import chess_detail_path
from product import solve_product, D, W, L

HERE = os.path.dirname(os.path.abspath(__file__))
FINITE = tg.TESTS[:11]
RANGE = list(range(-10, 11))
EXTRA = list(range(-20, -10)) + list(range(11, 21))


def solve(cg, tgm, mode):
    n, nt = cg.n, tgm.n
    stm, flip, incheck = cg.stm, cg.flip, cg.incheck
    soff, pred_off, pred = cg.succ_off, cg.pred_off, cg.pred
    tpred = (tgm.lpred, tgm.rpred)
    topts = (tgm.lopts, tgm.ropts)
    res = bytearray(n * nt)
    cnt = bytearray(n * nt)
    stack = []
    for c in range(n):
        s = stm[c]
        dchess = soff[c + 1] - soff[c]
        can_pass = flip[c] >= 0
        base = c * nt
        for t in range(nt):
            d = dchess + (len(topts[s][t]) if can_pass else 0)
            u = base + t
            if mode == 'blind' and dchess == 0 and not incheck[c]:
                cnt[u] = 255                    # stalemate: draw whatever T offers; never counted down to 0
                continue
            if d == 0:
                if mode == 'chess' and not incheck[c]:
                    continue                    # stalemate in the whole sum: draw
                res[u] = L if s == 0 else W
                stack.append(u)
            else:
                cnt[u] = d
    while stack:
        v = stack.pop()
        c2, t2 = divmod(v, nt)
        s = 1 - stm[c2]
        win_val, lose_val = s + 1, 2 - s
        v_good = res[v] == win_val
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


def tail_kind(seq):
    if len(set(seq)) == 1:
        return 'constant'
    if all(seq[i] == seq[i + 2] for i in range(len(seq) - 2)):
        return 'period2'
    return 'other'


def run(board):
    tag = board.replace(':', '_')
    cg = graph.ChessGraph(board)
    for n in range(-3, 4):                       # regression test of this copy against product.py
        T = tg.integer(n)
        assert solve(cg, T, 'chess') == solve_product(cg, T, stalemate_draw=True), n
        assert solve(cg, T, 'normal') == solve_product(cg, T), n
    quiet = cg.quiet_kpk
    fin = {c: [] for c in quiet}
    ns = {c: {} for c in quiet}
    for name in FINITE:
        T = tg.GAMES[name]
        r = solve(cg, T, 'blind')
        for c in quiet:
            fin[c].append('DWL'[r[c[0] * T.n + T.start]] + 'DWL'[r[c[1] * T.n + T.start]])
    for n in RANGE + EXTRA:
        T = tg.integer(n)
        r = solve(cg, T, 'blind')
        for c in quiet:
            ns[c][n] = 'DWL'[r[c[0] * T.n + T.start]] + 'DWL'[r[c[1] * T.n + T.start]]
    cnt = collections.Counter()
    thr = collections.Counter()
    ex = []
    chess_rows = {}
    with open(os.path.join(HERE, 'chess_tempo_%s.jsonl' % tag)) as f:
        for line in f:
            r = json.loads(line)
            chess_rows[r['placement']] = r
    for c in sorted(quiet, key=lambda p: cg.placement(p[0])):
        pl = cg.placement(c[0])
        prof = [ns[c][n] for n in RANGE]
        sens = len(set(fin[c])) > 1 or len(set(prof)) > 1
        pm1 = ns[c][1] != ns[c][0] or ns[c][-1] != ns[c][0]
        neg = tail_kind([ns[c][n] for n in range(-20, -1)])
        pos = tail_kind([ns[c][n] for n in range(2, 21)])
        thr.update(n for n, a, b in zip(RANGE, prof, prof[1:]) if a != b)
        cr = chess_rows[pl]
        cnt['quiet'] += 1
        cnt['blind_sensitive'] += sens
        cnt['blind_pm1'] += pm1
        cnt['blind_neg_' + neg] += 1
        cnt['blind_pos_' + pos] += 1
        cnt['blind_mutual_and_pm1'] += pm1 and cr['mutual_zugzwang']
        cnt['mutual'] += cr['mutual_zugzwang']
        cnt['chess_sensitive'] += cr['chess_sensitive']
        cnt['both_sensitive'] += sens and cr['chess_sensitive']
        cnt['chess_only'] += cr['chess_sensitive'] and not sens
        cnt['blind_only'] += sens and not cr['chess_sensitive']
        if cr['chess_sensitive'] and not sens and len(ex) < 5:
            ex.append(dict(placement=pl, kpsolve=cr['kpsolve'], chess_n=cr['chess_n'], blind_n=''.join(ns[c][n] for n in RANGE)))
    d = json.load(open(chess_detail_path(board)))
    out = dict(label='COMPUTED-1', board=board, quiet=cnt['quiet'],
               chess=dict(tempo_sensitive=d['tempo_sensitive'], sensitive_at_pm1=d['sensitive_at_pm1'],
                          tails_n_minus20_to_minus2=d['tails_n_minus20_to_minus2'],
                          mutual_zugzwangs=d['mutual_zugzwangs']),
               normal=dict(tempo_sensitive=d['normal_rule_same_placements']['tempo_sensitive']),
               spare_blind_stalemate=dict(
                   tempo_sensitive=cnt['blind_sensitive'], sensitive_at_pm1=cnt['blind_pm1'],
                   thresholds={str(k): v for k, v in sorted(thr.items())},
                   tails_n_minus20_to_minus2={k: cnt['blind_neg_' + k] for k in ('constant', 'period2', 'other')},
                   tails_n_2_to_20={k: cnt['blind_pos_' + k] for k in ('constant', 'period2', 'other')},
                   mutual_zugzwangs_also_sensitive_at_pm1=cnt['blind_mutual_and_pm1'],
                   sensitive_under_both_chess_and_blind=cnt['both_sensitive'],
                   sensitive_under_chess_only=cnt['chess_only'], sensitive_under_blind_only=cnt['blind_only']),
               examples_chess_only=ex)
    json.dump(out, open(os.path.join(HERE, 'ablation_%s.json' % tag), 'w'), indent=1)
    print(json.dumps(out), flush=True)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        run(b)
