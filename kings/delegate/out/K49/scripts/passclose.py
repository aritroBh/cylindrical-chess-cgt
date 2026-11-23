"""K49 Lemma P check: for every placement legal with both sides to move, r_N(y_b) = W implies r_N(y_w) = W.
Reads kn output with root 0 on stdin; prints counts and violations."""
import sys
r = {}
for ln in sys.stdin:
    if ln.startswith('#'): continue
    a, b = ln.split('|'); a = a.split(); r[(a[0], a[1], a[2], a[3])] = b.split()[0]
pl = {k[:3] for k in r}
both = [k for k in pl if (*k, 'w') in r and (*k, 'b') in r]
viol = [k for k in both if r[(*k, 'b')] == 'W' and r[(*k, 'w')] != 'W']
wb = sum(1 for k in both if r[(*k, 'b')] == 'W')
print(sys.argv[1], 'placements', len(both), 'Black-to-move wins', wb, 'violations', len(viol), ' '.join(' '.join(v) for v in viol[:4]))
