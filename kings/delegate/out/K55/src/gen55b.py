"""K55 part 2, supplementary battery (written after the first candidate scan): root A matched tiny-n for every n >= 5
tried and root B matched {0 | tiny-n}; these tests probe larger n (13 exceeds every integer in the battery, whose largest is 12) and give the order tests T = -H for those candidates.
usage: python3 gen55b.py > ../tests55b.txt"""
from games55 import G, node, integer, gsum, neg, line
def tiny(n): return node([G['0']], [node([G['0']], [integer(-n)])])
out = []
for n in (5, 6, 7, 8, 10, 12, 16, 20, 30):
    out.append(('miny%d' % n, neg(tiny(n))))
for n in (5, 12, 20, 30):
    out.append(('tiny%d' % n, tiny(n)))
for n in (5, 12, 13, 20):
    B = node([G['0']], [tiny(n)])                      # {0 | tiny-n}
    out.append(('B%d' % n, B)); out.append(('negB%d' % n, neg(B)))
for a in ('*', 'up', 'down', 'upstar', 'downstar', 'dbl_upstar', 'dbl_downstar', 'tiny2', 'miny2', 'over', 'under'):
    out.append(('miny13+%s' % a, gsum(neg(tiny(13)), G[a])))
    out.append(('negB13+%s' % a, gsum(neg(node([G['0']], [tiny(13)])), G[a])))
out.append(('miny13+negB13', gsum(neg(tiny(13)), neg(node([G['0']], [tiny(13)])))))
for name, g in out: print(line(name, g))
