#!/usr/bin/env python3
"""K15 fin2: list of all distinct dud groups (readings A and B, root passers allowed or not) with the confirmation result of the P-model
runs (cf/c*.table.json written by conf2.py cmp, or the partial comparison cf/*.partial.json).  Writes dud_groups.md."""
import subprocess, json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canonlib as CL
FIN2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(FIN2, 'scripts')
def collect(board):
    out = subprocess.run(['python3', os.path.join(HERE, 'collect.py'), os.path.join(FIN2, 'runs'), 'dud', board, 'AB'], capture_output=True, text=True).stdout
    out2 = subprocess.run(['python3', os.path.join(HERE, 'collect.py'), os.path.join(FIN2, '..', 'final', 'runs'), 'dud', board, 'AB'], capture_output=True, text=True).stdout
    d = {}
    for l in (out2 + out).splitlines():
        p = l.split('\t')
        if len(p) < 5: continue
        e = d.setdefault(p[1], {'rep': p[3], 'found': set()})
        e['found'].update(p[4].split())
    return d
def confirm_table(tag, W, H):
    f = os.path.join(FIN2, 'cf', tag + '.table.json')
    if not os.path.exists(f): f = os.path.join(FIN2, 'cf', tag + 'p.table.json')
    if not os.path.exists(f): return {}
    rows = json.load(open(f)); res = {}
    for r in rows:
        k = CL.canon(CL.parse(r['group']), W, H, False)
        e = res.setdefault(k, {'n': 0, 'agree': 0, 'dis': 0, 'inexact': 0, 'missing': 0, 'bad': set(), 'ctx': set()})
        e['n'] += 1; e['ctx'].add(r['ctx']); s = r.get('status', 'missing')
        if s == 'agree': e['agree'] += 1
        elif s == 'DISAGREE': e['dis'] += 1; e['bad'].add(r['ctx'])
        elif s == 'inexact': e['inexact'] += 1
        else: e['missing'] += 1
    return res
md = []
for board, tag in (('cyl:7x6', 'c7x6'), ('cyl:8x6', 'c8x6'), ('cyl:8x8', 'c8x8')):
    W, H = map(int, board.split(':')[1].split('x'))
    d = collect(board); ct = confirm_table(tag, W, H)
    md.append('## %s: %d distinct dud groups (up to file translation, file mirror, colour flip)\n' % (board, len(d)))
    md.append('A = dud against a defender with free passes (reading A); B = dud in plain P; "no passer" = found with root passers excluded (the brief\'s filter). Confirmation: kp_p (P model, exact) beside pawn contexts on the files at distance >= 2 from the group, all king states of the shuttle closure, both sides to move; ctx = number of different contexts (1 = the empty context only: the window leaves no context file).\n')
    md.append('| # | group (representative root) | found as | confirmation beside contexts |\n|---|---|---|---|')
    for i, (c, e) in enumerate(sorted(d.items()), 1):
        readings = sorted({x.split(':')[0] for x in e['found']}); nop = any(x.split(':')[1] == 'nopasser' for x in e['found'])
        rep = ' '.join(t for t in e['rep'].split() if t not in ('w', '-'))
        res = ct.get(c)
        if res is None: txt = 'not run'
        else:
            txt = '%d/%d agree, %d ctx' % (res['agree'], res['n'], len(res['ctx']))
            if res['dis'] or res['inexact'] or res['missing']: txt += '; %d DISAGREE (contexts %s), %d inexact, %d missing' % (res['dis'], ', '.join(sorted(res['bad'])[:4]), res['inexact'], res['missing'])
        md.append('| %d | `%s` | %s%s | %s |' % (i, rep, '+'.join(readings), ', no passer' if nop else '', txt))
    md.append('')
open(os.path.join(FIN2, 'dud_groups.md'), 'w').write('\n'.join(md))
print('\n'.join(md))
