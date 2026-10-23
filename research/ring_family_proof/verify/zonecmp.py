from eng import *
from red import build
def tok(fm):
    w, b = fm
    s = ''
    if w: s += 'W' + ''.join(str(r) for r in range(1, 9) if w >> (r - 1) & 1)
    if b: s += 'B' + ''.join(str(r) for r in range(1, 9) if b >> (r - 1) & 1)
    return s or '-'
for kind, n, files, fn in (('O', 17, [16, 0, 1, 2, 3, 4], 'zone_states_odd.txt'), ('E', 16, [15, 0, 1, 2, 3], 'zone_states_even.txt')):
    ids, order, info = build(ring(kind, n))
    mine = [' '.join(tok(p[f]) for f in files) for p, e in order]
    theirs = [l.strip() for l in open('/Users/aritro/Downloads/Research/Chessendgames/research/ring_family_proof/' + fn) if not l.startswith('#') and l.strip()]
    print(kind, n, 'mine', len(mine), len(set(mine)), 'theirs', len(theirs), len(set(theirs)), 'equal sets', set(mine) == set(theirs), 'first equal', mine[0] == theirs[0])
