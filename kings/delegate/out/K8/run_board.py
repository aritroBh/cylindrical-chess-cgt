"""Run one normal-play K6-style board pipeline under one runlim budget."""
import collections
import contextlib
import json
import os
import sys
import time

import gafni
import tempo_detail
import tempo_scan

HERE = os.path.dirname(os.path.abspath(__file__))


def run(board):
    tag = board.replace(':', '_')
    t0 = time.time()
    with open(os.path.join(HERE, 'log_gafni_%s.txt' % tag), 'w') as f, contextlib.redirect_stdout(f):
        gafni.main([board])

    rows = tempo_scan.scan(board)
    nj = collections.Counter(len(j) for _, _, j in rows)
    jump_at = collections.Counter(n for _, _, js in rows for n in js)
    far = [(pl, js) for pl, _, js in rows if any(j >= 2 or j <= -3 for j in js)]
    rec = dict(board=board, placements=len(rows), number_of_jumps=dict(sorted(nj.items())),
               jump_between_n_and_n_plus_1={str(k): v for k, v in sorted(jump_at.items())},
               placements_with_a_jump_beyond_pm2=len(far), examples_beyond_pm2=far[:5],
               all_profiles_constant_for_n_ge_2_and_n_le_minus_2=(not far))
    with open(os.path.join(HERE, 'tempo_scan.jsonl'), 'a') as f:
        f.write(json.dumps(rec) + '\n')
    with open(os.path.join(HERE, 'log_detail_%s.txt' % tag), 'w') as f, contextlib.redirect_stdout(f):
        tempo_detail.detail(board)
    print(json.dumps(dict(board=board, elapsed_seconds=round(time.time() - t0, 1),
                          quiet_placements=len(rows), thresholds=rec['jump_between_n_and_n_plus_1'])), flush=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: run_board.py BOARD')
    run(sys.argv[1])
