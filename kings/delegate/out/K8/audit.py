"""K8 audit: re-derive every headline number from the per-placement files, without the solver.

    .venv/bin/python kings/delegate/out/K8/audit.py          (stdlib only; prints one line per check, exit 1 on any failure)

What is recomputed, and from which file:
  * kpsolve inputs/outputs (check1/<board>.in.gz, .out.gz): line counts equal the node count in meta_*.json, no 'X' results,
    and every quiet placement's two kpsolve results equal the 'chess' field of <board>.jsonl (normal-play boards) or the
    'kpsolve' field of chess_tempo_<board>.jsonl (chess-rule boards).  This re-reads kpsolve's own answer for each
    placement by position string, so it does not use graph.py or product.py.
  * chess_tempo_<board>.jsonl: tempo-sensitive count (11 finite pairs + 21 n-pairs not constant), sensitive at n = +1 / -1,
    thresholds, parity tails, mutual zugzwangs (kpsolve White-to-move result worse for White than Black-to-move), and the
    zugzwang comparison; all against the numbers in tempo_detail_*.json and summary.json.
  * <board>.jsonl + tempo_detail_<board>.json (normal play): quiet count, off-class count, finite-test sensitivity from the 32-character
    signatures, thresholds recomputed from the stored 21-pair profiles, sensitive count.
"""
import collections
import glob
import gzip
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from names import TASK1, chess_detail_path, tag  # noqa: E402

RANK = {'L': 0, 'D': 1, 'W': 2}
RANGE = list(range(-10, 11))
Z0 = RANGE.index(0)
EXTRA = list(range(-20, -10)) + list(range(11, 21))
fails = []


def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg, flush=True)
    if not ok:
        fails.append(msg)


def pairs(s):
    return [s[i:i + 2] for i in range(0, len(s), 2)]


def jl(path):
    with open(path) as f:
        return [json.loads(x) for x in f]


def tail_kind(seq):
    if len(set(seq)) == 1:
        return 'constant'
    if all(seq[i] == seq[i + 2] for i in range(len(seq) - 2)):
        return 'period2'
    return 'other'


def kpsolve_table(board, nodes):
    """{position string without the side marker: (white-to-move result, black-to-move result)} from the gz files."""
    t = tag(board)
    with gzip.open(os.path.join(HERE, 'check1', t + '.in.gz'), 'rt') as f:
        ins = [x.rstrip('\n') for x in f]
    with gzip.open(os.path.join(HERE, 'check1', t + '.out.gz'), 'rt') as f:
        outs = [x.rstrip('\n') for x in f]
    check(len(ins) == nodes and len(outs) == nodes, '%s: kpsolve input/output have %d / %d lines, graph has %d nodes' %
          (board, len(ins), len(outs), nodes))
    res = {}
    bad_x = 0
    for a, b in zip(ins, outs):
        pos, r = b.rsplit(' | ', 1)
        assert pos.split() == a.split() or pos == a, (a, pos)
        x, y = r.split()
        if 'X' in (x, y) or x != y:           # kpsolve prints two results per position; they must agree and be solved
            bad_x += 1
        stm = a.split()[-2]
        key = ' '.join(a.split()[:-2])
        res.setdefault(key, {})[stm] = x
    check(bad_x == 0, '%s: no unsolved (X) or disagreeing result pair in the kpsolve output' % board)
    return res


def kp_key(wk, p, bk):
    return ' '.join(['K' + wk, 'k' + bk, 'P' + p])


def audit_normal(board, summary):
    t = tag(board)
    meta = json.load(open(os.path.join(HERE, 'meta_%s.json' % t)))
    det = json.load(open(os.path.join(HERE, 'tempo_detail_%s.json' % t)))
    rows = jl(os.path.join(HERE, t + '.jsonl'))
    check(meta['check1_differences'] == 0 and meta['check1']['x'] == 0, '%s: check 1 (T = 0 vs kpsolve) 0 differences, 0 X' % board)
    check(meta['check1']['kpk'] + meta['check1']['other'] == meta['nodes'], '%s: check 1 covers all %d nodes' % (board, meta['nodes']))
    check(len(rows) == meta['quiet_placements'] == det['quiet'], '%s: %d placements in jsonl = meta = tempo_detail' % (board, len(rows)))
    table = kpsolve_table(board, meta['nodes'])
    bad = 0
    for r in rows:
        k = kp_key(r['wk'], r['p'], r['bk'])
        got = [table[k]['w'], table[k]['b']]
        if got != r['chess']:
            bad += 1
    check(bad == 0, '%s: the T = 0 result of every placement equals the kpsolve output (%d mismatches)' % (board, bad))
    off = sum('off' in r['matched'] for r in rows)
    fin_sens = sum(len(set(pairs(r['sig'][:22]))) > 1 for r in rows)
    check(fin_sens == det['sensitive_to_finite_tests'], '%s: finite-test sensitive %d = %d' % (board, fin_sens, det['sensitive_to_finite_tests']))
    sens = det['sensitive']
    check(len(sens) == det['tempo_sensitive'], '%s: %d sensitive entries = tempo_sensitive' % (board, len(sens)))
    thr = collections.Counter()
    n_sens = 0
    for e in sens:
        prof = [e['n_profile_full'][str(n)] for n in RANGE]
        fin = list(e['finite_tests'].values())
        assert len(set(fin)) > 1 or len(set(prof)) > 1
        n_sens += len(set(prof)) > 1
        thr.update(n for n, a, b in zip(RANGE, prof, prof[1:]) if a != b)
    check({str(k): v for k, v in sorted(thr.items())} == det['thresholds'], '%s: thresholds recomputed from the stored profiles %s' % (board, dict(sorted(thr.items()))))
    check(n_sens == det['sensitive_to_n_scan'], '%s: n-scan sensitive %d' % (board, n_sens))
    s = next(x for x in summary['task1'] if x['board'] == board)
    check(s['tempo_sensitive'] == det['tempo_sensitive'] and s['off_placements'] == off and s['quiet'] == len(rows) and
          s['thresholds'] == det['thresholds'] and s['kpsolve_check']['differences'] == 0,
          '%s: summary.json agrees (off class %d placements, %d sensitive)' % (board, off, det['tempo_sensitive']))
    check((off > 0) == (det['tempo_sensitive'] > 0), '%s: off class %s <=> tempo-sensitive %s' % (board, off > 0, det['tempo_sensitive'] > 0))
    # direct (signature-free) count of what 'off' means is done by offclass.py
    reach_L = sum('L' in ''.join(e['n_profile_full'].values()) + ''.join(e['finite_tests'].values()) for e in sens)
    return dict(board=board, off=off, sensitive=det['tempo_sensitive'], sensitive_profiles_with_a_Black_win=reach_L)


def audit_chess(board, summary):
    t = tag(board)
    det = json.load(open(chess_detail_path(board)))
    rows = jl(os.path.join(HERE, 'chess_tempo_%s.jsonl' % t))
    meta = json.load(open(os.path.join(HERE, 'meta_chess_%s.json' % t)))
    check(meta['check1_differences'] == 0 and meta['check1']['x'] == 0, '%s [chess]: check 1 (T = 0 vs kpsolve) 0 differences, 0 X' % board)
    check(meta['check1']['kpk'] + meta['check1']['other'] == meta['nodes'], '%s [chess]: check 1 covers all %d nodes' % (board, meta['nodes']))
    check(len(rows) == meta['quiet_placements'] == det['quiet'], '%s [chess]: %d placements' % (board, len(rows)))
    table = kpsolve_table(board, meta['nodes'])
    bad = 0
    cnt = collections.Counter()
    thr = collections.Counter()
    for r in rows:
        k = kp_key(r['wk'], r['p'], r['bk'])
        kp = [table[k]['w'], table[k]['b']]
        bad += kp != r['kpsolve']
        fin = pairs(r['chess_finite'])
        ns = pairs(r['chess_n'])
        extra = dict(zip(EXTRA, pairs(r['chess_n_extra'])))
        assert len(fin) == 11 and len(ns) == 21 and len(extra) == 20
        bad += ''.join(kp) != ns[Z0] or fin[0] != ns[Z0]
        sens_fin, sens_n = len(set(fin)) > 1, len(set(ns)) > 1
        up, dn = ns[Z0 + 1] != ns[Z0], ns[Z0 - 1] != ns[Z0]
        zug = RANK[kp[1]] > RANK[kp[0]]
        full = dict(extra)
        full.update(zip(RANGE, ns))
        neg = tail_kind([full[n] for n in range(-20, -1)])
        pos = tail_kind([full[n] for n in range(2, 21)])
        bad += (zug != r['mutual_zugzwang']) + ((sens_fin or sens_n) != r['chess_sensitive']) + ((up, dn) != (r['sens_plus1'], r['sens_minus1']))
        bad += (neg != r['tail_n_le_minus2']) + (pos != r['tail_n_ge_2'])
        thr.update(n for n, a, b in zip(RANGE, ns, ns[1:]) if a != b)
        cnt['quiet'] += 1
        cnt['sens'] += sens_fin or sens_n
        cnt['sens_fin'] += sens_fin
        cnt['sens_n'] += sens_n
        cnt['plus1'] += up
        cnt['minus1'] += dn
        cnt['pm1'] += up or dn
        cnt['zug'] += zug
        cnt['zug_pm1'] += zug and (up or dn)
        cnt['zug_both'] += zug and up and dn
        cnt['sens_not_zug_pm1'] += (up or dn) and not zug
        cnt['sens_not_zug_any'] += (sens_fin or sens_n) and not zug
        cnt['zug_not_sens_any'] += zug and not (sens_fin or sens_n)
        cnt['neg_' + neg] += 1
        cnt['pos_' + pos] += 1
        cnt['zug_pair_not_DW'] += zug and ''.join(kp) != 'DW'
    check(bad == 0, '%s [chess]: kpsolve results, zugzwang flags, sensitivity flags, tails recomputed from the stored strings (%d mismatches)' % (board, bad))
    ok = (cnt['sens'] == det['tempo_sensitive'] and cnt['sens_fin'] == det['sensitive_to_finite_tests'] and
          cnt['sens_n'] == det['sensitive_to_n_scan'] and cnt['pm1'] == det['sensitive_at_pm1'] and
          cnt['plus1'] == det['sensitive_at_plus1'] and cnt['minus1'] == det['sensitive_at_minus1'] and
          cnt['zug'] == det['mutual_zugzwangs'] and cnt['zug_pm1'] == det['mutual_also_pm1'] and
          cnt['sens_not_zug_pm1'] == det['pm1_not_mutual'] and cnt['zug'] - cnt['zug_pm1'] == det['mutual_not_pm1'] and
          {str(k): v for k, v in sorted(thr.items())} == det['thresholds'] and
          {k: cnt['neg_' + k] for k in ('constant', 'period2', 'other')} == det['tails_n_minus20_to_minus2'] and
          {k: cnt['pos_' + k] for k in ('constant', 'period2', 'other')} == det['tails_n_2_to_20'])
    check(ok, '%s [chess]: every count in tempo_detail agrees with the recount from the jsonl' % board)
    s = next(x for x in summary['task2'] + summary['task2_extra'] if x['board'] == board)
    check(s['tempo_sensitive'] == cnt['sens'] and s['mutual_zugzwangs'] == cnt['zug'] and s['sensitive_at_pm1'] == cnt['pm1'] and
          s['kpsolve_check']['differences'] == 0, '%s [chess]: summary.json agrees' % board)
    check(cnt['zug'] == cnt['zug_both'] and cnt['zug_pair_not_DW'] == 0,
          '%s [chess]: all %d mutual zugzwangs are sensitive at BOTH n = +1 and n = -1 and all are (White to move D, Black to move W)' %
          (board, cnt['zug']))
    return cnt


def audit_pvstats(summary):
    normal = {x['board']: x for x in summary['task1']}
    for d in summary.get('pvstats', []):
        b = d['board']
        n = d['normal play']
        mt = n['mask_tests_quiet_placements_that_differ_from_the_full_result']
        check(mt['all zugzwang nodes']['n=+1'] == 0 and mt['all zugzwang nodes']['n=-1'] == 0,
              '%s: normal play, the spare move is needed only at strict-zugzwang nodes (0 placements differ with the pass allowed only there)' % b)
        check(mt['no spare move']['n=+1'] + mt['no spare move']['n=-1'] > 0 or n['spare_move_wins']['states'] == 0,
              '%s: normal play, the mask test is not vacuous' % b)
        if b in normal:
            check(n['spare_move_wins']['states'] > 0 if normal[b]['tempo_sensitive'] else True,
                  '%s: normal-play tempo-sensitive board has positions won only with the spare move' % b)
        ends = n['spare_move_wins']['how_the_win_ends']
        check(set(ends) <= {'Black stalemated', 'Black checkmated', 'Black captured/other'}, '%s: end types known %s' % (b, ends))


def audit_side(summary):
    """offclass_*.json, explain_*.json, asym_*.json against each other and against the chess-rule counts."""
    chess = {x['board']: x for x in summary['task2'] + summary['task2_extra']}
    normal = {x['board']: x for x in summary['task1']}
    for d in summary['offclass']:
        b = d['board']
        if 'off_class_equals_white_stalemated' in d:
            check(d['off_class_equals_white_stalemated'] and d['off_class_from_signatures'] == d['white_stalemated'],
                  '%s: the off / off+* class is exactly the %d placements where White to move is stalemated' % (b, d['white_stalemated']))
        if b in normal:
            check(d['quiet'] == normal[b]['quiet'], '%s: offclass.py sees %d quiet placements' % (b, d['quiet']))
    for d in summary['explain']:
        b = d['board']
        cn = d['critical_nodes']
        check(cn['zugzwang_white'] == chess[b]['mutual_zugzwangs'] == cn['zugzwang_black'] and
              cn['zugzwang_white_that_are_kpk'] == cn['zugzwang_white'] and cn['zugzwang_black_that_are_kpk'] == cn['zugzwang_black'],
              '%s: the generalised zugzwang nodes of the whole graph are exactly the %d mutual-zugzwang placements (no officer position)' %
              (b, chess[b]['mutual_zugzwangs']))
    for d in summary['asym']:
        b = d['board']
        check(d['symmetric_rules_reproduce_chess_scan'] in (True, 'not scanned by chess_scan.py'), '%s: asym.py reproduces chess_scan.py' % b)
        r = d['rules']
        if b in chess:
            check(r['WdBd']['tempo_sensitive'] == chess[b]['tempo_sensitive'], '%s: asym WdBd count = chess_scan count %d' % (b, chess[b]['tempo_sensitive']))
        if b in normal:
            check(r['WlBl']['tempo_sensitive'] == normal[b]['tempo_sensitive'], '%s: asym WlBl count = normal-play count %d' % (b, normal[b]['tempo_sensitive']))


if __name__ == '__main__':
    summary = json.load(open(os.path.join(HERE, 'summary.json')))
    out = {}
    for b in TASK1:
        out[b] = audit_normal(b, summary)
    for b in [x['board'] for x in summary['task2'] + summary['task2_extra']]:
        out['chess ' + b] = dict(audit_chess(b, summary))
    audit_side(summary)
    audit_pvstats(summary)
    print(json.dumps({k: v for k, v in out.items() if not k.startswith('chess ')}))
    print('\n%d check(s) failed' % len(fails))
    sys.exit(1 if fails else 0)
