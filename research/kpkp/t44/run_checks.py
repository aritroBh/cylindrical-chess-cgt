#!/usr/bin/env python3
"""Run the second-program checks.  From the project root:
    PYTHONPATH=. .venv/bin/python -I research/kpkp/t44/run_checks.py <job> [<job> ...]
jobs:  cyl_G1 flat_G1 cyl_G2 flat_G2 cyl_G3 flat_G3   (cap 1, QRBN; expected values = the kpsolve tables)
       cyl_U0 flat_U0                  (cap 0; expected values = a fresh kpsolve --cap 0 run)
Each job writes check_<job>.out (ref output), check_<job>.json (counts, disagreements).
A job input is the random sample of the stratum plus the cylinder-only mutual-zugzwang positions whose pawn files
fall in that stratum (their cylinder value is expected on the cylinder, their flat value on the flat board).
Every process is started under nice -n 15, one at a time.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def read_exp(name):
    d = {}
    order = []
    with open(os.path.join(HERE, name)) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            pos, res = line.split(' | ')
            d[pos] = tuple(res.split())
            order.append(pos)
    return d, order


def group(pos):
    t = pos.split()
    wf, bf = t[1][1], t[3][1]
    if wf in 'ah' and bf in 'ah':
        return 'G1'
    return 'G2' if (wf in 'bdg' and bf in 'beg') else 'G3'


def run(cmd, lines, env=None):
    p = subprocess.run(['nice', '-n', '15'] + cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True,
                       cwd=ROOT, env=env)
    if p.returncode != 0:
        raise SystemExit('failed: %s\n%s' % (cmd, p.stderr[-2000:]))
    return p.stdout, p.stderr


def parse_out(text):
    d = {}
    for line in text.splitlines():
        if ' | ' in line:
            pos, res = line.split(' | ')
            d[pos.strip()] = tuple(res.split())
    return d


def main():
    env = dict(os.environ, PYTHONPATH=ROOT)
    py = os.path.join(ROOT, '.venv/bin/python')
    mz_c, mz_c_order = read_exp('chk_cyl_mz.exp')
    mz_f, _ = read_exp('chk_flat_mz.exp')
    for job in sys.argv[1:]:
        board, tag = job.split('_')
        t0 = time.time()
        if tag in ('G1', 'G2', 'G3'):
            rnd, rorder = read_exp('chk_%s_%s.exp' % (board, tag))
            mz = mz_c if board == 'cyl' else mz_f
            mzsel = [p for p in mz_c_order if group(p) == tag]
            exp = dict(rnd)
            for p in mzsel:
                exp.setdefault(p, mz[p])
            inputs = rorder + [p for p in mzsel if p not in rnd]
            cap = 1
            kinds = {p: 'random' for p in rorder}
            kinds.update({p: 'mz' for p in mzsel})        # a random position that is also an mz counts as mz too
        else:                                             # U0: cap 0, expected from kpsolve
            _, rorder = read_exp('chk_%s_U.exp' % board)
            inputs = rorder + [p for p in mz_c_order if p not in set(rorder)]
            out, err = run([os.path.join(ROOT, 'kings/kpsolve'), '--board', board + ':8x8', '--ep', 'on',
                            '--promote', 'QRBN', '--cap', '0'], inputs)
            exp = parse_out(out)
            cap = 0
            kinds = {p: 'random' for p in rorder}
            kinds.update({p: 'mz' for p in mz_c_order})
        out, err = run([py, '-m', 'kings.ref.solve', '--board', board + ':8x8', '--ep', 'on', '--promote', 'QRBN',
                        '--cap', str(cap)], inputs, env=env)
        with open(os.path.join(HERE, 'check_%s.out' % job), 'w') as f:
            f.write(out)
        got = parse_out(out)
        res = {'job': job, 'cap': cap, 'positions': len(inputs), 'seconds': round(time.time() - t0),
               'agree': 0, 'disagree': [], 'by_kind': {}}
        for p in inputs:
            ok = got.get(p) == exp.get(p)
            for k in {kinds.get(p, 'random'), 'all'}:
                bk = res['by_kind'].setdefault(k, [0, 0])
                bk[1] += 1
                bk[0] += ok
            if ok:
                res['agree'] += 1
            else:
                res['disagree'].append({'pos': p, 'expected': exp.get(p), 'ref': got.get(p)})
        with open(os.path.join(HERE, 'check_%s.json' % job), 'w') as f:
            json.dump(res, f, indent=1)
        print(json.dumps({k: v for k, v in res.items() if k != 'disagree'}), 'disagreements:', len(res['disagree']),
              flush=True)


if __name__ == '__main__':
    main()
