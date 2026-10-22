"""K6: one summary record per board, from the files the pipeline wrote.

    PYTHONPATH=. .venv/bin/python kings/delegate/out/K6/summarize.py flat:6x4 cyl:7x4 ... > summary.json

Reads meta_<board>.json, <board>.jsonl, tempo_detail_<board>.json, runs.jsonl.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sig_kind(sig):
    pairs = {sig[i:i + 2] for i in range(0, len(sig), 2)}
    return pairs.pop() if len(pairs) == 1 else None


def summarize(board):
    tag = board.replace(':', '_')
    meta = json.load(open(os.path.join(HERE, 'meta_%s.json' % tag)))
    rows = [json.loads(l) for l in open(os.path.join(HERE, tag + '.jsonl'))]
    td = json.load(open(os.path.join(HERE, 'tempo_detail_%s.json' % tag)))
    c = collections.Counter()
    for r in rows:
        if r['cls'] == 'unmatched':
            c['unmatched, T-independent' if sig_kind(r['sig']) else 'unmatched, T-dependent'] += 1
        else:
            c[r['cls']] += 1
    runs = [json.loads(l) for l in open(os.path.join(HERE, 'runs.jsonl'))]
    mine = [r for r in runs if r['label'] in ('gafni ' + board, 'tempo_scan ' + board)]
    ck = meta['check1']
    out = dict(board=board, quiet=meta['quiet_placements'], nodes=meta['nodes'], edges=meta['edges'],
               kpk_positions=meta['kpk_positions'], kpsolve_kpk=ck['kpk'], kpsolve_other=ck['other'],
               kpsolve_compared=ck['kpk'] + ck['other'], kpsolve_diffs=meta['check1_differences'],
               tempo_sensitive=td['tempo_sensitive'], sens_finite_tests=td['sensitive_to_finite_tests'],
               sens_n_scan=td['sensitive_to_n_scan'], thresholds=td['thresholds'],
               WHITE_WINS_ALL=c['WHITE-WINS-ALL'], BLACK_WINS_ALL=c['BLACK-WINS-ALL'], on=c['on/on+*'],
               off=c['off/off+*'], dud=c['dud'], unmatched_Tdep=c['unmatched, T-dependent'],
               unmatched_Tindep=c['unmatched, T-independent'],
               other_classes={k: v for k, v in c.items() if k not in (
                   'WHITE-WINS-ALL', 'BLACK-WINS-ALL', 'on/on+*', 'off/off+*', 'dud', 'unmatched, T-dependent',
                   'unmatched, T-independent')},
               seconds=round(sum(r['seconds'] for r in mine), 1),
               gafni_seconds=meta['seconds'],
               peak_rss_mb=max([r.get('tree_maxrss_mb', 0) for r in mine] + [0]),
               peak_polled_rss_mb=max([r['peak_single_rss_mb'] for r in mine] + [0]),
               peak_polled_total_mb=max([r['peak_total_rss_mb'] for r in mine] + [0]))
    assert sum(c.values()) == out['quiet']
    return out


if __name__ == '__main__':
    print(json.dumps([summarize(b) for b in sys.argv[1:]], indent=1))
