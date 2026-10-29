def parse(s):
    t = [x for x in s.split() if len(x) >= 3 and x[0] in 'KkPp']
    return [(x[0], ord(x[1]) - 97, int(x[2:])) for x in t]
def fmt(p):
    ks = sorted(p, key=lambda z: ('KkPp'.index(z[0]), z[1], z[2]))
    return ' '.join('%s%s%d' % (c, chr(97 + f), r) for c, f, r in ks)
def canon(p, W, H, flat=False):
    best = None
    for flip in (0, 1):
        for mir in ((0, 1) if not flat else (0,)):
            q = []
            for c, f, r in p:
                if mir: f = (-f) % W
                if flip: c = c.swapcase(); r = H + 1 - r
                q.append((c, f, r))
            for tr in (range(W) if not flat else [0]):
                v = fmt([(c, (f + tr) % W, r) for c, f, r in q])
                if best is None or v < best: best = v
    return best
