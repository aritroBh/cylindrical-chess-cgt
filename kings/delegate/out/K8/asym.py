"""K8 causal test: which side's stalemate rule creates, and which removes, tempo-sensitivity?

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/asym.py flat:3x4 cyl:5x6 ...

Four stalemate rules for the sum x (+) T (everything else as in K4/K6: a move in T is illegal while the mover is in check, a
side in check with no move loses, infinite play is a draw).  Stalemate = the mover has no legal move in the whole sum and is not in check.
    WlBl   both stalemates lose            = normal play (K4/K6, product.solve_product default)
    WdBd   both stalemates draw            = the chess rule (product.solve_product(..., stalemate_draw=True))
    WdBl   only White's stalemate draws, Black's loses
    WlBd   only White's stalemate loses, Black's draws
For each rule: the number of tempo-sensitive placements (K6 definition: the (White starts, Black starts) result is not constant over the
11 finite test games and over x (+) n, n = -10..10), the number sensitive at n = +1 or -1, the thresholds, and the parity tails
(n = -10..-2 and n = 2..10; period 2 = the result alternates with the parity of n).  The two symmetric rules are asserted to reproduce product.solve_product, and their counts to
reproduce chess_scan.py's per-placement file.  Writes asym_<board>.json.
"""
import collections
import json
import os
import sys
import time

import graph
import testgames as tg
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
FINITE = tg.TESTS[:11]
RANGE = list(range(-10, 11))
Z0 = RANGE.index(0)
RULES = [('WlBl', (False, False)), ('WdBd', (True, True)), ('WdBl', (True, False)), ('WlBd', (False, True))]


def solve_rule(cg, tgm, white_draws, black_draws):
    """product.solve_product with the stalemate result chosen per side."""
    n, nt = cg.n, tgm.n
    stm, flip, incheck = cg.stm, cg.flip, cg.incheck
    soff, pred_off, pred = cg.succ_off, cg.pred_off, cg.pred
    tpred = (tgm.lpred, tgm.rpred)
    topts = (tgm.lopts, tgm.ropts)
    draws = (white_draws, black_draws)
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
            if d == 0:
                if draws[s] and not incheck[c]:
                    continue
                res[u] = 2 if s == 0 else 1
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


def scan(cg, wd, bd):
    quiet = cg.quiet_kpk
    fin = {c: [] for c in quiet}
    prof = {c: {} for c in quiet}
    cache = {}
    for name in FINITE:
        T = tg.GAMES[name]
        r = cache[name] = solve_rule(cg, T, wd, bd)
        for c in quiet:
            fin[c].append('DWL'[r[c[0] * T.n + T.start]] + 'DWL'[r[c[1] * T.n + T.start]])
    for n in RANGE:
        T = tg.integer(n)
        r = cache['0'] if n == 0 else solve_rule(cg, T, wd, bd)
        for c in quiet:
            prof[c][n] = 'DWL'[r[c[0] * T.n + T.start]] + 'DWL'[r[c[1] * T.n + T.start]]
    cnt = collections.Counter()
    thr = collections.Counter()
    sens = {}
    for c in quiet:
        ns = [prof[c][n] for n in RANGE]
        s = len(set(fin[c])) > 1 or len(set(ns)) > 1
        up, dn = prof[c][1] != prof[c][0], prof[c][-1] != prof[c][0]
        sens[cg.placement(c[0])] = (s, up, dn)
        cnt['quiet'] += 1
        cnt['sensitive'] += s
        cnt['plus1'] += up
        cnt['minus1'] += dn
        cnt['pm1'] += up or dn
        cnt['neg_' + tail_kind([prof[c][n] for n in range(-10, -1)])] += 1
        cnt['pos_' + tail_kind([prof[c][n] for n in range(2, 11)])] += 1
        thr.update(n for n, a, b in zip(RANGE, ns, ns[1:]) if a != b)
    # kinds of result seen anywhere in a sensitive profile
    black_wins = sum(1 for c in quiet if len(set(fin[c]) | {prof[c][n] for n in RANGE}) > 1 and
                     any('L' in x for x in set(fin[c]) | {prof[c][n] for n in RANGE}))
    rec = dict(tempo_sensitive=cnt['sensitive'], sensitive_at_pm1=cnt['pm1'], sensitive_at_plus1=cnt['plus1'],
               sensitive_at_minus1=cnt['minus1'], thresholds={str(k): v for k, v in sorted(thr.items())},
               tails_n_minus10_to_minus2={k: cnt['neg_' + k] for k in ('constant', 'period2', 'other')},
               tails_n_2_to_10={k: cnt['pos_' + k] for k in ('constant', 'period2', 'other')},
               sensitive_profiles_containing_a_Black_win=black_wins)
    return rec, sens


def run(board):
    t0 = time.time()
    tag = board.replace(':', '_')
    cg = graph.ChessGraph(board)
    for n in range(-3, 4):                       # regression of the copy against product.py
        T = tg.integer(n)
        assert solve_rule(cg, T, False, False) == solve_product(cg, T), n
        assert solve_rule(cg, T, True, True) == solve_product(cg, T, stalemate_draw=True), n
    out = dict(label='COMPUTED-1', board=board, quiet=len(cg.quiet_kpk), rules={})
    allsens = {}
    for name, (wd, bd) in RULES:
        rec, sens = scan(cg, wd, bd)
        out['rules'][name] = rec
        allsens[name] = sens
    # the symmetric rules must reproduce chess_scan.py's per-placement file (when that board was scanned)
    path = os.path.join(HERE, 'chess_tempo_%s.jsonl' % tag)
    if os.path.exists(path):
        rows = {}
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                rows[r['placement']] = r
        ok = all(rows[pl]['chess_sensitive'] == s[0] and rows[pl]['normal_sensitive'] == allsens['WlBl'][pl][0] and
                 rows[pl]['sens_plus1'] == s[1] and rows[pl]['sens_minus1'] == s[2] for pl, s in allsens['WdBd'].items())
        out['symmetric_rules_reproduce_chess_scan'] = ok
        assert ok, 'asym.py disagrees with chess_scan.py on ' + board
    else:
        out['symmetric_rules_reproduce_chess_scan'] = 'not scanned by chess_scan.py'
    # overlap of the sensitive sets
    sets = {k: {pl for pl, v in d.items() if v[0]} for k, d in allsens.items()}
    out['sensitive_set_overlaps'] = {'%s&%s' % (a, b): len(sets[a] & sets[b]) for a in sets for b in sets if a < b}
    out['same_sensitive_set'] = {'WdBl == WlBl (White\'s stalemate result irrelevant, Black loses)': sets['WdBl'] == sets['WlBl'],
                                 'WlBd == WdBd (White\'s stalemate result irrelevant, Black draws)': sets['WlBd'] == sets['WdBd']}
    pm = {k: {pl for pl, v in d.items() if v[1] or v[2]} for k, d in allsens.items()}
    out['same_pm1_set'] = {'WdBl == WlBl': pm['WdBl'] == pm['WlBl'], 'WlBd == WdBd': pm['WlBd'] == pm['WdBd']}
    out['seconds'] = round(time.time() - t0, 1)
    json.dump(out, open(os.path.join(HERE, 'asym_%s.json' % tag), 'w'), indent=1)
    print(json.dumps(out), flush=True)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        run(b)
