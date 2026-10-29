#!/usr/bin/env python3
"""K26: breakdown of the exhaustive <= 3-pawn context runs by the number of context pawns.  Reads logs/f/exh (fresh) when all shards are there, else logs/exh (earlier attempt); prints markdown."""
import json, glob, ast, os, collections
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEED = {('ZB', 'cyl_8x6', 'efg'): 12, ('ZC', 'cyl_8x6', 'efg'): 12, ('ZB', 'cyl_7x6', 'ef'): 4, ('ZB', 'flat_7x6', 'efg'): 12}
print('| group | board | files | source | contexts with 0, 1, 2, 3 pawns | of which differ from the dud_D prediction (0, 1, 2, 3 pawns) |')
print('|---|---|---|---|---|---|')
for (g, b, f), n in NEED.items():
    for src, d in (('fresh', 'logs/f/exh'), ('earlier attempt', 'logs/exh')):
        fl = sorted(glob.glob(os.path.join(OUT, d, '%s_%s_%s_m3_s*of%d.json' % (g, b, f, n))))
        if len(fl) == n:
            break
    else:
        print('| %s | %s | %s | incomplete | | |' % (g, b.replace('_', ':'), f)); continue
    tot = collections.Counter(); bad = collections.Counter()
    for x in fl:
        r = json.load(open(x))['rows']
        if isinstance(r, str): r = ast.literal_eval(r)
        for row in r:
            k = len(row['W']) + len(row['B']); tot[k] += 1; bad[k] += bool(row['bad'])
    print('| %s | %s | %s | %s | %s | %s |' % (g, b.replace('_', ':'), f, src, ', '.join(str(tot[k]) for k in range(4)), ', '.join(str(bad[k]) for k in range(4))))
