"""K55 part 2, third battery (written after the second scan): the loopy candidates tA = {0 || 0 | off} (root A) and
tB = {0 | tA} (root B), their negatives (for the order tests of part 2.2) and a few sums.
usage: python3 gen55c.py > ../tests55c.txt"""
from games55 import G, node, gsum, neg, line
tA = node([G['0']], [node([G['0']], [G['off']])]); tB = node([G['0']], [tA])
out = [('tA', tA), ('tB', tB), ('negtA', neg(tA)), ('negtB', neg(tB)), ('negtA+negtB', gsum(neg(tA), neg(tB))),
       ('tA+negtB', gsum(tA, neg(tB))), ('tB+negtA', gsum(tB, neg(tA)))]
for a in ('*', 'up', 'down', 'tiny2', 'miny2', 'over', 'under'):
    out.append(('negtA+%s' % a, gsum(neg(tA), G[a]))); out.append(('negtB+%s' % a, gsum(neg(tB), G[a])))
for name, g in out: print(line(name, g))
