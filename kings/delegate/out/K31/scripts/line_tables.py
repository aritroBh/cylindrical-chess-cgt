import sys; sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K31/scripts')
from lk_py import *
import line_flat6 as L
from line_flat6 import *
def opt_table(st):
    x, c, s = st
    rows = []
    for k, v in L.S_[st]:
        if k == 'T': rows.append(('event %s' % ('+' if v == 1 else '-'), ''))
        else:
            (S1, w1, b1), c1, s1 = v
            if v[0] == x: mv = 'pass (reserve)'
            else: mv = ('K' + name(w1)) if s == 0 else ('k' + name(b1))
            o = L.outcome(v)
            rows.append((mv, '%s%s' % (o[0], '' if o[1] is None else o[1])))
    return rows
for title, st in [('Black to move, no reserve', (L.x, 0, 1)), ('White to move, no reserve', (L.x, 0, 0)), ('White to move, Black has one spare move', (L.x, -1, 0)), ('Black to move, Black has one spare move', (L.x, -1, 1))]:
    print('##', title, L.show(st), L.outcome(st))
    print('   ', opt_table(st))
