"""Normal play against the chess rule on the same placements (reads chess_tempo_<board>.jsonl written by chess_scan.py).

    .venv/bin/python kings/delegate/out/K8/compare_rules.py > kings/delegate/out/K8/compare_rules.json

For every board: how the normal-rule outcome (constant over all 11 finite tests and n = -10..10, or not) is distributed
over (a) all quiet placements, (b) the chess-rule mutual zugzwangs, (c) the chess-rule tempo-sensitive placements.
Outcome codes: pair (White starts, Black starts) when it is the same for every test, e.g. 'WW'; 'varies' otherwise.
"""
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def normal_kind(r):
    s = {r['normal_finite'][i:i + 2] for i in range(0, 22, 2)} | {r['normal_n'][i:i + 2] for i in range(0, 42, 2)}
    return next(iter(s)) if len(s) == 1 else 'varies'


out = {}
for path in sorted(glob.glob(os.path.join(HERE, 'chess_tempo_*.jsonl'))):
    board = os.path.basename(path)[len('chess_tempo_'):-len('.jsonl')]
    rows = [json.loads(l) for l in open(path)]
    z = [r for r in rows if r['mutual_zugzwang']]
    cs = [r for r in rows if r['chess_sensitive']]
    ns = [r for r in rows if r['normal_sensitive']]
    out[board] = dict(
        quiet=len(rows),
        normal_outcome_all=dict(collections.Counter(normal_kind(r) for r in rows)),
        normal_outcome_of_chess_mutual_zugzwangs=dict(collections.Counter(normal_kind(r) for r in z)),
        normal_outcome_of_chess_tempo_sensitive=dict(collections.Counter(normal_kind(r) for r in cs)),
        chess_outcome_of_normal_tempo_sensitive=dict(collections.Counter(''.join(r['kpsolve']) for r in ns)),
        chess_tempo_sensitive_by_kpsolve_pair=dict(collections.Counter(''.join(r['kpsolve']) for r in cs)),
        chess_pair_all=dict(collections.Counter(''.join(r['kpsolve']) for r in rows)))
print(json.dumps(out, indent=1))
