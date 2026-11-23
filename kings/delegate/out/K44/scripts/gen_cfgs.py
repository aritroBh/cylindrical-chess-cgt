#!/usr/bin/env python3
"""K44: enumerate pawn-pair configurations on cyl:WxH and write cfgfiles for kg44.
A configuration = a set of blocked pairs (file, white rank r in 2..H-2), distinct files, all files inside an arc of
at most WIN consecutive files (cyclic). Region 'free' = whole board; region box(m) = the minimal arc covering the
pawn files, widened by m files on each side (every minimal arc is a separate region when there are ties).
Canonical form: rotations and reflections of the cylinder (pawns and arc together).
usage: gen_cfgs.py W H maxwin outprefix   -> writes outprefix_free.txt, outprefix_m0.txt, _m1, _m2, and a .meta
"""
import sys, itertools
W, H, WIN, outp = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
KMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 3
ranks = list(range(2, H - 1))

def arcs_min(files):
    """all minimal covering arcs (start, length) of a set of files on a cylinder of W files"""
    best = None; res = []
    for s in range(W):
        # arc starting at s of length L covers files if every file f has (f-s)%W < L ; minimal L for this start
        L = max(((f - s) % W) for f in files) + 1
        # start must itself be a pawn file for minimality
        if s not in files: continue
        if best is None or L < best: best = L; res = [(s, L)]
        elif L == best: res.append((s, L))
    return res

def transform(pairs, arc, refl, sh):
    def tf(f): 
        g = (W - 1 - f) if refl else f
        return (g + sh) % W
    np_ = tuple(sorted((tf(f), r) for f, r in pairs))
    if arc is None: return np_, None
    s, L = arc
    if refl: s = (W - 1 - (s + L - 1))     # reflect: arc [s, s+L-1] -> [W-1-(s+L-1), W-1-s]
    s = (s + sh) % W
    return np_, (s % W, L)

def canon(pairs, arc):
    forms = []
    for refl in (0, 1):
        for sh in range(W):
            forms.append(transform(pairs, arc, refl, sh))
    return min(forms, key=lambda t: (t[0], (-1, -1) if t[1] is None else t[1]))

def span_ok(files):
    a = arcs_min(files)
    return a and a[0][1] <= WIN

singles = [(f, r) for f in range(W) for r in ranks]
cfgs = {}
for k in range(1, KMAX + 1):
    for combo in itertools.combinations(singles, k):
        files = [f for f, r in combo]
        if len(set(files)) < k: continue
        if not span_ok(files): continue
        c = canon(combo, None)[0]
        cfgs.setdefault(c, None)
out = {}
for reg in ('free', 'm0', 'm1', 'm2'):
    out[reg] = set()
for c in cfgs:
    files = [f for f, r in c]
    out['free'].add((c, None))
    for m in (0, 1, 2):
        for (s, L) in arcs_min(files):
            L2 = L + 2 * m
            if L2 >= W: continue
            out['m%d' % m].add(canon(c, ((s - m) % W, L2)))
def name(c): return ' '.join('%s%d' % (chr(97 + f), r) for f, r in c)
meta = open(outp + '.meta', 'w')
for reg, S in out.items():
    lines = []
    for (c, arc) in sorted(S, key=lambda t: (len(t[0]), t[0], (-1, -1) if t[1] is None else t[1])):
        if arc is None:
            lines.append('all|' + name(c)); continue
        s, L = arc
        c2 = tuple(sorted(((f - s) % W, r) for f, r in c))
        lines.append('0-%d|%s' % (L - 1, name(c2)))
    open('%s_%s.txt' % (outp, reg), 'w').write('\n'.join(lines) + '\n')
    byk = {}
    for (c, arc) in S: byk[len(c)] = byk.get(len(c), 0) + 1
    meta.write('%s %s lines %d by pairs %s\n' % (outp, reg, len(lines), byk))
meta.close()
print(open(outp + '.meta').read())
