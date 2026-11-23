"""K49: the odd-width fortresses: DUD positions where Black does not force Kxp against a passing White.
Runs kn with T = on and Kxp scored as a Black win (-k); D = fortress.  Prints counts and the geometry."""
import subprocess, load
from collections import Counter
def cd(a, b, W): d = (a - b) % W; return min(d, W - d)
for W, H in [(3, 6), (3, 8), (5, 6), (5, 7), (5, 8), (6, 8), (7, 6), (7, 7), (7, 8), (8, 8), (9, 6), (9, 7), (9, 8)]:
    out = subprocess.run(['../tmp/kn', str(W), str(H), 'on.t', '-k'], capture_output=True, text=True).stdout.splitlines()[1:]
    c = Counter(); n = 0
    for ln in out:
        a, r = ln.split('|')
        if r.split()[0] != 'D': continue
        n += 1; a = a.split(); (wf, wr), (bf, br), (pf, pr) = map(load.sq, a[:3])
        c[(a[3], 'wdist', cd(wf, pf, W), 'bdist', cd(bf, pf, W), 'samefile' if wf == bf else 'otherfile', 'dr', br - wr)] += 1
    print(f'cyl:{W}x{H} fortress positions {n}', dict(sorted(c.items())))
