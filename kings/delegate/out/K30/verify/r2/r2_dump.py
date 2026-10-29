"""dump every reachable state from X (own generator) with own P/EPW/EPB values; compare with ref3 (P) over ALL of them."""
import sys, subprocess, collections
from r2_lib import *
kind = sys.argv[1]
B = Board(kind)
X = parse(B, 'Ke6 Pd7 kd8 pe7 w -')
ids, states, succ, term, chk = build(B, [X])
vals = {}
for m in ('P', 'EPW', 'EPB'):
    WW, BW = solve(states, succ, term, chk, m)
    vals[m] = [value(WW, BW, i) for i in range(len(states))]
lines = [fmt(s) for s in states]
open('all_%s.txt' % kind, 'w').write('\n'.join(lines) + '\n')
import json
json.dump(vals, open('own_vals_%s.json' % kind, 'w'))
bd = 'cyl:8x8' if kind == 'cyl' else 'flat8x8'
out = subprocess.run(['bin/ref3', '--board', bd], input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.splitlines()
res = [l for l in out if ' | ' in l]
assert len(res) == len(lines), (len(res), len(lines))
diff = 0
cnt = collections.Counter()
for i, l in enumerate(res):
    pos, v = l.rsplit(' | ', 1)
    assert pos == lines[i], (pos, lines[i])
    cnt[(vals['P'][i], v)] += 1
    if v != vals['P'][i]:
        diff += 1
print(kind, 'states', len(lines), 'ref3 vs own P: differences', diff, dict(cnt))
