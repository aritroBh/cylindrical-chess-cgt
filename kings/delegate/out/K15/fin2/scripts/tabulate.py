#!/usr/bin/env python3
"""tabulate census runs: each run file holds two JSON objects (variant strict = root passers excluded, passer = allowed).
usage: tabulate.py runs_dir [prefix...]"""
import sys, json, glob, os, re
d = sys.argv[1]
rows = []
for f in sorted(glob.glob(os.path.join(d, '*.json'))):
    t = open(f).read()
    dec = json.JSONDecoder(); i = 0; objs = []
    while i < len(t):
        while i < len(t) and t[i] in ' \n': i += 1
        if i >= len(t): break
        try: o, j = dec.raw_decode(t, i)
        except Exception: break
        objs.append(o); i = j
    for o in objs:
        rows.append((os.path.basename(f)[:-5], o))
print('%-18s %-9s %-7s %-4s %-5s %10s | %6s %5s %5s %5s %5s %5s | distinct dud/over' % ('run', 'board', 'files', 'w+b', 'passr', 'roots', 'frozen', 'on', 'off', 'dud', 'over', 'under'))
for name, o in rows:
    if o.get('mode') == 'tempo-signature':
        tt = o['total']
        print('%-18s %-9s %-7s %d+%d  %-5s %10d | tempo: %s' % (name, o['board'], o['files'], o['wmax'], o['bmax'], o['root_passers'][:5], o['roots'], ' '.join('%s=%d' % (k, v) for k, v in tt.items())))
        continue
    t = o['total']; dg = o.get('distinct_groups', {})
    print('%-18s %-9s %-7s %d+%d  %-5s %10d | %6d %5d %5d %5d %5d %5d | dud=%s over=%s under=%s' % (name, o['board'], o['files'], o['wmax'], o['bmax'], o['root_passers'][:5], o['roots'], t['frozen'], t['on'], t['off'], t['dud'], t['over'], t['under'], dg.get('dud'), dg.get('over'), dg.get('under')))
