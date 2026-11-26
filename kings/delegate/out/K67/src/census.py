"""K67: census of exact over groups from the p45a hit lists (over orientation) of the four classes.
Uses recount.py's parser and canonical form (K65 referee).  Writes in/groups_new.txt (groups not among K65's 38,
lines name|pieces with Black king on z0|z0|z1) and prints the tables.
usage: census.py <A abe> <A ade> <A bcf> <A bef> [<R abe> <R ade>]"""
import sys, re, lzma
def opn(f): return lzma.open(f, 'rt') if f.endswith('.xz') else open(f)
def sq(s): return (ord(s[0]) - 97, int(s[1:]))
def n(p): return chr(97 + p[0]) + str(p[1])
def parseA(f):
    out = {}
    for l in opn(f):
        if not l.startswith('HIT sh=1'): continue
        m = re.match(r'HIT sh=\d+ (.*?) [bw] - +shuttle ([a-h]\d)([a-h]\d)', l)
        pcs, z0, z1 = m.groups(); toks = pcs.split()
        wk = [sq(t[1:]) for t in toks if t[0] == 'K'][0]
        wp = frozenset(sq(t[1:]) for t in toks if t[0] == 'P'); bp = frozenset(sq(t[1:]) for t in toks if t[0] == 'p')
        out[(wk, frozenset([sq(z0), sq(z1)]), wp, bp)] = (pcs, z0, z1)
    return out
def parseR(f):
    out = set()
    for l in opn(f):
        m = re.match(r'HIT under: shuttle ([a-h]\d)-([a-h]\d), Black king ([a-h]\d), (.*)', l)
        if not m: continue
        z0, z1, bk, pcs = m.groups(); toks = pcs.split(); fl = lambda p: (p[0], 9 - p[1])
        wp = frozenset(fl(sq(t[1:])) for t in toks if t[0] == 'p'); bp = frozenset(fl(sq(t[1:])) for t in toks if t[0] == 'P')
        out.add((fl(sq(bk)), frozenset([fl(sq(z0)), fl(sq(z1))]), wp, bp))
    return out
def canon(g):
    wk, z, wp, bp = g; best = None
    for refl in (0, 1):
        for d in range(-7, 8):
            t = lambda p: ((7 - p[0] if refl else p[0]) + d, p[1])
            pts = [t(wk)] + [t(p) for p in z] + [t(p) for p in wp] + [t(p) for p in bp]
            if any(not 0 <= p[0] <= 7 for p in pts): continue
            key = (t(wk), tuple(sorted(t(p) for p in z)), tuple(sorted(t(p) for p in wp)), tuple(sorted(t(p) for p in bp)))
            if best is None or key < best: best = key
    return best
def name(g):
    wk, z, wp, bp = g; zz = sorted(z, key=lambda p: (p[1], p[0]))
    return 'K%s k%s/%s %s %s' % (n(wk), n(zz[0]), n(zz[1]), ' '.join('P' + n(p) for p in sorted(wp)), ' '.join('p' + n(p) for p in sorted(bp)))
men = lambda g: 2 + len(g[2]) + len(g[3])
A = [parseA(f) for f in sys.argv[1:5]]; lab = ['{a,b,e}', '{a,d,e}', '{b,c,f}', '{b,e,f}']
for l, a in zip(lab, A): print('p45a %s: %d exact over groups' % (l, len(a)))
if len(sys.argv) > 6:
    for i, f in enumerate(sys.argv[5:7]):
        R = parseR(f); print('r48 %s: %d hits, same set as p45a: %s' % (lab[i], len(R), R == set(A[i])))
        if R != set(A[i]): print('  only p45a:', [name(g) for g in set(A[i]) - R], ' only r48:', [name(g) for g in R - set(A[i])])
old = set(A[2]) | set(A[3]); new = set(A[0]) | set(A[1]); U = old | new
print('K65 (two classes): %d distinct; K67 classes: %d distinct, %d of them not among K65\'s 38; in both K67 classes: %d' % (len(old), len(new), len(new - old), len(set(A[0]) & set(A[1]))))
print('four classes: %d distinct groups, %d up to reflection and file translation' % (len(U), len({canon(g) for g in U})))
print('new shapes (not a reflection/translation of a K65 group): %d' % len({canon(g) for g in new} - {canon(g) for g in old}))
for m in sorted({men(g) for g in U}):
    gs = [g for g in U if men(g) == m]; ns = [g for g in gs if g not in old]
    print('  men %d: %d groups (%d new), %d shapes (%d new shapes)' % (m, len(gs), len(ns), len({canon(g) for g in gs}), len({canon(g) for g in ns} - {canon(g) for g in old})))
print('per class: groups also in another class:')
for l, a in zip(lab, A): print('  %s %d, of which also in another of the four classes %d' % (l, len(a), sum(1 for g in a if sum(g in b for b in A) > 1)))
print('new groups:')
rows = []
for i, (cl, a) in enumerate(zip(('C014', 'C034'), A[:2])):
    for k, g in enumerate(sorted(a, key=lambda g: (men(g), name(g)))):
        pcs, z0, z1 = a[g]; tag = '%s_%02d' % (cl, k + 1)
        dup = 'K65 group' if g in old else ('= C014 group' if i == 1 and g in A[0] else '')
        shp = 'shape known from K65' if canon(g) in {canon(h) for h in old} else 'new shape'
        print('  %s  %s  men %d  %s  %s' % (tag, name(g), men(g), shp, dup))
        if not dup: rows.append('%s|%s|%s|%s' % (tag, pcs, z0, z1))
open('in/groups_new.txt', 'w').write('\n'.join(rows) + '\n')
print('%d groups to classify -> in/groups_new.txt' % len(rows))
