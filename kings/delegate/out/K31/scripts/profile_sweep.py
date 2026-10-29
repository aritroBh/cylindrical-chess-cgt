#!/usr/bin/env python3
# K31 task 3: tempo profiles (Lw, Fw, Lb, Fb with N spare moves) of every root of many configurations; aggregates.
import subprocess, sys, re, json, os, itertools
BIN = os.path.dirname(os.path.abspath(__file__)) + '/../bin'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 12
out = open(sys.argv[1], 'w')
def configs():
    # single pairs
    for kind in ('cyl', 'flat'):
        Ws = range(5, 13) if kind == 'cyl' else (6, 7, 8)
        Hs = range(5, 9) if kind == 'cyl' else (6,)
        for H in Hs:
            for W in Ws:
                for f in (range(1) if kind == 'cyl' else range(W)):
                    for r in range(2, H - 1):
                        yield ('%s:%dx%d' % (kind, W, H), '%s%d' % (chr(97 + f), r), True)
    # two pairs
    for kind, W, H in (('cyl', 6, 6), ('cyl', 7, 6), ('cyl', 8, 6), ('flat', 6, 6), ('flat', 7, 6)):
        seen = set()
        for f1 in (range(1) if kind == 'cyl' else range(W)):
            for f2 in range(W):
                if f1 == f2: continue
                d = abs(f1 - f2)
                if kind == 'cyl': d = min(d, W - d)
                if d > 3: continue
                if kind == 'flat' and f2 < f1: continue
                for r1 in range(2, H - 1):
                    for r2 in range(2, H - 1):
                        key = (min((f1, r1), (f2, r2)), max((f1, r1), (f2, r2)))
                        if kind == 'flat' and key in seen: continue
                        seen.add(key)
                        yield ('%s:%dx%d' % (kind, W, H), '%s%d,%s%d' % (chr(97 + f1), r1, chr(97 + f2), r2), d >= 2)
agg = {}
tot = 0
for board, pairs, faithful in configs():
    o = subprocess.run(['nice', '-n', '15', BIN + '/tempo', 'profile', board, pairs, 'free', str(N)], capture_output=True, text=True).stdout
    m = re.search(r'roots (\d+)', o)
    if not m: print('FAIL', board, pairs, file=sys.stderr); continue
    for line in o.splitlines():
        mm = re.match(r'  Lw=(-?\d+) Fw=(-?\d+) Lb=(-?\d+) Fb=(-?\d+)\s+(\d+)\s+e\.g\. \[(.*?)\]  labels: (.*)', line)
        if not mm: continue
        Lw, Fw, Lb, Fb, c = map(int, mm.groups()[:5]); ex = mm.group(6)
        out.write(json.dumps({'board': board, 'pairs': pairs, 'faithful': faithful, 'Lw': Lw, 'Fw': Fw, 'Lb': Lb, 'Fb': Fb, 'n': c, 'ex': ex, 'labels': mm.group(7)}) + '\n')
        tot += c
    out.flush()
print('total roots', tot)
