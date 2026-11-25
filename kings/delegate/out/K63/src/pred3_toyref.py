"""K63: third check of the omega prediction with the K57 referee's toyref.over_vals, for contexts whose X can never
create an e.p. right (ep 0 in the .pred file; the T format has no e.p. clearing).  usage: python3 pred3_toyref.py <tag>"""
import sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from toyref import over_vals, WT, BT  # noqa: E402

tag = sys.argv[1]
tg = {}
for line in open('in/ctx_%s.tg' % tag):
    name, k, body = line.rstrip('\n').split('|')
    L, R = [], []
    for part in body.split(';')[:int(k)]:
        a, b = part.split('/')
        conv = lambda x: [WT if t == 'W' else BT if t == 'B' else int(t) for t in x.split(',') if t]  # noqa: E731
        L.append(conv(a)); R.append(conv(b))
    tg[name] = (L, R)
n = bad = skip = 0
for line in open('in/ctx_%s.pred' % tag):
    t = line.split()
    name = t[0]
    rest = line.split('] ', 1)[1].split()
    if rest[rest.index('ep') + 1] == '1':
        skip += 1; continue
    ov = over_vals(tg[name])
    got = (ov[(0, 0, 0)], ov[(0, 0, 1)])
    want = (rest[2], rest[4])
    n += 1
    if got != want:
        bad += 1; print('DIFF', line.strip(), 'toyref', got)
print('%d contexts compared (%d with an e.p. possibility skipped), %d differ' % (n, skip, bad))
