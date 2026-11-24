"""K48 referee, claim 1: read the raw cap-1 outputs (kp39 --refine: 'A: ... | B: ...'; own39: one file per bound) and
count exact / open move values.  Bound A scores a capped promotion as a White win (an upper bound for White), bound B as a
Black win (a lower bound).  A value is exact iff A == B.  A move loses at once for the mover iff its exact value is the
opponent's win.
usage: p1_check.py <kp39-style out (A and B lists)> <own39 bound A out> <own39 bound B out>"""
import sys

def kp(path):
    d = {}
    for line in open(path):
        if ' | ' not in line: continue
        p = [x.strip() for x in line.rstrip('\n').split(' | ')]
        a, b = p[1].split()
        if len(p) > 3:
            ma = dict(x.rsplit(':', 1) for x in p[2][2:].split()); mb = dict(x.rsplit(':', 1) for x in p[3][2:].split())
        else:
            ma = mb = dict(x.rsplit(':', 1) for x in p[2].split())
        d[p[0]] = ((a, b), {m: (ma[m], mb[m]) for m in ma})
    return d

def own(pa, pb):
    d = {}
    A = {}; B = {}
    for path, T in ((pa, A), (pb, B)):
        for line in open(path):
            if ' | ' not in line: continue
            p = [x.strip() for x in line.rstrip('\n').split(' | ')]
            T[p[0]] = (p[1], dict(x.rsplit(':', 1) for x in p[2].split()) if len(p) > 2 else {})
    for pos in A:
        d[pos] = ((A[pos][0], B[pos][0]), {m: (A[pos][1][m], B[pos][1][m]) for m in A[pos][1]})
    return d

K = kp(sys.argv[1])
O = own(sys.argv[2], sys.argv[3])
diff = 0; n = ex = 0; cnt = {}
for pos in K:
    stm = pos.split()[-2]
    if K[pos][0] != O[pos][0]: diff += 1
    if set(K[pos][1]) != set(O[pos][1]): diff += 1
    print('%s  root bounds kp39 %s own39 %s' % (pos, K[pos][0], O[pos][0]))
    for m, ab in sorted(K[pos][1].items()):
        n += 1
        if O[pos][1].get(m) != ab: diff += 1
        a, b = ab
        if a == b:
            ex += 1
            lose = a == ('L' if stm == 'w' else 'W')
            tag = 'loses' if lose else ('wins' if a == ('W' if stm == 'w' else 'L') else 'draw')
        else:
            tag = 'open (%s,%s)' % (a, b)
        cnt[tag] = cnt.get(tag, 0) + 1
        print('    %-8s kp39 %s own39 %s  %s' % (m, ab, O[pos][1].get(m), tag))
print('moves %d exact %d  %s  differences kp39/own39 %d' % (n, ex, cnt, diff))
