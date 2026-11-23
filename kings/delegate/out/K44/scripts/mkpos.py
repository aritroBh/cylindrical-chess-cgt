#!/usr/bin/env python3
"""mkpos.py roots.txt out.pos: positions (both sides to move) of every full-pawn-set root of a kg44 --roots file, plus the D 'alone' outcome
usage: mkpos.py <roots file> <pos out> <key out> [classfilter...]"""
import sys
roots, posf, keyf = sys.argv[1:4]
cf = set(sys.argv[4:])
seen = set(); np_ = None
with open(posf, 'w') as p, open(keyf, 'w') as k:
    rows = []
    for l in open(roots):
        cn, pos, rest = l.rstrip('\n').split('|', 2)
        nm, sh, sig = rest.rsplit('|', 2)
        rows.append((cn.strip(), pos, nm, sig))
    for cn, pos, nm, sig in rows:
        if len(pos.split()) != 2 + 2 * len(cn.split()): continue
        if cf and nm.split('=')[0] not in cf: continue
        for s, side in ((0, 'w'), (1, 'b')):
            line = '%s %s -' % (pos, side)
            p.write(line + '\n'); k.write('%s | %s | %s | %s\n' % (line, nm, cn, 'WDL'[int(sig[s])]))
