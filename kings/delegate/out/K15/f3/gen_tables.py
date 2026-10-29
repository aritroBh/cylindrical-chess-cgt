#!/usr/bin/env python3
"""Markdown table of every structural census run (f3/runs/*.json and v2/runs/np_*.json, cen_*.json): roots and distinct groups per class."""
import json, glob, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(glob.glob(HERE + '/runs/pA_*.json') + glob.glob(HERE + '/runs/npB_*.json')) + sorted(glob.glob(HERE + '/../v2/runs/np_*.json'))
dec = json.JSONDecoder()
rows = []
for f in files:
    s = open(f).read(); i = 0
    while i < len(s):
        while i < len(s) and s[i].isspace(): i += 1
        if i >= len(s): break
        o, j = dec.raw_decode(s, i); i = j
        nm = os.path.basename(f)[:-5]
        notion = 'B (no passes)' if ('npB' in nm or nm.startswith('np_')) else 'A (passes)'
        t, d = o['total'], o['distinct_groups']
        rows.append((o['board'], o['files'], f"{o['wmax']}+{o['bmax']}", notion, 'allowed' if o['root_passers'] == 'allowed' else 'excluded', o['roots'],
                     *[f"{t[k]} / {d[k]}" for k in ('frozen', 'on', 'off', 'dud', 'over', 'under')], nm))
rows.sort(key=lambda r: (r[0], r[1], r[3], r[4]))
print("| board | files | pawns <= | notion | root passer | roots | frozen | on | off | dud | over | under | run |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in rows: print("| " + " | ".join(str(x) for x in r) + " |")
