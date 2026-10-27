#!/usr/bin/env python3
"""stdin: kpp --moves output for k roots per candidate (k given), candidates file given. Prints per-candidate leak list
and summary.  leak at a root = number of legal non-shuttle moves that do not lose at once for the mover."""
import sys, json, collections
k = int(sys.argv[2]); cands = sys.argv[1]
def nm(p): return chr(96 + p[0]) + str(p[1])
hist = collections.Counter(); keep = []
lines = sys.stdin
for ci, cl in enumerate(open(cands)):
    if ci >= int(sys.argv[3]) : pass
    c = json.loads(cl)
    z = [nm(p) for p in c['W']]; w = [nm(p) for p in c['B']]
    leaks = []; illegal = False
    for r in range(k):
        line = lines.readline().rstrip('\n')
        parts = line.split(' | ')
        if parts[1].split()[0] == 'X': illegal = True; leaks.append(None); continue
        mv = parts[2].split() if len(parts) > 2 else []
        pos = parts[0].split(); side = pos[-2]
        a = pos[0][1:]; b = pos[1][1:]
        leak = 0; shuttles = 0
        for m in mv:
            name, val = m.rsplit(':', 1)
            base = name.split('=')[0]
            if base[0] == 'K':
                frm, to = base[1:3], base[3:5]
                if side == 'w' and {frm, to} == set(z): shuttles += 1; continue
                if side == 'b' and {frm, to} == set(w): shuttles += 1; continue
            want = 'L' if side == 'w' else 'W'
            if val != want: leak += 1
        if shuttles != 1: illegal = True
        leaks.append(leak)
    if illegal: hist['illegal'] += 1; continue
    hist[sum(leaks)] += 1
    if sum(leaks) == 0: keep.append(c)
print(json.dumps({'hist_total_leak_over_roots': {str(a): b for a, b in sorted(hist.items(), key=lambda t: str(t[0]))}}), file=sys.stderr)
for c in keep: print(json.dumps(c))
