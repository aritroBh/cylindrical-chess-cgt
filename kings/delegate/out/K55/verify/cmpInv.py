"""K55 referee: compare rv55 root results with the investigator's za outputs for the same test games (by name map)."""
import re
names = {'0': '0', '*': '*', 'up': 'up', 'down': 'down', 'down+*': '*+down', 'up+*': '*+up', 'under': 'under',
         'under+*': '*+under', 'over': 'over', 'over+*': '*+over', 'down+down': 'down+down', 'under+up': 'up+under',
         'under+down': 'down+under', 'under+under': 'under+under', '1+pm1': '1+pm1', 'pm1': 'pm1', '1': '1', '-1': '-1',
         'on': 'on', 'off': 'off', 'dud': 'dud', 'over+down': 'down+over', 'miny2': 'miny2', 'tiny2': 'tiny2',
         'dblup*': 'dbl_upstar', 'dbldown*': 'dbl_downstar', '-2': '-2', '-3': '-3', '-4': '-4', '-5': '-5', '-6': '-6'}
def inv(files):
    d = {}
    for fn in files:
        for l in open(fn):
            t = [x.strip() for x in l.split('|')]
            if len(t) < 6: continue
            d.setdefault(t[0], {})[(t[1], t[2])] = (t[3][-1], t[4][-1])
    return d
def mine(fn, roots):
    d = {}
    for l in open(fn):
        if l.startswith(' '): continue
        t = [x.strip() for x in l.split('|')]
        for r, c in zip(roots, t[1:]):
            c = c.split()[0]; d.setdefault(t[0], {})[(r, 'w')] = c[0]; d[t[0]][(r, 'b')] = c[1]
    return d
import sys
for grp, myfiles, invfiles, rootf in [
    ('H10', ['logs/main_H10.out', 'logs/tempo_H10.out'], ['../logs/p1_za_H10.out', '../logs/p1x_za_H10_tests55.out'], 'roots_H10.txt'),
    ('Z_O', ['logs/main_G8.out', 'logs/tempo_G8.out'], ['../../K47/logs/full_A_N.out', '../logs/p2_za_G8.out'], 'roots_G8.txt')]:
    roots = [l.strip() for l in open(rootf) if l.strip()]
    I = inv(invfiles); M = {}
    for f in myfiles: M.update(mine(f, roots))
    n = d = nov = miss = 0
    for my, iv in names.items():
        if my not in M: continue
        if iv not in I: miss += 1; print(grp, 'not in investigator logs:', iv); continue
        for k, v in M[my].items():
            z, o = I[iv][k]; n += 1
            if v != z: d += 1; print(grp, 'DIFF', my, k, 'mine', v, 'za', z)
            if v != o: nov += 1
    print('%s: %d results compared with za, %d differ; %d of them differ from over' % (grp, n, d, nov))
