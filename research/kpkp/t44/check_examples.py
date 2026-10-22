#!/usr/bin/env python3
"""Second-program check of the example positions (examples.in): kings/ref/solve.py versus the kpsolve --moves run
(examples_<board>.out).  From the project root:
    PYTHONPATH=. .venv/bin/python -I research/kpkp/t44/check_examples.py cyl|flat [examples|examples2]
Writes check_examples_<board>.txt."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
board = sys.argv[1]
stem = sys.argv[2] if len(sys.argv) > 2 else 'examples'
pos = [l.strip() for l in open(os.path.join(HERE, stem + '.in')) if l.strip() and not l.startswith('#')]
exp = {}
for l in open(os.path.join(HERE, stem + '_%s.out' % board)):
    if ' | ' in l and not l.startswith('#'):
        p, rest = l.split(' | ', 1)
        exp[p.strip()] = tuple(rest.split(' | ')[0].split())
env = dict(os.environ, PYTHONPATH=ROOT)
out = subprocess.run(['nice', '-n', '15', os.path.join(ROOT, '.venv/bin/python'), '-m', 'kings.ref.solve', '--board',
                      board + ':8x8', '--ep', 'on', '--promote', 'QRBN', '--cap', '1'],
                     input='\n'.join(pos) + '\n', capture_output=True, text=True, cwd=ROOT, env=env).stdout
got = {}
for l in out.splitlines():
    p, r = l.split(' | ')
    got[p.strip()] = tuple(r.split())
ok = sum(got.get(p) == exp.get(p) for p in pos)
lines = ['%s | kpsolve %s | ref %s | %s' % (p, ' '.join(exp.get(p, ('?',))), ' '.join(got.get(p, ('?',))),
                                          'agree' if got.get(p) == exp.get(p) else 'DISAGREE') for p in pos]
open(os.path.join(HERE, 'check_' + stem + '_%s.txt' % board), 'w').write('\n'.join(lines) + '\nagree %d of %d\n' % (ok, len(pos)))
print(board, 'agree', ok, 'of', len(pos))
