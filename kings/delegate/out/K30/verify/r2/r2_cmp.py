import json, sys, collections
kind = sys.argv[1]
own = json.load(open('own_vals_%s.json' % kind))
lines = open('all_%s.txt' % kind).read().splitlines()
def rd(fn):
    out = []
    for l in open(fn):
        p, v = l.rstrip('\n').split(' | ', 1)
        out.append((p, v))
    return out
res = {}
for m, tag in (('P', 'p'), ('EPW', 'bb'), ('EPB', 'bw')):
    r = rd('mine_%s_%s.out' % (kind, tag))
    assert len(r) == len(lines)
    d = 0
    c = collections.Counter()
    for i, (p, v) in enumerate(r):
        assert p == lines[i]
        c[v.split()[0]] += 1
        if v.split()[0] != own[m][i]:
            d += 1
    print(kind, m, 'own vs mine.c(%s): positions %d differences %d' % (tag, len(r), d), dict(c))
r = rd('kpp_%s.out' % kind)
d = 0; d2 = 0
for i, (p, v) in enumerate(r):
    assert p == lines[i]
    a, b = v.split()[:2]
    if a != b: d2 += 1
    if a != own['P'][i]: d += 1
print(kind, 'own P vs kp_p --pmodel: positions %d differences %d (A!=B in %d)' % (len(r), d, d2))
