#!/usr/bin/env python3
"""K15 fin2: markdown tables of the census runs.  Source of each run: fin2/runs (own re-run, binary built from K15/grp.c) if present, else
final/runs (earlier attempt, same source: its binary is byte-identical to the rebuilt one).  Writes logs/search_table.md and logs/search_table.json"""
import json, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FIN2 = os.path.dirname(HERE)
def docs(f):
    t = open(f).read(); dec = json.JSONDecoder(); i = 0; out = []
    while i < len(t):
        while i < len(t) and t[i].isspace(): i += 1
        if i >= len(t): break
        try: o, i = dec.raw_decode(t, i)
        except Exception: break
        out.append(o)
    return out
runs = {}
for d, tag in ((os.path.join(FIN2, '..', 'final', 'runs'), 'earlier'), (os.path.join(FIN2, 'runs'), 'rerun')):
    for f in glob.glob(os.path.join(d, '*.json')):
        n = os.path.basename(f)[:-5]
        ds = docs(f)
        if not ds: continue
        # a run counts as finished only if its .done file exists (fin2) or the json has both documents
        if tag == 'rerun' and not os.path.exists(f[:-5] + '.done'): continue
        runs[n] = (tag, ds)
rows = []
for n, (tag, ds) in sorted(runs.items()):
    for o in ds:
        if o.get('mode') == 'tempo-signature': continue
        rows.append((n, tag, o))
def key(r):
    n, tag, o = r
    b = o['board']; return (b, o['files'], o['wmax'], o['bmax'], 0 if n.startswith(('pA', 'flatA')) else 1, o['root_passers'])
rows.sort(key=key)
md = ['| board | files | pawns W+B | reading | root passers | roots | frozen | on | off | dud roots (groups) | over | under | source |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
js = []
for n, tag, o in rows:
    t = o['total']; dg = o['distinct_groups']
    reading = 'A (passes)' if n.startswith(('pA', 'flatA')) else 'B (plain P)'
    md.append('| %s | %d | %d+%d | %s | %s | %d | %d | %d | %d | %d (%d) | %d | %d | %s |' % (o['board'], o['files'], o['wmax'], o['bmax'], reading, o['root_passers'], o['roots'], t['frozen'], t['on'], t['off'], t['dud'], dg['dud'], t['over'], t['under'], tag))
    js.append({'run': n, 'board': o['board'], 'files': o['files'], 'wmax': o['wmax'], 'bmax': o['bmax'], 'reading': reading[0], 'root_passers': o['root_passers'], 'roots': o['roots'],
               'frozen': t['frozen'], 'on': t['on'], 'off': t['off'], 'dud_roots': t['dud'], 'dud_groups': dg['dud'], 'over': t['over'], 'under': t['under'], 'source': tag})
tp = ['| board | files | pawns W+B | root passers | roots | all-draw signature (dud sig.) | over signature | under signature | source |', '|---|---|---|---|---|---|---|---|---|']
for n, (tag, ds) in sorted(runs.items()):
    for o in ds:
        if o.get('mode') != 'tempo-signature': continue
        t = o['total']
        tp.append('| %s | %d | %d+%d | %s | %d | %d | %d | %d | %s |' % (o['board'], o['files'], o['wmax'], o['bmax'], o['root_passers'], o['roots'], t['dud'], t['over'], t['under'], tag))
open(os.path.join(FIN2, 'logs', 'search_table.md'), 'w').write('\n'.join(md) + '\n\n' + '\n'.join(tp) + '\n')
json.dump(js, open(os.path.join(FIN2, 'logs', 'search_table.json'), 'w'), indent=0)
print('\n'.join(md)); print(); print('\n'.join(tp))
