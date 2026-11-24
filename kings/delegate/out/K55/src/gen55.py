"""K55 part 2: the enlarged battery (new single games, then every sum of three atoms of the reduced list, zeros dropped,
skipping the sums already in K47's 275 tests).  usage: python3 gen55.py > ../tests55.txt"""
import itertools
from games55 import G, NEW_SINGLES, ATOMS, gsum, line
BASE275 = {'0', '*', 'up', 'down', 'pm1', '1', '-1', 'over', 'under'}
out = []
for n in NEW_SINGLES: out.append((n, G[n]))
for combo in itertools.combinations_with_replacement(ATOMS, 3):
    nz = [a for a in combo if a != '0']
    if not nz: continue
    if len(nz) <= 2 and all(a in BASE275 for a in nz): continue      # already among the 275
    if len(nz) == 1 and nz[0] in NEW_SINGLES: continue                # already a new single
    out.append(('+'.join(nz), gsum(*[G[a] for a in nz])))
for name, g in out: print(line(name, g))
