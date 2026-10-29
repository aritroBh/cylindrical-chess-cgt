"""value K30's own position lists with own solver, ref3, mine.c, kp_p and compare (P, EPW, EPB)."""
import sys, subprocess, collections, os
from r2_lib import *
kind = sys.argv[1]
B = Board(kind)
lines = [l.strip() for l in open('../../logs/compare_positions_%s_8x8.txt' % kind) if l.strip()]
roots = []
illegal = 0
for l in lines:
    st = parse(B, l)
    if not legal_state(B, st): illegal += 1
    roots.append(st)
ids, states, succ, term, chk = build(B, roots)
vals = {}
for m in ('P', 'EPW', 'EPB'):
    WW, BW = solve(states, succ, term, chk, m)
    vals[m] = [value(WW, BW, ids[r]) for r in roots]
bd = 'cyl:8x8' if kind == 'cyl' else 'flat:8x8'
bd3 = 'cyl:8x8' if kind == 'cyl' else 'flat8x8'
def run(cmd, inp):
    return subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout.splitlines()
txt = '\n'.join(lines) + '\n'
r3 = [l.rsplit(' | ', 1)[1] for l in run(['bin/ref3', '--board', bd3], txt) if ' | ' in l]
kp = [l.rsplit(' | ', 1)[1].split()[0] for l in run(['bin/kpp', '--board', bd, '--pmodel'], txt) if ' | ' in l]
mine = {}
for m, tag in (('P', 'p'), ('EPW', 'bb'), ('EPB', 'bw')):
    out = []
    for i in range(0, len(lines), 4000):
        chunk = '\n'.join(lines[i:i + 4000]) + '\n'
        out += [l.rsplit(' | ', 1)[1].split()[0] for l in run(['bin/mine', '--board', bd, '--model', tag], chunk) if ' | ' in l]
    mine[m] = out
print(kind, 'list size', len(lines), 'illegal by own generator', illegal)
assert len(r3) == len(kp) == len(lines) == len(mine['P'])
print(' value sets own: ', {m: dict(collections.Counter(vals[m])) for m in vals})
print(' differences own vs ref3 (P):', sum(a != b for a, b in zip(vals['P'], r3)),
      '| own vs kp_p (P):', sum(a != b for a, b in zip(vals['P'], kp)),
      '| own vs mine.c P/EPW/EPB:', [sum(a != b for a, b in zip(vals[m], mine[m])) for m in ('P', 'EPW', 'EPB')])
