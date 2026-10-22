"""K6: per-placement tempo profiles, built on tempo_scan.scan (same code, same results).

    PYTHONPATH=. nice -n 10 .venv/bin/python kings/delegate/out/K6/tempo_detail.py flat:6x4 cyl:7x4 ...

For every quiet placement x it takes
  * the 11 finite test results from <board>.jsonl (tests 0, 1, 2, -1, -2, *, up, down, 1/2, -1/2, +-1),
  * the results of x (+) n for n = -10..10 from tempo_scan.scan,
and calls the placement TEMPO-SENSITIVE if these results (a two-letter pair: White starts, Black starts) are not all
equal.  Writes tempo_detail_<board>.json: counts, thresholds (n with result(n) != result(n+1)) and every sensitive
placement with its profile.  It asserts that its jump counts equal the line tempo_scan.py printed (tempo_scan.jsonl).
"""
import collections
import json
import os
import sys

import tempo_scan
import testgames as tg

HERE = os.path.dirname(os.path.abspath(__file__))
FINITE = ['0', '1', '2', '-1', '-2', '*', 'up', 'down', '1/2', '-1/2', '+-1']      # first 11 of tg.TESTS
assert tg.TESTS[:11] == FINITE
NS = list(tempo_scan.RANGE)


def runs(profile):
    """'n<=-2: DD | n=-1: DW | n>=0: WW' style run-length text of the 21 results n = -10..10."""
    out, start = [], 0
    for i in range(1, len(profile) + 1):
        if i == len(profile) or profile[i] != profile[start]:
            a, b = NS[start], NS[i - 1]
            lab = ('n<=%d' % b if a == NS[0] else 'n>=%d' % a if b == NS[-1] else
                   'n=%d' % a if a == b else 'n=%d..%d' % (a, b))
            out.append('%s: %s' % (lab, profile[start]))
            start = i
    return ' | '.join(out)


def detail(board):
    tag = board.replace(':', '_')
    sig = {}
    for line in open(os.path.join(HERE, tag + '.jsonl')):
        r = json.loads(line)
        sig[r['placement']] = r['sig']
    rows = tempo_scan.scan(board)
    assert len(rows) == len(sig), (len(rows), len(sig))
    nj = collections.Counter(len(j) for _, _, j in rows)
    thr = collections.Counter(n for _, _, js in rows for n in js)
    fin_sens = n_sens = union_sens = 0
    sensitive = []
    for pl, prof, jumps in rows:
        s = sig[pl]
        fin = [s[2 * i:2 * i + 2] for i in range(11)]
        a = len(set(fin)) > 1
        b = len(set(prof)) > 1
        fin_sens += a
        n_sens += b
        if a or b:
            union_sens += 1
            sensitive.append(dict(placement=pl, finite_tests=dict(zip(FINITE, fin)), n_profile=runs(prof),
                                  n_profile_full=dict(zip(map(str, NS), prof)), jumps_at=jumps))
    # cross-check against the line tempo_scan.py printed for this board
    ts = [json.loads(l) for l in open(os.path.join(HERE, 'tempo_scan.jsonl'))]
    ts = [d for d in ts if d['board'] == board]
    assert len(ts) == 1, 'tempo_scan.jsonl needs exactly one line for %s' % board
    assert ts[0]['placements'] == len(rows)
    assert ts[0]['number_of_jumps'] == {str(k): v for k, v in sorted(nj.items())}, 'jump counts differ'
    assert ts[0]['jump_between_n_and_n_plus_1'] == {str(k): v for k, v in sorted(thr.items())}, 'thresholds differ'
    rec = dict(board=board, quiet=len(rows), tempo_sensitive=union_sens, sensitive_to_finite_tests=fin_sens,
               sensitive_to_n_scan=n_sens, thresholds={str(k): v for k, v in sorted(thr.items())},
               max_jump_beyond_pm2=ts[0]['placements_with_a_jump_beyond_pm2'], sensitive=sensitive)
    json.dump(rec, open(os.path.join(HERE, 'tempo_detail_%s.json' % tag), 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in rec.items() if k != 'sensitive'}), flush=True)


if __name__ == '__main__':
    for b in sys.argv[1:]:
        detail(b)
