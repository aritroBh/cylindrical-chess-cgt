"""Print the tables of REPORT.md from summary.json:

    .venv/bin/python kings/delegate/out/K8/tables.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, 'summary.json')))


def thr(d):
    return ', '.join('%s:%d' % (k, v) for k, v in d.items()) or 'none'


print('## Task 1 (normal play)')
print('| board | quiet | off class | off placements | tempo-sensitive | thresholds (n: placements) | kpsolve compared / diffs | mutual zugzwangs (chess, kpsolve) | Ka3 Pa2 ka5 (W to move, B to move) | prediction | seconds |')
print('|---|---:|---|---:|---:|---|---|---:|---|---|---:|')
for r in S['task1']:
    p = r['prediction']
    pr = '-' if not p else '%s (off class says %s, observed %s): %s' % (
        p['expected'], p['from_off_class'], p['observed'], 'CONFIRMED' if p['confirmed'] else 'REFUTED')
    print('| %s | %d | %s | %d | %d | %s | %d / %d | %d | %s | %s | %s |' % (
        r['board'], r['quiet'], r['off_class'], r['off_placements'], r['tempo_sensitive'], thr(r['thresholds']),
        r['kpsolve_check']['compared'], r['kpsolve_check']['differences'], r['mutual_zugzwangs_kpsolve'],
        ' '.join(r['Ka3_Pa2_ka5_chess_result'] or ['-']), pr, r['seconds']))

print()
print('## Task 2 (chess stalemate rule)')
print('| board | quiet | tempo-sensitive | sens. at n=+1 | sens. at n=-1 | sens. at +-1 | mutual zugzwangs | zugzwang not sens. at +-1 | sens. at +-1 not zugzwang | kpsolve compared / diffs | normal-rule count (recomputed; K4/K6) | sensitive under both rules | seconds |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|')
for r in S['task2']:
    nr = r['normal_rule_same_placements']
    print('| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d / %d | %d (%d) | %d | %s |' % (
        r['board'], r['quiet'], r['tempo_sensitive'], r['sensitive_at_plus1'], r['sensitive_at_minus1'],
        r['sensitive_at_pm1'], r['mutual_zugzwangs'], r['mutual_not_pm1'], r['pm1_not_mutual'],
        r['kpsolve_check']['compared'], r['kpsolve_check']['differences'], nr['tempo_sensitive'],
        r['K4_K6_normal_rule_count'], nr['sensitive_under_both_rules'], r['seconds']))

print()
print('## Task 2 thresholds and tails')
print('| board | thresholds, chess rule, n=-10..10 (n: placements with result(n) != result(n+1)) | tail n<=-2 (const/period2/other) | tail n>=2 | Ka3 Pa2 ka5 |')
print('|---|---|---|---|---|')
for r in S['task2']:
    a, b = r['tails_n_minus20_to_minus2'], r['tails_n_2_to_20']
    print('| %s | %s | %d / %d / %d | %d / %d / %d | %s |' % (
        r['board'], thr(r['thresholds']), a['constant'], a['period2'], a['other'],
        b['constant'], b['period2'], b['other'], ' '.join(r['Ka3_Pa2_ka5_chess_result'] or ['-'])))

print()
print('## Task 2 placements in one set only')
print('| board | sens.+-1 not zugzwang: kpsolve pair | direction | plies to a pass-effect node | insensitive: plies to a pass-effect node |')
print('|---|---|---|---|---|')
for r in S['task2']:
    d = r['diagnostics']
    print('| %s | %s | %s | %s | %s |' % (r['board'], d['sens_pm1_not_zugzwang_by_kpsolve_pair'],
          d['sens_pm1_not_zugzwang_direction'], d['sens_pm1_not_zugzwang_plies_to_pass_effect'],
          d['insensitive_plies_to_pass_effect']))

print()
print('## Four stalemate rules (asym.py): tempo-sensitive placements (K6 definition) under each rule')
print('| board | quiet | normal play (W loses, B loses) | W draws, B loses | W loses, B draws | chess (both draw) | same set when only White\'s rule changes (both pairs) |')
print('|---|---:|---:|---:|---:|---:|---|')
for r in S['asym']:
    x = r['rules']
    print('| %s | %d | %d | %d | %d | %d | %s |' % (r['board'], r['quiet'], x['WlBl']['tempo_sensitive'], x['WdBl']['tempo_sensitive'],
          x['WlBd']['tempo_sensitive'], x['WdBd']['tempo_sensitive'],
          'yes' if all(r['same_sensitive_set'].values()) and all(r['same_pm1_set'].values()) else 'NO'))

print()
print('## Where is a single spare move needed? (explain.py, chess rule; placements that change when the pass is allowed only at the listed nodes)')
print('| board | strict-zugzwang nodes W/B (all are K+P vs K) | forced-pass nodes W/B | pass only at zugzwang nodes (optional pass): n=+1 / n=-1 differ | pass only at zugzwang + forced-pass nodes (chess rule): n=+1 / n=-1 differ | White wins with the spare move, not without: positions / spent at a zugzwang node |')
print('|---|---|---|---|---|---|')
for r in S['explain']:
    cn = r['critical_nodes']
    o1, o2 = r['mask_test optional-pass rule n=+1'], r['mask_test optional-pass rule n=-1']
    c1, c2 = r['mask_test chess rule n=+1'], r['mask_test chess rule n=-1']
    w = r['spare_move_for_White_turns_non_win_into_win']
    z = w['first_pass_node_type'].get('zugzwang/KPK', 0)
    print('| %s | %d / %d | %d / %d | %d / %d | %d / %d | %d / %d |' % (
        r['board'], cn['zugzwang_white'], cn['zugzwang_black'], cn['forced_pass_white'], cn['forced_pass_black'],
        o1['quiet_placements_that_differ'], o2['quiet_placements_that_differ'],
        c1['quiet_placements_that_differ'], c2['quiet_placements_that_differ'], w['placements_states'], z))

print()
print('## Normal play (pv_stats.py): strict-zugzwang K+P vs K placements, mask tests, how the spare-move win ends')
print('| board | off class (White stalemated) | K+P vs K strict-zugzwang placements, normal play | quiet placements that differ at n=+1 / n=-1 if the pass is allowed only at zugzwang nodes WITH a pawn | ... with NO pass | positions won only with the spare move | win ends: Black stalemated / checkmated |')
print('|---|---:|---:|---|---|---:|---|')
off = {r['board']: r['white_stalemated'] for r in S['offclass']}
for r in S['pvstats']:
    n = r['normal play']
    mt = n['mask_tests_quiet_placements_that_differ_from_the_full_result']
    e = n['spare_move_wins']['how_the_win_ends']
    print('| %s | %d | %d | %d / %d | %d / %d | %d | %d / %d |' % (
        r['board'], off[r['board']], n['zugzwang_nodes']['kpk_placements'],
        mt['zugzwang nodes with a pawn']['n=+1'], mt['zugzwang nodes with a pawn']['n=-1'],
        mt['no spare move']['n=+1'], mt['no spare move']['n=-1'], n['spare_move_wins']['states'],
        e.get('Black stalemated', 0), e.get('Black checkmated', 0)))
