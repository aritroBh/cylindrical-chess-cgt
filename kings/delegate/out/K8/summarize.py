"""Build summary.json for K8 from the persisted per-board records (run it from anywhere):

    PYTHONPATH=. .venv/bin/python kings/delegate/out/K8/summarize.py > kings/delegate/out/K8/summary.json
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from names import chess_detail_path

HERE = os.path.dirname(os.path.abspath(__file__))
NORMAL = ['cyl:5x4', 'cyl:3x7', 'cyl:5x7', 'cyl:3x8', 'cyl:4x7', 'cyl:4x8',
          'flat:4x6', 'flat:3x7', 'cyl:2x6', 'cyl:2x8', 'cyl:6x7']
CHESS = ['flat:3x4', 'flat:4x4', 'cyl:4x4', 'cyl:4x6', 'flat:5x6',
         'cyl:3x6', 'cyl:5x6', 'cyl:6x5', 'cyl:7x5']
CHESS_EXTRA = ['cyl:3x7', 'cyl:3x8', 'cyl:2x6', 'cyl:2x8']      # not in the brief: boards with no chess-rule mutual zugzwang
PREDICTED_INSENSITIVE = {'cyl:5x4', 'cyl:3x7', 'cyl:5x7', 'cyl:3x8'}
PREDICTED_SENSITIVE = {'cyl:4x7', 'cyl:4x8', 'flat:4x6', 'flat:3x7'}
# normal-play tempo-sensitive counts published in K4/K6 for the Task 2 boards (a consistency check of the
# normal-rule recomputation inside chess_scan.py)
K4K6_NORMAL = {'flat:3x4': 10, 'flat:4x4': 22, 'cyl:4x4': 24, 'cyl:4x6': 144, 'flat:5x6': 174,
               'cyl:3x6': 0, 'cyl:5x6': 0, 'cyl:6x5': 0, 'cyl:7x5': 0,
               'cyl:3x7': 0, 'cyl:3x8': 0, 'cyl:2x6': 0, 'cyl:2x8': 0}      # the last four: task 1 of this run
ZUG = 'Ka3 Pa2 ka5'


def tag(board):
    return board.replace(':', '_')


def jl(path):
    with open(path) as f:
        return [json.loads(row) for row in f]


def runs_by_label():
    out = {}
    p = os.path.join(HERE, 'runs.jsonl')
    if os.path.exists(p):
        for r in jl(p):
            out[r['label']] = r
    return out


RUNS = runs_by_label()


def normal_record(board):
    name = tag(board)
    meta = json.load(open(os.path.join(HERE, 'meta_%s.json' % name)))
    detail = json.load(open(os.path.join(HERE, 'tempo_detail_%s.json' % name)))
    rows = jl(os.path.join(HERE, name + '.jsonl'))
    off = sum('off' in r['matched'] for r in rows)         # the off / off+* class (identical signatures)
    classes = collections.Counter(r['cls'] for r in rows)
    zug = [r['chess'] for r in rows if r['placement'] == ZUG]
    prediction = None
    if board in PREDICTED_INSENSITIVE | PREDICTED_SENSITIVE:
        expected = 'insensitive' if board in PREDICTED_INSENSITIVE else 'sensitive'
        conj = 'sensitive' if off else 'insensitive'            # what the K6 conjecture says given the off class
        observed = 'sensitive' if detail['tempo_sensitive'] else 'insensitive'
        prediction = dict(expected=expected, from_off_class=conj, observed=observed,
                          confirmed=(conj == observed == expected))
    c1 = meta['check1']
    run = RUNS.get('normal ' + board, {})
    return dict(label='COMPUTED-1', board=board, rule='normal play in the whole sum (stalemate loses)',
                quiet=meta['quiet_placements'], off_class='non-empty' if off else 'empty', off_placements=off,
                tempo_sensitive=detail['tempo_sensitive'],
                sensitive_to_finite_tests=detail['sensitive_to_finite_tests'],
                sensitive_to_n_scan=detail['sensitive_to_n_scan'], thresholds=detail['thresholds'],
                max_jump_beyond_pm2=detail['max_jump_beyond_pm2'],
                classes=dict(classes),
                kpsolve_check=dict(passed=meta['check1_differences'] == 0, kpk=c1['kpk'], other=c1['other'],
                                   compared=c1['kpk'] + c1['other'], differences=meta['check1_differences']),
                mutual_zugzwangs_kpsolve=c1['mutual_zugzwangs'], Ka3_Pa2_ka5_chess_result=zug[0] if zug else None,
                prediction=prediction, sensitive_examples=detail['sensitive'][:5],
                seconds=run.get('seconds'), peak_rss_mb=run.get('peak_single_rss_mb'),
                jsonl=name + '.jsonl', tempo_detail='tempo_detail_%s.json' % name)


def chess_record(board):
    name = tag(board)
    d = json.load(open(chess_detail_path(board)))
    rows = jl(os.path.join(HERE, 'chess_tempo_%s.jsonl' % name))
    zug = [r['kpsolve'] for r in rows if r['placement'] == ZUG]
    run = RUNS.get('chess ' + board, {})
    nr = d['normal_rule_same_placements']
    return dict(label='COMPUTED-1', board=board, rule=d['rule'], quiet=d['quiet'],
                tempo_sensitive=d['tempo_sensitive'], sensitive_to_finite_tests=d['sensitive_to_finite_tests'],
                sensitive_to_n_scan=d['sensitive_to_n_scan'], thresholds=d['thresholds'],
                tails_n_minus20_to_minus2=d['tails_n_minus20_to_minus2'], tails_n_2_to_20=d['tails_n_2_to_20'],
                kpsolve_check=d['kpsolve_check'], check2=d.get('check2'),
                mutual_zugzwangs=d['mutual_zugzwangs'], sensitive_at_pm1=d['sensitive_at_pm1'],
                sensitive_at_plus1=d['sensitive_at_plus1'], sensitive_at_minus1=d['sensitive_at_minus1'],
                mutual_also_pm1=d['mutual_also_pm1'], mutual_not_pm1=d['mutual_not_pm1'],
                pm1_not_mutual=d['pm1_not_mutual'],
                mutual_not_tempo_sensitive=d['mutual_not_tempo_sensitive'],
                tempo_sensitive_not_mutual=d['tempo_sensitive_not_mutual'],
                mutual_not_pm1_examples=d['mutual_not_pm1_examples'],
                pm1_not_mutual_examples=d['pm1_not_mutual_examples'],
                diagnostics=d['diagnostics'],
                normal_rule_same_placements=nr,
                normal_rule_matches_K4_K6=(nr['tempo_sensitive'] == K4K6_NORMAL[board]),
                K4_K6_normal_rule_count=K4K6_NORMAL[board],
                Ka3_Pa2_ka5_chess_result=zug[0] if zug else None,
                sensitive_examples=d['sensitive_examples'], seconds=run.get('seconds'),
                peak_rss_mb=run.get('peak_single_rss_mb'), jsonl='chess_tempo_%s.jsonl' % name,
                tempo_detail=os.path.basename(chess_detail_path(board)))


ASYM_EXTRA = ['cyl:4x7', 'cyl:4x8', 'flat:4x6', 'flat:3x7']      # task 1 boards that have an off class


def side_file(prefix, board):
    path = os.path.join(HERE, '%s_%s.json' % (prefix, tag(board)))
    return json.load(open(path)) if os.path.exists(path) else None


def explain_record(board):
    d = side_file('explain', board)
    if d is None:
        return None
    return {k: v for k, v in d.items() if k != 'spare_move_for_White_turns_non_win_into_win'} | dict(
        spare_move_for_White_turns_non_win_into_win={
            k: v for k, v in d['spare_move_for_White_turns_non_win_into_win'].items() if k != 'examples'},
        example_lines_in='explain_%s.json' % tag(board))


if __name__ == '__main__':
    t1 = [normal_record(b) for b in NORMAL if os.path.exists(os.path.join(HERE, 'tempo_detail_%s.json' % tag(b)))]
    t2 = [chess_record(b) for b in CHESS if os.path.exists(os.path.join(HERE, 'tempo_detail_%s.json' % tag(b)))]
    t2x = [chess_record(b) for b in CHESS_EXTRA if os.path.exists(os.path.join(HERE, 'chess_tempo_%s.jsonl' % tag(b)))]
    variant = [dict(board=r['board'], rule='chess', compared=r['kpsolve_check']['compared'],
                    differences=r['kpsolve_check']['differences']) for r in t2]
    variant += [dict(board=r['board'], rule='chess (extra boards)', compared=r['kpsolve_check']['compared'],
                     differences=r['kpsolve_check']['differences']) for r in t2x]
    variant += [dict(board=r['board'], rule='normal-play scan boards (same T = 0 variant gate)',
                     compared=r['kpsolve_check']['compared'], differences=r['kpsolve_check']['differences'])
                for r in t1]
    boards = list(dict.fromkeys(NORMAL + CHESS + CHESS_EXTRA))
    off = [d for d in (side_file('offclass', b) for b in boards) if d]
    exp = [d for d in (explain_record(b) for b in CHESS + CHESS_EXTRA) if d]
    asym = [d for d in (side_file('asym', b) for b in CHESS + CHESS_EXTRA + ASYM_EXTRA) if d]
    pvs = []
    for b in CHESS + CHESS_EXTRA + ASYM_EXTRA:
        d = side_file('pvstats', b)
        if d:
            for rule in ('normal play', 'chess rule'):
                d[rule]['spare_move_wins'] = {k: v for k, v in d[rule]['spare_move_wins'].items() if k != 'examples'}
            pvs.append(d | dict(example_lines_in='pvstats_%s.json' % tag(b)))
    print(json.dumps(dict(label='COMPUTED-1', task1=t1, task2=t2, task2_extra=t2x, variant_check_T0=variant,
                          offclass=off, explain=exp, asym=asym, pvstats=pvs), indent=1, ensure_ascii=False))
