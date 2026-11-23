"""K49: x (+) {0|off} and x (+) {|{0|off}} under (N), by class.  Usage: python zoff.py W H (needs ../tmp/kn, ../tmp/zoff.t)"""
import sys, load, subprocess
from collections import Counter
W, H = int(sys.argv[1]), int(sys.argv[2]); cls = load.load(W, H); c = Counter(); ex = {}
out = subprocess.run(['../tmp/kn', str(W), str(H), 'zoff.t'], capture_output=True, text=True).stdout.splitlines()
names = out[0].split()[1:]
for ln in out[1:]:
    a, b = ln.split('|'); pos = ' '.join(a.split()); r = dict(zip(names, b.split()))
    k = cls[pos]; kb = cls.get(pos[:-1] + 'b', 'X') if pos.endswith('w') else ''
    key = (pos[-1], k, kb, r['0|off'], r['|{0|off}']); c[key] += 1; ex.setdefault(key, pos)
for k in sorted(c): print(f'cyl:{W}x{H}', k, c[k], ex[k])
