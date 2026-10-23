#!/usr/bin/env python3
"""Decomposition tests with the C evaluator.
  python3 decomp.py pairs   : for each flat *3 core, remove any two pawns; report removals leaving *2, and the removed group's own value
  python3 decomp.py ring    : for the four C7 ring *3 classes, remove 1..4 pawns; report any removal leaving *2 or *3
  python3 decomp.py star2   : for the 35 flat single-component *2 cores, test whether removing 1 or 2 pawns leaves a *2
"""
import itertools, sys, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect import parse, fmt
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'h4')
def ev(positions, width, cyl=False):
    open('/tmp/_decomp_in.txt', 'w').write("\n".join(positions) + "\n")
    cmd = [H, '--cylinder' if cyl else '--flat', '--width', str(width), '--max-entries', '4194304', '--eval', '/tmp/_decomp_in.txt']
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[1:]
    res = []
    for line in out:
        p = line.split('\t'); res.append(p[4] if len(p) > 4 and p[3] in 'NLRP' else p[3] if len(p) > 3 else '?')
    return res
def removals(core, ks):
    w, b = parse(core)
    allp = [('W', p) for p in w] + [('B', p) for p in b]
    for k in ks:
        for comb in itertools.combinations(range(len(allp)), k):
            w2 = [p for i, (s, p) in enumerate(allp) if s == 'W' and i not in comb]
            b2 = [p for i, (s, p) in enumerate(allp) if s == 'B' and i not in comb]
            if w2 and b2: yield k, comb, allp, fmt(w2, b2)
mode = sys.argv[1]
nm = lambda s, p: f"{s}{chr(97+p[0])}{p[1]}"
if mode == 'pairs':
    cores = [l.strip() for l in open('seeds/cores3_all.txt')] + [l.strip() for l in open('seeds/w5p10_star3.txt')]
    for c in cores:
        rows = list(removals(c, [2])); res = ev([r[3] for r in rows], 8)
        hits = [r for r, v in zip(rows, res) if v == '2']
        for k, comb, allp, txt in hits:
            grp = sorted(allp[i] for i in comb)
            gtxt = "W: " + " ".join(nm('', p) for s, p in grp if s == 'W') + " / B: " + " ".join(nm('', p) for s, p in grp if s == 'B')
            print(c, '| removing', [nm(*allp[i]) for i in comb], 'leaves *2; the pair alone is', ev([gtxt], 8))
elif mode == 'ring':
    for c in [l.strip() for l in open('seeds/c7_reps.txt')]:
        found = []
        for k in (1, 2, 3, 4):
            rows = list(removals(c, [k])); res = ev([r[3] for r in rows], 7, True)
            found += [([nm(*r[2][i]) for i in r[1]], v) for r, v in zip(rows, res) if v in ('2', '3')]
        print(c, '| removals (<=4 pawns) leaving *2/*3:', found if found else 'none')
elif mode == 'star2':
    cores = [l.strip() for l in open('seeds/cores2_all.txt')]
    red = 0
    for c in cores:
        rows = list(removals(c, [1, 2])); res = ev([r[3] for r in rows], 8)
        red += any(v == '2' for v in res)
    print(len(cores), 'cores;', red, 'reducible by removing 1-2 pawns to a *2')
