# K65 referee: recount of the census from the raw hit lists (p45a over-orientation output, r48 under-orientation output).
# usage: python3 recount.py A125.out A145.out R125.out [R145.out]
import sys, re, lzma
def opn(f): return lzma.open(f, 'rt') if f.endswith('.xz') else open(f)
def sq(s): return (ord(s[0]) - 97, int(s[1:]))
def parseA(f):
    out = set()
    for l in opn(f):
        if not l.startswith('HIT'): continue
        m = re.match(r'HIT sh=\d+ (.*?) [bw] - +shuttle ([a-h]\d)([a-h]\d)', l)
        pcs, z0, z1 = m.groups(); toks = pcs.split()
        wk = [sq(t[1:]) for t in toks if t[0] == 'K'][0]
        wp = frozenset(sq(t[1:]) for t in toks if t[0] == 'P'); bp = frozenset(sq(t[1:]) for t in toks if t[0] == 'p')
        out.add((wk, frozenset([sq(z0), sq(z1)]), wp, bp))
    return out
def parseR(f):  # under orientation: White king shuttles, Black king fixed; mirror colours and ranks into the over frame
    out = set()
    for l in opn(f):
        m = re.match(r'HIT under: shuttle ([a-h]\d)-([a-h]\d), Black king ([a-h]\d), (.*)', l)
        if not m: continue
        z0, z1, bk, pcs = m.groups(); toks = pcs.split()
        fl = lambda p: (p[0], 9 - p[1])
        wp = frozenset(fl(sq(t[1:])) for t in toks if t[0] == 'p'); bp = frozenset(fl(sq(t[1:])) for t in toks if t[0] == 'P')
        out.add((fl(sq(bk)), frozenset([fl(sq(z0)), fl(sq(z1))]), wp, bp))
    return out
def canon(g):
    wk, z, wp, bp = g; best = None
    for refl in (0, 1):
        for d in range(-7, 8):
            def t(p):
                f = 7 - p[0] if refl else p[0]; return (f + d, p[1])
            pts = [t(wk)] + [t(p) for p in z] + [t(p) for p in wp] + [t(p) for p in bp]
            if any(not 0 <= p[0] <= 7 for p in pts): continue
            key = (t(wk), tuple(sorted(t(p) for p in z)), tuple(sorted(t(p) for p in wp)), tuple(sorted(t(p) for p in bp)))
            if best is None or key < best: best = key
    return best
def name(g):
    wk, z, wp, bp = g; n = lambda p: chr(97 + p[0]) + str(p[1]); zz = sorted(z)
    return 'K%s k%s/%s %s %s' % (n(wk), n(zz[0]), n(zz[1]), ' '.join('P' + n(p) for p in sorted(wp)), ' '.join('p' + n(p) for p in sorted(bp)))
A125, A145, R125 = parseA(sys.argv[1]), parseA(sys.argv[2]), parseR(sys.argv[3])
print('p45a {b,c,f}:', len(A125), ' p45a {b,e,f}:', len(A145), ' r48 {b,c,f}:', len(R125), ' r48 = p45a on {b,c,f}:', R125 == A125)
if len(sys.argv) > 4:
    R145 = parseR(sys.argv[4]); print('r48 {b,e,f}:', len(R145), ' r48 = p45a on {b,e,f}:', R145 == A145)
    if R145 != A145: print('  only p45a:', [name(g) for g in A145 - R145], '  only r48:', [name(g) for g in R145 - A145])
U = A125 | A145
print('distinct:', len(U), ' in both classes:', len(A125 & A145), ' up to reflection and file translation:', len({canon(g) for g in U}))
for men in sorted({2 + len(g[2]) + len(g[3]) for g in U}):
    gs = [g for g in U if 2 + len(g[2]) + len(g[3]) == men]
    print('men %d: %d groups, %d shapes' % (men, len(gs), len({canon(g) for g in gs})))
    if men == 6:
        for g in sorted(gs, key=canon): print('   ', name(g), ' shape', sorted({canon(h) for h in U}).index(canon(g)) + 1 if False else '', 'canon', canon(g)[0])
