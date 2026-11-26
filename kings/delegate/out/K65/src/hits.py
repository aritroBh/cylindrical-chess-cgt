"""K65: collect the exact over groups of the flat 8x8 searches.  A = p45a (over orientation, 'HIT sh=1' lines);
R = r48 (under orientation; each hit is colour-mirrored, rank r -> 9 - r, into the over frame).  Prints, per class,
whether A and R give the same set, then the distinct groups (a group with pawns on <= 2 files lies in several classes)
grouped up to left-right reflection and file translation.
usage: hits.py <A out> <R out> [<A out> <R out> ...]"""
import lzma, re, sys
H = 8
def rd(p): return (lzma.open(p, 'rt') if p.endswith('.xz') else open(p)).read()
def sq(s): return ord(s[0]) - 97, int(s[1:])
def nm(f, r): return chr(97 + f) + str(r)
def key(men, z):   # men: frozenset of (piece letter, file, rank) without the Black king; z: frozenset of 2 squares
    return (men, z)
def fromA(line):
    m = re.match(r'HIT sh=1 (.*) b -\s+shuttle (\w\d)(\w\d)', line)
    toks = m.group(1).split(); z0, z1 = sq(m.group(2)), sq(m.group(3))
    men = frozenset((t[0], *sq(t[1:])) for t in toks if t[0] != 'k')
    return key(men, frozenset([z0, z1]))
def fromR(line):
    m = re.match(r'HIT under: shuttle (\w\d)-(\w\d), Black king (\w\d),(.*)', line)
    mir = lambda s: (sq(s)[0], H + 1 - sq(s)[1])
    z = frozenset([mir(m.group(1)), mir(m.group(2))])
    men = {('K', *mir(m.group(3)))}
    for t in m.group(4).split(): men.add(('p' if t[0] == 'P' else 'P', *mir(t[1:])))
    return key(frozenset(men), z)
def show(k):
    men, z = k
    z0, z1 = sorted(z, key=lambda s: (s[1], s[0]))
    order = lambda x: ('KkPp'.index(x[0]), x[1], x[2])
    allm = sorted(list(men) + [('k', *z0)], key=order)
    return ' '.join(p + nm(f, r) for p, f, r in allm), nm(*z1)
def shape(k):
    men, z = k
    best = None
    for refl in (0, 1):
        tf = (lambda f: 7 - f) if refl else (lambda f: f)
        ms = [(p, tf(f), r) for p, f, r in men] + [('z', tf(f), r) for f, r in z]
        lo = min(f for _, f, _ in ms)
        s = tuple(sorted((p, f - lo, r) for p, f, r in ms))
        best = s if best is None or s < best else best
    return best
allk = {}
args = sys.argv[1:]
for i in range(0, len(args), 2):
    a = {fromA(l) for l in rd(args[i]).splitlines() if l.startswith('HIT sh=1')}
    r = {fromR(l) for l in rd(args[i + 1]).splitlines() if l.startswith('HIT under')}
    print('%s: A %d hits, R %d hits, %s' % (args[i], len(a), len(r), 'same set' if a == r else 'DIFFER'))
    for k in a | r: allk.setdefault(k, []).append(args[i].split('_f')[-1].split('.')[0])
shapes = {}
for k in allk: shapes.setdefault(shape(k), []).append(k)
print('%d distinct exact over groups, %d up to reflection and file translation' % (len(allk), len(shapes)))
for n, (s, ks) in enumerate(sorted(shapes.items(), key=lambda kv: (len(kv[1][0][0]), show(kv[1][0])))):
    for k in sorted(ks, key=show):
        g, z1 = show(k); nw = sum(1 for p in k[0] if p[0] == 'P'); nb = sum(1 for p in k[0] if p[0] == 'p')
        print('shape %d  %s  /%s  pawns %d+%d men %d  classes %s' % (n + 1, g, z1, nw, nb, nw + nb + 2, ','.join(sorted(set(allk[k])))))
