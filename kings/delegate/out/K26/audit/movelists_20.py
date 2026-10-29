#!/usr/bin/env python3
"""K26: readable root values and move lists of the 20 selected groups (both colour orientations), from logs/f/confirm/confirm_final.json (kpp and ref3m agree at every line listed)."""
import json, os
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(OUT, 'logs', 'f', 'confirm', 'confirm_final.json')))
o = open(os.path.join(OUT, 'audit', 'movelists_20groups.txt'), 'w')
print('# 20 groups, kpp --pmodel and ref3m (fresh build); each root as "position | value | moves with the value after the move, White view"; both orientations (the second is the colour mirror, ranks flipped)', file=o)
for g in d['groups']:
    print('\n## %s  (%s, %s)  all_agree=%s  flip-symmetry roots %s' % (g['id'], g['board'], g['class'], g['all_agree'], g['flip_symmetry_ok_roots']), file=o)
    for r in g['roots']:
        print('%s | %s | %s | kpp=ref3m: value %s moves %s' % (r['pos'], r['value'], r['moves'], r['value_agree'], r['moves_agree']), file=o)
o.close()
print(sum(len(g['roots']) for g in d['groups']), 'roots written')
