"""K40 step 3: x (+) T for every legal K+P v K position x on cyl:WxH (P model) and every test game T.

Runs bin/kpsum for each test family and merges the columns.  Writes data/sums_cyl_WxH.tsv.xz with
columns wk bk p stm, then one W/D column per test root, and prints the class counts (JSON).
Usage: python sums.py W H [--normal]
"""
import json, lzma, subprocess, sys, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__)) + '/..'
W, H = int(sys.argv[1]), int(sys.argv[2])
normal = '--normal' in sys.argv
TESTS = ['ints', 'on', 'off', 'dud', 'over', 'under', 'star', 'up', 'down', 'pm1']
cols, rows = [], None
for t in TESTS:
    cmd = [f'{D}/bin/kpsum', str(W), str(H), '1', t] + (['--normal'] if normal else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.splitlines()
    names = out[0].split(':', 1)[1].split()
    cols += names
    body = [l.split('|') for l in out[1:]]
    if rows is None:
        rows = [[a.strip(), b.split()] for a, b in body]
    else:
        assert len(body) == len(rows)
        for r, (a, b) in zip(rows, body):
            assert r[0] == a.strip()
            r[1] += b.split()
tag = 'normal_' if normal else ''
with lzma.open(f'{D}/data/sums_{tag}cyl_{W}x{H}.tsv.xz', 'wt') as fh:
    fh.write('pos\t' + '\t'.join(cols) + '\n')
    for a, b in rows:
        fh.write(a + '\t' + '\t'.join(b) + '\n')
print(json.dumps({'board': f'cyl:{W}x{H}', 'normal': normal, 'n': len(rows), 'cols': cols}))
