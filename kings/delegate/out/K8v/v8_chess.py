"""K8v: chess-rule / mixed-stalemate-rule tempo scan with my own graph (v_gen), test games (v_games), C solver
(v_prod.c, stalemate modes 0 normal, 1 chess, 2 only White's stalemate draws, 3 only Black's draws) and kpsolve.
usage: v8_chess.py [--asym-only] board ...
Per board:
  1. my graph, written to work/; kpsolve (built from kings/kpsolve.c) on every node; check 1: kpsolve == my solver
     with the chess rule at T = 0 on every node (K+P vs K and the officer endings they lead to).
  2. every quiet placement (White to move, no officer, pawn on board, neither king in check): the 11 finite tests and
     x (+) n for n = -20..20 under the chess rule (sd=1) and normal play (sd=0); K8 comparison, field by field.
  3. mutual zugzwangs from kpsolve's own pair; zugzwang vs spare-move comparison; asym rules (sd=2,3).
Writes out/chess_<tag>.json and prints one summary line."""
import collections, json, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

RANK = {'L': 0, 'D': 1, 'W': 2}
FIN = vg.TESTS[:11]
assert FIN == ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1']
NS = list(range(-20, 21))
OUT = os.path.join(HERE, 'out')
CHESS_BOARDS = ['flat:3x4', 'flat:4x4', 'cyl:4x4', 'cyl:4x6', 'flat:5x6', 'cyl:3x6', 'cyl:5x6', 'cyl:6x5', 'cyl:7x5',
                'cyl:3x7', 'cyl:3x8', 'cyl:2x6', 'cyl:2x8']


def tail(seq):
    """seq: list of pair strings over consecutive n.  constant / period2 (pair(n) = pair(n+2), not constant) / other"""
    if len(set(seq)) == 1:
        return 'constant'
    if all(seq[i] == seq[i + 2] for i in range(len(seq) - 2)):
        return 'period2'
    return 'other'


def tailcount(seqs):
    c = collections.Counter(tail(q) for q in seqs)
    return {k: c.get(k, 0) for k in ('constant', 'period2', 'other')}


def thresholds(prof, lo=-10, hi=10):
    """prof: dict n -> pair; n in lo..hi-1 with prof[n] != prof[n+1]"""
    return [n for n in range(lo, hi) if prof[n] != prof[n + 1]]


def analyse(R, quiet, finkeys, ns_scan, ns_tail_lo, ns_tail_hi):
    """R: dict game name -> result string.  returns dict placement-index -> record"""
    recs = []
    for (cw, cb) in quiet:
        fin = {t: R[k][cw] + R[k][cb] for t, k in finkeys.items() if t in FIN}
        prof = {n: R['N%d' % (n + 20)][cw] + R['N%d' % (n + 20)][cb] for n in ns_scan}
        thr = thresholds(prof, -10, 10)
        fsens = len(set(fin.values())) > 1
        nsens = bool(thr)
        recs.append(dict(fin=fin, prof=prof, thr=thr, sens=fsens or nsens, fsens=fsens, nsens=nsens,
                         plus1=prof[1] != prof[0], minus1=prof[-1] != prof[0]))
    return recs


def main(board, asym_only=False):
    t0 = time.time()
    M = v_gen.build(board)
    G = M['G']
    n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.g8')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]),
                                           ' '.join(map(str, M['succ'][i]))))
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes'])
             if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    place = []
    for (cw, cb) in quiet:
        p = M['nodes'][cw]
        place.append('K%s P%s k%s' % (v_gen.name(G, p[1]), v_gen.name(G, p[3]), v_gen.name(G, p[2])))
    # ---- kpsolve on every node
    inp = os.path.join(v_run.WORK, tag + '.kp8in')
    outp = os.path.join(v_run.WORK, tag + '.kp8out')
    with open(inp, 'w') as f:
        for p in M['nodes']:
            f.write(v_gen.kpline(G, p) + '\n')
    cmd = ['nice', '-n', '10', os.path.join(HERE, 'kp'), '--board', board, '--ep', 'on', '--promote', 'QRBN',
           '--cap', '1', '--threads', '2']
    with open(inp) as fi, open(outp, 'w') as fo:
        subprocess.run(cmd, stdin=fi, stdout=fo, stderr=subprocess.DEVNULL, check=True)
    lines = open(outp).read().splitlines()
    assert len(lines) == n
    KP = []
    nonexact = 0
    for line in lines:
        a, b = line.rsplit(' | ', 1)[1].split()
        nonexact += a != b
        KP.append(a)
    os.remove(inp); os.remove(outp)
    # ---- games
    tpath = os.path.join(v_run.WORK, tag + '.t8')
    nsc = list(range(-10, 11)) if asym_only else NS
    items = [('T%d' % k, vg.GAMES[t]) for k, t in enumerate(vg.TESTS[:11])]
    items += [('N%d' % (k + 20), vg.integer(k)) for k in nsc]
    v_run.write_games(tpath, items)
    sds = (0, 1, 2, 3) if asym_only else (0, 1)
    RES = {sd: v_run.run_c(gpath, tpath, sd) for sd in sds}
    os.remove(gpath); os.remove(tpath)
    # ---- check 1: chess rule at T = 0 against kpsolve on every node
    Z = RES[1]['N20']
    d_check1 = sum(KP[i] != Z[i] for i in range(n))
    kpk = sum(1 for p in M['nodes'] if p[3] >= 0 and p[4] is None)
    chk = dict(nodes=n, kpk=kpk, other=n - kpk, differences=d_check1, kp_nonexact_lines=nonexact)
    # ---- scan under each rule
    finkeys = {t: 'T%d' % k for k, t in enumerate(vg.TESTS[:11])}
    scans = {}
    for sd in sds:
        scans[sd] = analyse(RES[sd], quiet, finkeys, nsc, -20, 20)
    rule_name = {0: 'WlBl', 1: 'WdBd', 2: 'WdBl', 3: 'WlBd'}
    summ = dict(board=board, quiet=len(quiet), check1=chk)
    # kpsolve pair and mutual zugzwang
    kppair = [(KP[cw], KP[cb]) for (cw, cb) in quiet]
    zug = [RANK[a] < RANK[b] for a, b in kppair]
    summ['mutual_zugzwangs'] = sum(zug)
    summ['zug_by_pair'] = dict(collections.Counter(a + b for (a, b), z in zip(kppair, zug) if z))
    summ['kp_pair_all'] = dict(collections.Counter(a + b for a, b in kppair))
    # own T=0 chess results agree with kp pair (redundant with check1 but explicit at quiet placements)
    summ['kp_vs_mine_T0_quiet_pairs'] = sum((RES[1]['N20'][cw] + RES[1]['N20'][cb]) != a + b for (cw, cb), (a, b) in zip(quiet, kppair))
    rules = {}
    for sd in sds:
        S = scans[sd]
        r = {}
        r['tempo_sensitive'] = sum(x['sens'] for x in S)
        r['sensitive_to_finite_tests'] = sum(x['fsens'] for x in S)
        r['sensitive_to_n_scan'] = sum(x['nsens'] for x in S)
        r['sensitive_at_plus1'] = sum(x['plus1'] for x in S)
        r['sensitive_at_minus1'] = sum(x['minus1'] for x in S)
        r['sensitive_at_pm1'] = sum(x['plus1'] or x['minus1'] for x in S)
        thr = collections.Counter(t for x in S for t in x['thr'])
        r['thresholds'] = {str(k): v for k, v in sorted(thr.items())}
        r['tails_n_minus10_to_minus2'] = tailcount([x['prof'][m] for m in range(-10, -1)] for x in S)
        r['tails_n_2_to_10'] = tailcount([x['prof'][m] for m in range(2, 11)] for x in S)
        if not asym_only:
            r['tails_n_minus20_to_minus2'] = tailcount([x['prof'][m] for m in range(-20, -1)] for x in S)
            r['tails_n_2_to_20'] = tailcount([x['prof'][m] for m in range(2, 21)] for x in S)
        r['sensitive_profiles_containing_a_Black_win'] = sum(
            x['sens'] and ('L' in ''.join(x['fin'].values()) or 'L' in ''.join(x['prof'].values())) for x in S)
        r['sensitive_profiles_with_a_Black_win_in_the_n_scan_or_finite_tests_any_placement'] = sum(
            ('L' in ''.join(x['fin'].values()) or 'L' in ''.join(x['prof'].values())) for x in S)
        r['deepest_threshold'] = min(thr) if thr else None
        r['sensitive_set_hash'] = sum(1 << i for i, x in enumerate(S) if x['sens']) % (1 << 61)
        rules[rule_name[sd]] = r
    summ['rules'] = rules
    sets = {rule_name[sd]: {i for i, x in enumerate(scans[sd]) if x['sens']} for sd in sds}
    pm1 = {rule_name[sd]: {i for i, x in enumerate(scans[sd]) if x['plus1'] or x['minus1']} for sd in sds}
    if asym_only:
        names = list(rule_name.values())
        ov = {}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                ov['&'.join(sorted([a, b]))] = len(sets[a] & sets[b])
        summ['sensitive_set_overlaps'] = ov
        summ['same_sensitive_set'] = {'WdBl == WlBl': sets['WdBl'] == sets['WlBl'], 'WlBd == WdBd': sets['WlBd'] == sets['WdBd']}
        summ['same_pm1_set'] = {'WdBl == WlBl': pm1['WdBl'] == pm1['WlBl'], 'WlBd == WdBd': pm1['WlBd'] == pm1['WdBd']}
        def t0diff(a, b):
            za, zb = RES[a]['N20'], RES[b]['N20']
            return dict(all_nodes=sum(x != y for x, y in zip(za, zb)),
                        quiet_placements=sum((za[cw] + za[cb]) != (zb[cw] + zb[cb]) for (cw, cb) in quiet))
        summ['T0_changed_by_rule'] = {'White stalemate loss->draw, Black loses (sd0 vs sd2)': t0diff(0, 2),
                                      'White stalemate loss->draw, Black draws (sd3 vs sd1)': t0diff(3, 1),
                                      'Black stalemate loss->draw, White loses (sd0 vs sd3)': t0diff(0, 3),
                                      'Black stalemate loss->draw, White draws (sd2 vs sd1)': t0diff(2, 1)}
        summ['seconds'] = round(time.time() - t0, 1)
        json.dump(summ, open(os.path.join(OUT, 'asym_' + tag + '.json'), 'w'))
        print(json.dumps(summ), flush=True)
        return 0
    # ---- chess-rule detail (sd = 1), normal rule (sd = 0)
    C, N = scans[1], scans[0]
    sens_c = {i for i, x in enumerate(C) if x['sens']}
    sens_pm1 = pm1['WdBd']
    zset = {i for i, z in enumerate(zug) if z}
    summ['zug_not_sens_pm1'] = len(zset - sens_pm1)
    summ['zug_not_sens_at_both_plus1_and_minus1'] = len({i for i in zset if not (C[i]['plus1'] and C[i]['minus1'])})
    summ['zug_not_tempo_sensitive'] = len(zset - sens_c)
    summ['pm1_not_zug'] = len(sens_pm1 - zset)
    summ['pm1_not_zug_share_percent'] = round(100.0 * len(sens_pm1 - zset) / max(1, len(sens_pm1)), 1)
    summ['tempo_sensitive_not_zug'] = len(sens_c - zset)
    summ['pm1_not_zug_by_kp_pair'] = dict(collections.Counter(kppair[i][0] + kppair[i][1] for i in sens_pm1 - zset))
    dire = collections.Counter()
    for i in sens_pm1 - zset:
        dire[('+1' if C[i]['plus1'] else '') + ('-1' if C[i]['minus1'] else '')] += 1
    summ['pm1_not_zug_direction'] = dict(dire)
    summ['sens_both_rules'] = len(sens_c & {i for i, x in enumerate(N) if x['sens']})
    summ['normal_tempo_sensitive'] = sum(x['sens'] for x in N)
    summ['sens_chess_only'] = len(sens_c - {i for i, x in enumerate(N) if x['sens']})
    summ['sens_normal_only'] = len({i for i, x in enumerate(N) if x['sens']} - sens_c)
    # chess zugzwangs under normal play: all W for every finite test and every n?
    bad = 0
    for i in zset:
        s = ''.join(N[i]['fin'].values()) + ''.join(N[i]['prof'].values())
        bad += set(s) != {'W'}
    summ['chess_zug_not_all_W_under_normal_play'] = bad
    # normal-play strict zugzwang K+P vs K placements: T=0 normal pair with White-to-move strictly worse than Black-to-move
    nz = [RANK[RES[0]['N20'][cw]] < RANK[RES[0]['N20'][cb]] for (cw, cb) in quiet]
    summ['normal_play_strict_zugzwang_placements'] = sum(nz)
    summ['normal_play_strict_zugzwang_pairs'] = dict(collections.Counter(RES[0]['N20'][cw] + RES[0]['N20'][cb] for (cw, cb), z in zip(quiet, nz) if z))
    # ---- compare with K8's per-placement jsonl (chess boards only)
    jl = os.path.join(BUILDER, 'chess_tempo_%s.jsonl' % tag)
    cmp = collections.Counter()
    if os.path.exists(jl):
        rows = {r['placement']: r for r in map(json.loads, open(jl))}
        cmp['rowset_symmetric_difference'] = len(set(rows) ^ set(place))
        for k, pl in enumerate(place):
            r = rows.get(pl)
            if r is None:
                continue
            c, nm = C[k], N[k]
            fin_c = ''.join(c['fin'][t] for t in FIN)
            fin_n = ''.join(nm['fin'][t] for t in FIN)
            n_c = ''.join(c['prof'][m] for m in range(-10, 11))
            n_n = ''.join(nm['prof'][m] for m in range(-10, 11))
            extra = ''.join(c['prof'][m] for m in list(range(-20, -10)) + list(range(11, 21)))
            cmp['kpsolve'] += r['kpsolve'] != list(kppair[k])
            cmp['mutual_zugzwang'] += r['mutual_zugzwang'] != zug[k]
            cmp['chess_finite'] += r['chess_finite'] != fin_c
            cmp['chess_n'] += r['chess_n'] != n_c
            cmp['chess_n_extra'] += r['chess_n_extra'] != extra
            cmp['chess_thresholds'] += r['chess_thresholds'] != c['thr']
            cmp['chess_sensitive'] += r['chess_sensitive'] != c['sens']
            cmp['sens_plus1'] += r['sens_plus1'] != c['plus1']
            cmp['sens_minus1'] += r['sens_minus1'] != c['minus1']
            cmp['sens_pm1'] += r['sens_pm1'] != (c['plus1'] or c['minus1'])
            cmp['normal_finite'] += r['normal_finite'] != fin_n
            cmp['normal_n'] += r['normal_n'] != n_n
            cmp['normal_thresholds'] += r['normal_thresholds'] != nm['thr']
            cmp['normal_sensitive'] += r['normal_sensitive'] != nm['sens']
            cmp['tail_n_le_minus2'] += r['tail_n_le_minus2'] != tail([c['prof'][m] for m in range(-20, -1)])
            cmp['tail_n_ge_2'] += r['tail_n_ge_2'] != tail([c['prof'][m] for m in range(2, 21)])
        summ['compared_with_K8_placements'] = len(rows)
    summ['K8_field_mismatches'] = dict(cmp)
    summ['K8_total_mismatches'] = sum(cmp.values())
    # ---- compare aggregates with K8 tempo_detail
    cand = [os.path.join(BUILDER, 'tempo_detail_chess_%s.json' % tag), os.path.join(BUILDER, 'tempo_detail_%s.json' % tag)]
    det = None
    for pth in cand:
        if os.path.exists(pth):
            d = json.load(open(pth))
            if d.get('rule', '').startswith('chess'):
                det = d
                break
    agg_bad = {}
    if det:
        r = rules['WdBd']
        pairs = [('tempo_sensitive', r['tempo_sensitive']), ('sensitive_to_finite_tests', r['sensitive_to_finite_tests']),
                 ('sensitive_to_n_scan', r['sensitive_to_n_scan']), ('thresholds', r['thresholds']),
                 ('tails_n_minus20_to_minus2', r['tails_n_minus20_to_minus2']), ('tails_n_2_to_20', r['tails_n_2_to_20']),
                 ('sensitive_at_pm1', r['sensitive_at_pm1']), ('sensitive_at_plus1', r['sensitive_at_plus1']),
                 ('sensitive_at_minus1', r['sensitive_at_minus1']), ('mutual_zugzwangs', summ['mutual_zugzwangs']),
                 ('mutual_also_pm1', summ['mutual_zugzwangs'] - summ['zug_not_sens_pm1']),
                 ('mutual_and_sensitive_at_both_plus1_and_minus1', summ['mutual_zugzwangs'] - summ['zug_not_sens_at_both_plus1_and_minus1']),
                 ('mutual_not_pm1', summ['zug_not_sens_pm1']), ('pm1_not_mutual', summ['pm1_not_zug']),
                 ('mutual_not_tempo_sensitive', summ['zug_not_tempo_sensitive']), ('tempo_sensitive_not_mutual', summ['tempo_sensitive_not_zug'])]
        for k, v in pairs:
            if det.get(k) != v:
                agg_bad[k] = (det.get(k), v)
        nr = det.get('normal_rule_same_placements', {})
        for k, v in (('tempo_sensitive', summ['normal_tempo_sensitive']), ('sensitive_under_both_rules', summ['sens_both_rules']),
                     ('only_chess_rule', summ['sens_chess_only']), ('only_normal_rule', summ['sens_normal_only'])):
            if nr.get(k) != v:
                agg_bad['normal_rule_same_placements.' + k] = (nr.get(k), v)
        sens_b = {e['placement']: e for e in det['sensitive']}
        mine_s = {place[i] for i in sens_c}
        agg_bad_sets = len(set(sens_b) ^ mine_s)
        summ['sensitive_listing_symmetric_difference_with_K8_tempo_detail'] = agg_bad_sets
    summ['K8_tempo_detail_aggregate_mismatches'] = agg_bad
    summ['seconds'] = round(time.time() - t0, 1)
    json.dump(summ, open(os.path.join(OUT, 'chess_' + tag + '.json'), 'w'))
    # per-placement result file (for later analysis): placement, kp pair, zug, chess prof, normal prof
    with open(os.path.join(OUT, 'chess_pp_' + tag + '.jsonl'), 'w') as f:
        for k, pl in enumerate(place):
            c, nm = C[k], N[k]
            f.write(json.dumps(dict(p=pl, kp=''.join(kppair[k]), z=zug[k], c=''.join(c['prof'][m] for m in NS),
                                    cf=''.join(c['fin'][t] for t in FIN), nn=''.join(nm['prof'][m] for m in NS),
                                    nf=''.join(nm['fin'][t] for t in FIN))) + '\n')
    print(json.dumps(summ), flush=True)
    return summ['K8_total_mismatches'] + len(agg_bad) + d_check1


if __name__ == '__main__':
    args = sys.argv[1:]
    ao = '--asym-only' in args
    args = [a for a in args if a != '--asym-only']
    sys.exit(1 if sum(main(b, ao) for b in args) else 0)
