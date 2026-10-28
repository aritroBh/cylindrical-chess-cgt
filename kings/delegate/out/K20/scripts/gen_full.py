#!/usr/bin/env python3
"""Full-board test of the finite-tempo claim (K20).  Builds positions  G + H  (group + context pawns) for the
roots of class +1, -1, {1|0}, {0|-1} (flat boards, pairs Pa2 pa3 + Pc4 pc5, kings as listed) and the
prediction o(value(G) + value(H)) with cylcgt (H's value computed by cylcgt.pawns.value, BIG model).
Writes <out>.pos (kpsolve input) and <out>.pred (position -> predicted pair)."""
import sys
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames')
from cylcgt import cgt
from cylcgt.pawns import Board, Pos, value

def pair_of(g):
    o = cgt.outcome(g)   # 'L' 'R' 'N' 'P' ?
    return {'L': 'WW', 'R': 'LL', 'N': 'WL', 'P': 'LW'}[o]

board = sys.argv[1]            # flat:8x6
out = sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else 'near'
W, H = [int(x) for x in board.split(':')[1].split('x')]
B = Board(W, H, board.startswith('cyl'), True)
one = cgt.integer(1)
G = {
    '+1':    ('Kc3 ka4 Pa2 pa3 Pc4 pc5', one),
    '{1|0}': ('Kd3 ka4 Pa2 pa3 Pc4 pc5', cgt.make([one], [cgt.integer(0)])),
    '-1':    ('Ka3 kc4 Pa4 pa5 Pc2 pc3', cgt.integer(-1)),
    '{0|-1}': ('Ka3 kd4 Pa4 pa5 Pc2 pc3', cgt.make([cgt.integer(0)], [cgt.integer(-1)])),
}
# contexts: (name, kpsolve tokens, cylcgt text)
def ctx(name, toks):
    w = [t[1:] for t in toks.split() if t[0] == 'P']
    b = [t[1:] for t in toks.split() if t[0] == 'p']
    pos = Pos.parse('W: %s / B: %s' % (' '.join(w), ' '.join(b)))
    return name, toks, value(B, pos)
if mode == 'far2':
    CT = [ctx('Hp1(f)+Hm1(h)', 'Pf2 Pf4 pf5 Ph2 ph3 ph5'), ctx('Hp2', 'Pf2 Pf4 pf5 Ph2 Ph4 ph5'), ctx('Hm2', 'Pf2 pf3 pf5 Ph2 ph3 ph5'),
          ctx('Hp1+H0', 'Pf2 Pf4 pf5 Ph3 ph4'), ctx('H*+H*', 'Pf3 pf5 Ph3 ph5'), ctx('Hm1+H0', 'Pf2 pf3 pf5 Ph3 ph4'), ctx('Hp1(f)+H*(h)', 'Pf2 Pf4 pf5 Ph3 ph5')]
elif mode == 'far':
    CT = [ctx('none', ''), ctx('H0', 'Pg3 pg4'), ctx('Hp1', 'Pg2 Pg4 pg5'), ctx('Hm1', 'Pg2 pg3 pg5'), ctx('H*', 'Pg3 pg5'), ctx('H*2', 'Pg2 pg5')]
else:
  CT = [ctx('none', ''), ctx('H0', 'Pe3 pe4'), ctx('Hp1', 'Pe2 Pe4 pe5'), ctx('Hm1', 'Pe2 pe3 pe5'), ctx('H*', 'Pe3 pe5'),
      ctx('H*2', 'Pe2 pe5'), ctx('Hp2', 'Pe2 Pe4 pe5 Pg2 Pg4 pg5'), ctx('Hm2', 'Pe2 pe3 pe5 Pg2 pg3 pg5'),
      ctx('Hp1Hm1', 'Pe2 Pe4 pe5 Pg2 pg3 pg5')] if W >= 8 else \
     [ctx('none', ''), ctx('H0', 'Pe3 pe4'), ctx('Hp1', 'Pe2 Pe4 pe5'), ctx('Hm1', 'Pe2 pe3 pe5'), ctx('H*', 'Pe3 pe5'), ctx('H*2', 'Pe2 pe5')]
with open(out + '.pos', 'w') as fp, open(out + '.pred', 'w') as fq:
    for gname, (gt, gv) in G.items():
        for cname, ctoks, cv in CT:
            tot = cgt.add(gv, cv)
            pr = pair_of(tot)
            for stm in 'wb':
                pos = (gt + ' ' + ctoks).strip() + ' ' + stm + ' -'
                fp.write(pos + '\n')
                fq.write('%s | %s | %s | %s | %s\n' % (pos, gname, cname, cgt.show(cv), pr[0] if stm == 'w' else pr[1]))
print('ok')
