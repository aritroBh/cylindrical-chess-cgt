"""K8 Task 2: the tempo scan under the chess stalemate rule, and the mutual-zugzwang comparison.

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K8/chess_scan.py flat:3x4

Rule ("chess"): a side with no legal move in the whole sum x (+) T that is NOT in check draws (the mover
is stalemated); a side in check with no move loses (checkmate).  Everything else is as in K4/K6: a move in
T is illegal while the mover is in check, infinite play is a draw.  Implemented as
product.solve_product(..., stalemate_draw=True); the default (normal play) is unchanged.

Steps for one board
 1. Gate: check1.check1 solves every legal K+P vs K position (and every K+officer / K vs K position they lead
    to) with T = 0 under the chess rule and compares each with kpsolve.  Any difference stops the run.
 2. Chess-rule scan: for every quiet placement (neither king in check) the (White starts, Black starts)
    result against the 11 finite test games and against the integer n for n = -10..10.
    TEMPO-SENSITIVE = these 11 + 21 results are not all equal (the K6 definition).
    SENSITIVE AT +-1 = the result at n = +1 or at n = -1 differs from the result at n = 0.
 3. The same scan under normal play (stalemate = loss), for a placement-by-placement comparison of the rules.
    (For the board's normal-play tempo count this is the K6 definition again; it is NOT the K8 task 1 run.)
 4. Mutual zugzwangs from kpsolve: a placement whose kpsolve result with White to move is worse for White than
    with Black to move (White's view L < D < W, e.g. White to move draws and Black to move loses).  Both
    sides then prefer the other to move.  Compared with the +-1-sensitive placements.
 5. Diagnostics for the placements in one set but not the other: kpsolve pair, which of n = +1 / n = -1
    changes, and the distance (in plies) to the nearest generalised zugzwang node (any node of the chess graph,
    also with officers, whose mover would rather pass: result worse for the mover than with the other side
    to move) over chess moves only.
"""
import collections
import json
import os
import sys
import time

import check1
import checks
import graph
import testgames as tg
from names import chess_detail_path
from product import solve_product

HERE = os.path.dirname(os.path.abspath(__file__))
RANGE = list(range(-10, 11))
EXTRA = list(range(-20, -10)) + list(range(11, 21))     # chess rule only: do the tails persist?
FINITE = tg.TESTS[:11]
RANK = {'L': 0, 'D': 1, 'W': 2}
Z0 = RANGE.index(0)


def pair(res, c, T):
    return 'DWL'[res[c[0] * T.n + T.start]] + 'DWL'[res[c[1] * T.n + T.start]]


def profiles(cg, stalemate_draw, extra=()):
    """{(wnode, bnode): (list of 11 finite-test pairs, list of 21 pairs for n = -10..10, {n: pair} for n in extra)}"""
    fin = {c: [] for c in cg.quiet_kpk}
    ns = {c: [] for c in cg.quiet_kpk}
    ex = {c: {} for c in cg.quiet_kpk}
    cache = {}
    for name in FINITE:
        T = tg.GAMES[name]
        res = cache[name] = solve_product(cg, T, stalemate_draw=stalemate_draw)
        for c in fin:
            fin[c].append(pair(res, c, T))
    for n in RANGE:
        T = tg.integer(n)
        res = cache['0'] if n == 0 else solve_product(cg, T, stalemate_draw=stalemate_draw)
        for c in ns:
            ns[c].append(pair(res, c, T))
    for n in extra:
        T = tg.integer(n)
        res = solve_product(cg, T, stalemate_draw=stalemate_draw)
        for c in ex:
            ex[c][n] = pair(res, c, T)
    return fin, ns, ex


def tail_kind(seq):
    """'constant', 'period2' (a_i == a_{i+2} but not constant) or 'other' for a list of results at consecutive n."""
    if len(set(seq)) == 1:
        return 'constant'
    if all(seq[i] == seq[i + 2] for i in range(len(seq) - 2)):
        return 'period2'
    return 'other'


def runs(profile):
    """'n<=-2: DD | n=-1: DW | n>=0: WW' style run-length text of the 21 results n = -10..10."""
    out, start = [], 0
    for i in range(1, len(profile) + 1):
        if i == len(profile) or profile[i] != profile[start]:
            a, b = RANGE[start], RANGE[i - 1]
            lab = ('n<=%d' % b if a == RANGE[0] else 'n>=%d' % a if b == RANGE[-1] else
                   'n=%d' % a if a == b else 'n=%d..%d' % (a, b))
            out.append('%s: %s' % (lab, profile[start]))
            start = i
    return ' | '.join(out)


def pass_sensitive_distances(cg, res0):
    """Plies from every node to the nearest node where ONE spare move (a pass) can change the value, over chess moves only.

    Two kinds of source node c (the mover can pass, i.e. is not in check; res0 = chess rule, T = 0, White's view):
      (i)  zugzwang node: the mover does strictly worse than if the other side moved from the same placement
           (White's view: result(White to move) < result(Black to move)); a pass helps the mover.
      (ii) forced-pass node: the mover has no chess move (stalemate under the chess rule, value D) and the
           result after the pass differs from D; a spare move cancels the stalemate and the pass is forced.
    Returns (dist_i, dist_any): distance to the nearest (i) node, and to the nearest (i)-or-(ii) node; -1 = none."""
    n = cg.n
    order = {2: 0, 0: 1, 1: 2}                     # White's view: L < D < W
    src_i, src_ii = [], []
    for c in range(n):
        f = cg.flip[c]
        if f < 0:
            continue
        w, b = (res0[c], res0[f]) if cg.stm[c] == 0 else (res0[f], res0[c])
        if order[w] < order[b]:
            src_i.append(c)
        elif cg.succ_off[c + 1] == cg.succ_off[c] and res0[f] != 0:
            src_ii.append(c)

    def bfs(sources):
        dist = [-1] * n
        for c in sources:
            dist[c] = 0
        frontier, d = list(sources), 0
        while frontier:
            d += 1
            nxt = []
            for v in frontier:
                for k in range(cg.pred_off[v], cg.pred_off[v + 1]):
                    p = cg.pred[k]
                    if dist[p] < 0:
                        dist[p] = d
                        nxt.append(p)
            frontier = nxt
        return dist
    return bfs(src_i), bfs(src_i + src_ii), len(src_i), len(src_ii)


def scan(board):
    t0 = time.time()
    tag = board.replace(':', '_')
    cg = graph.ChessGraph(board)

    # Gate 0 (check 2): the pure CGT sums of the test games agree with known facts.
    c2 = checks.check2()
    if not all(r[4] for r in c2):
        raise SystemExit('CHECK 2 FAILED: %r' % [r[0] for r in c2 if not r[4]])

    # Gate: the chess-rule variant at T = 0 must equal kpsolve on every position of the graph.
    c1 = check1.check1(cg, os.path.join(HERE, 'check1'))
    if c1['diffs']:
        path = os.path.join(HERE, 'FAILED_chess_check1_%s.json' % tag)
        json.dump(c1, open(path, 'w'), indent=1)
        raise SystemExit('CHECK 1 FAILED on %s; see %s' % (board, path))

    cfin, cns, cex = profiles(cg, True, EXTRA)      # chess rule
    nfin, nns, _ = profiles(cg, False)              # normal play (for the comparison)

    # T = 0 of the scan must agree with kpsolve for every quiet placement
    for c in cg.quiet_kpk:
        assert cns[c][Z0] == ''.join(c1['kpk_outcomes'][cg.placement(c[0])]), cg.placement(c[0])
        assert cfin[c][0] == cns[c][Z0]

    res0 = solve_product(cg, tg.GAMES['0'], stalemate_draw=True)
    dist, dist_any, n_src_i, n_src_ii = pass_sensitive_distances(cg, res0)

    mutual = set(c1['mutual_placements'])
    thresholds = collections.Counter()
    nthresholds = collections.Counter()
    rows, sensitive = [], []
    cnt = collections.Counter()
    for c in sorted(cg.quiet_kpk, key=lambda p: cg.placement(p[0])):
        pl = cg.placement(c[0])
        fin, ns = cfin[c], cns[c]
        s_fin, s_n = len(set(fin)) > 1, len(set(ns)) > 1
        s_all = s_fin or s_n
        up, dn = ns[Z0 + 1] != ns[Z0], ns[Z0 - 1] != ns[Z0]
        jumps = [n for n, a, b in zip(RANGE, ns, ns[1:]) if a != b]
        thresholds.update(jumps)
        nf, nn = nfin[c], nns[c]
        ns_all = len(set(nf)) > 1 or len(set(nn)) > 1
        njumps = [n for n, a, b in zip(RANGE, nn, nn[1:]) if a != b]
        nthresholds.update(njumps)
        stm, wk, bk, offs, wp, bp, ep = cg.pos[c[0]]
        kp = c1['kpk_outcomes'][pl]
        z = pl in mutual
        d = min([x for x in (dist[c[0]], dist[c[1]]) if x >= 0], default=-1)
        d2 = min([x for x in (dist_any[c[0]], dist_any[c[1]]) if x >= 0], default=-1)
        row = dict(placement=pl, wk=cg.sqname(wk), p=cg.sqname(wp.bit_length() - 1), bk=cg.sqname(bk),
                   kpsolve=kp, mutual_zugzwang=z,
                   chess_finite=''.join(fin), chess_n=''.join(ns), chess_thresholds=jumps,
                   chess_sensitive=s_all, sens_plus1=up, sens_minus1=dn, sens_pm1=up or dn,
                   normal_finite=''.join(nf), normal_n=''.join(nn), normal_thresholds=njumps,
                   normal_sensitive=ns_all, plies_to_zugzwang=d, plies_to_pass_effect=d2)
        full = dict(cex[c])
        full.update(zip(RANGE, ns))
        neg = tail_kind([full[n] for n in range(-20, -1)])       # n = -20 .. -2
        pos = tail_kind([full[n] for n in range(2, 21)])         # n = 2 .. 20
        row['tail_n_le_minus2'] = neg
        row['tail_n_ge_2'] = pos
        row['chess_n_extra'] = ''.join(cex[c][n] for n in EXTRA)      # n = -20..-11, 11..20
        cnt['neg_' + neg] += 1
        cnt['pos_' + pos] += 1
        rows.append(row)
        cnt['quiet'] += 1
        cnt['sens'] += s_all
        cnt['sens_fin'] += s_fin
        cnt['sens_n'] += s_n
        cnt['pm1'] += up or dn
        cnt['plus1'] += up
        cnt['minus1'] += dn
        cnt['normal_sens'] += ns_all
        cnt['both_rules'] += s_all and ns_all
        cnt['only_chess_rule'] += s_all and not ns_all
        cnt['only_normal_rule'] += ns_all and not s_all
        cnt['mutual'] += z
        if z and (up or dn):
            cnt['mutual_and_pm1'] += 1
        if z and up and dn:
            cnt['mutual_and_both_pm1'] += 1
        if s_all:
            sensitive.append(dict(placement=pl, kpsolve=kp, mutual_zugzwang=z,
                                  finite_tests=dict(zip(FINITE, fin)), n_profile=runs(ns),
                                  thresholds=jumps, sens_pm1=up or dn,
                                  normal_rule_sensitive=ns_all, plies_to_zugzwang=d, plies_to_pass_effect=d2))

    by_pm1 = {r['placement']: r for r in rows}
    zug_not_sens = [r for r in rows if r['mutual_zugzwang'] and not r['sens_pm1']]
    sens_not_zug = [r for r in rows if r['sens_pm1'] and not r['mutual_zugzwang']]
    zug_not_any = [r for r in rows if r['mutual_zugzwang'] and not r['chess_sensitive']]
    sens_not_zug_any = [r for r in rows if r['chess_sensitive'] and not r['mutual_zugzwang']]

    def kp_pair(r):
        return ''.join(r['kpsolve'])

    # diagnostics on the placements in one set only
    diag = dict(
        sens_pm1_not_zugzwang_by_kpsolve_pair=dict(collections.Counter(kp_pair(r) for r in sens_not_zug)),
        sens_pm1_not_zugzwang_direction=dict(collections.Counter(
            ('+1' if r['sens_plus1'] else '') + ('-1' if r['sens_minus1'] else '') for r in sens_not_zug)),
        sens_pm1_not_zugzwang_plies_to_zugzwang=dict(sorted(collections.Counter(
            r['plies_to_zugzwang'] for r in sens_not_zug).items())),
        sens_pm1_not_zugzwang_plies_to_pass_effect=dict(sorted(collections.Counter(
            r['plies_to_pass_effect'] for r in sens_not_zug).items())),
        zugzwang_plies_to_zugzwang=dict(sorted(collections.Counter(
            r['plies_to_zugzwang'] for r in rows if r['mutual_zugzwang']).items())),
        insensitive_plies_to_zugzwang=dict(sorted(collections.Counter(
            r['plies_to_zugzwang'] for r in rows if not r['sens_pm1']).items())),
        insensitive_plies_to_pass_effect=dict(sorted(collections.Counter(
            r['plies_to_pass_effect'] for r in rows if not r['sens_pm1']).items())),
        pass_effect_source_nodes=dict(zugzwang_nodes=n_src_i, forced_pass_nodes=n_src_ii),
        zugzwang_by_kpsolve_pair=dict(collections.Counter(kp_pair(r) for r in rows if r['mutual_zugzwang'])),
        zugzwang_direction=dict(collections.Counter(
            ('+1' if r['sens_plus1'] else '') + ('-1' if r['sens_minus1'] else '') or 'none'
            for r in rows if r['mutual_zugzwang'])),
        all_by_kpsolve_pair=dict(collections.Counter(kp_pair(r) for r in rows)),
    )

    def ex(rs, k=6):
        return [dict(placement=r['placement'], kpsolve=r['kpsolve'], chess_n=r['chess_n'],
                     plies_to_zugzwang=r['plies_to_zugzwang'],
                     plies_to_pass_effect=r['plies_to_pass_effect']) for r in rs[:k]]

    jlpath = os.path.join(HERE, 'chess_tempo_%s.jsonl' % tag)
    with open(jlpath, 'w') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    meta = dict(board=board, nodes=cg.n, edges=len(cg.succ), kpk_positions=len(cg.kpk),
                quiet_placements=len(cg.quiet_kpk),
                check1={k: v for k, v in c1.items() if k not in ('diffs', 'mutual_placements', 'kpk_outcomes')},
                check1_differences=0, mutual_examples=c1['mutual_placements'][:5])
    json.dump(meta, open(os.path.join(HERE, 'meta_chess_%s.json' % tag), 'w'), indent=1)

    detail = dict(
        label='COMPUTED-1', board=board, rule='chess stalemate rule (stalemate draws, checkmate loses)',
        quiet=len(rows),
        check2=dict(passed=True, facts=len(c2)),
        kpsolve_check=dict(passed=True, kpk=c1['kpk'], other=c1['other'], compared=c1['kpk'] + c1['other'],
                           differences=0, x=c1['x']),
        tempo_sensitive=cnt['sens'], sensitive_to_finite_tests=cnt['sens_fin'], sensitive_to_n_scan=cnt['sens_n'],
        thresholds={str(k): v for k, v in sorted(thresholds.items())},
        tails_n_minus20_to_minus2={k: cnt['neg_' + k] for k in ('constant', 'period2', 'other')},
        tails_n_2_to_20={k: cnt['pos_' + k] for k in ('constant', 'period2', 'other')},
        sensitive_at_pm1=cnt['pm1'], sensitive_at_plus1=cnt['plus1'], sensitive_at_minus1=cnt['minus1'],
        mutual_zugzwangs=cnt['mutual'], mutual_also_pm1=cnt['mutual_and_pm1'],
        mutual_and_sensitive_at_both_plus1_and_minus1=cnt['mutual_and_both_pm1'],
        mutual_not_pm1=len(zug_not_sens), pm1_not_mutual=len(sens_not_zug),
        mutual_not_tempo_sensitive=len(zug_not_any), tempo_sensitive_not_mutual=len(sens_not_zug_any),
        mutual_not_pm1_examples=ex(zug_not_sens), pm1_not_mutual_examples=ex(sens_not_zug),
        diagnostics=diag,
        normal_rule_same_placements=dict(
            tempo_sensitive=cnt['normal_sens'], thresholds={str(k): v for k, v in sorted(nthresholds.items())},
            sensitive_under_both_rules=cnt['both_rules'], only_chess_rule=cnt['only_chess_rule'],
            only_normal_rule=cnt['only_normal_rule']),
        sensitive_examples=sensitive[:5], sensitive=sensitive,
        per_placement_jsonl=os.path.basename(jlpath), seconds=round(time.time() - t0, 1))
    json.dump(detail, open(chess_detail_path(board), 'w'), indent=1, ensure_ascii=False)
    short = {k: v for k, v in detail.items() if k not in ('sensitive', 'sensitive_examples')}
    print(json.dumps(short, ensure_ascii=False), flush=True)
    return detail


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: chess_scan.py BOARD')
    scan(sys.argv[1])
