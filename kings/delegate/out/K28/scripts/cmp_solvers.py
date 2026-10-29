"""cmp_solvers.py X.out Y.out [--moves] : compare two solver outputs (kpsolve/kq3 format) position by position.
Prints the number of positions compared, the number with different (A, B) and, with --moves, with different per-move values."""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess
args = [x for x in sys.argv[1:] if not x.startswith('--')]
mv = '--moves' in sys.argv
X = kchess.parse_kp_output(args[0]); Y = kchess.parse_kp_output(args[1])
common = sorted(set(X) & set(Y))
bad = badm = 0
from collections import Counter
cnt = Counter()
for p in common:
    ax, bx, mx = X[p]; ay, by, my = Y[p]
    cnt[(ax, bx)] += 1
    if (ax, bx) != (ay, by):
        bad += 1; print("DIFF", p, (ax, bx), (ay, by))
    elif mv and mx != my:
        badm += 1; print("MOVEDIFF", p, {k: (mx.get(k), my.get(k)) for k in set(mx) | set(my) if mx.get(k) != my.get(k)})
print(f"compared {len(common)} positions (only in first: {len(set(X)-set(Y))}, only in second: {len(set(Y)-set(X))}); (A,B) differences: {bad}; move-value differences: {badm}")
print("value pairs seen:", dict(cnt))
