#!/usr/bin/env python3
"""SUPPLEMENTARY local search (not part of the core-in-wall enumeration).
Seeds: every ring with signature first-non-N index >= 2 found by the enumeration (the *2 rings and the NNNR near miss).
Moves: shift one pawn one rank, delete one pawn, add one pawn (any file, W ranks 2..6 / B ranks 3..7); keep rings with no passed pawn.
BFS to depth DEPTH from every ring whose first-non-N index is >= 2.  Rings are canonicalised under rotation and reflection.
usage: nbr.py DEPTH MAXEVAL > nbr_results.tsv"""
import sys, glob, os, subprocess
DEPTH = int(sys.argv[1]); MAXEVAL = int(sys.argv[2])
def parse(tok):
    if tok == '-': return (frozenset(), frozenset())
    w = set(); b = set(); m = None
    for c in tok:
        if c == 'W': m = 'w'
        elif c == 'B': m = 'b'
        else: (w if m == 'w' else b).add(int(c))
    return (frozenset(w), frozenset(b))
def fmt(fs):
    w, b = fs
    if not w and not b: return '-'
    return ('W' + ''.join(map(str, sorted(w))) if w else '') + ('B' + ''.join(map(str, sorted(b))) if b else '')
def canon(ring):
    n = len(ring); best = None
    for seq in (ring, ring[::-1]):
        for s in range(n):
            t = tuple(fmt(x) for x in seq[s:] + seq[:s])
            if best is None or t < best: best = t
    return best
def nopassed(ring):
    n = len(ring)
    for f in range(n):
        w, b = ring[f]
        nb = set().union(*[ring[(f + d) % n][1] for d in (-1, 0, 1)]); nw = set().union(*[ring[(f + d) % n][0] for d in (-1, 0, 1)])
        if any(not any(x > r for x in nb) for r in w): return False
        if any(not any(x < r for x in nw) for r in b): return False
    return True
def neighbours(ring):
    n = len(ring); out = []
    for f in range(n):
        w, b = ring[f]
        for r in w:
            for d in (-1, 1):
                r2 = r + d
                if 2 <= r2 <= 6 and r2 not in w and r2 not in b:
                    nr = list(ring); nr[f] = ((w - {r}) | {r2}, b); out.append(nr)
            nr = list(ring); nr[f] = (w - {r}, b); out.append(nr)
        for r in b:
            for d in (-1, 1):
                r2 = r + d
                if 3 <= r2 <= 7 and r2 not in w and r2 not in b:
                    nr = list(ring); nr[f] = (w, (b - {r}) | {r2}); out.append(nr)
            nr = list(ring); nr[f] = (w, b - {r}); out.append(nr)
        for r in range(2, 7):
            if r not in w and r not in b:
                nr = list(ring); nr[f] = (w | {r}, b); out.append(nr)
        for r in range(3, 8):
            if r not in w and r not in b:
                nr = list(ring); nr[f] = (w, b | {r}); out.append(nr)
    return out
def fn(sig): return next((i for i, c in enumerate(sig) if c != 'N'), None)
seeds = {}
for f in sorted(glob.glob('out/*.res')):
    for line in open(f):
        if line.startswith('HIT\t'):
            p = line.rstrip('\n').split('\t')
            k = fn(p[2])
            if k is not None and k >= 2: seeds[canon([parse(t) for t in p[1].split()])] = p[2]
seen = {c: s for c, s in seeds.items()}
frontier = [list(map(parse, c)) for c in seeds]
total = 0; stats = {}
for depth in range(1, DEPTH + 1):
    cand = {}
    for ring in frontier:
        for nr in neighbours(ring):
            if not nopassed(nr): continue
            c = canon(nr)
            if c in seen or c in cand: continue
            cand[c] = nr
    items = list(cand.items())
    if total + len(items) > MAXEVAL: items = items[:MAXEVAL - total]
    newfront = []
    for i in range(0, len(items), 3000):
        batch = items[i:i + 3000]
        inp = '\n'.join(' '.join(c) for c, _ in batch) + '\n'
        o = subprocess.run(['nice', '-n', '15', './rgq', 'solvef', '7'], input=inp, capture_output=True, text=True, env=dict(os.environ, TBITS='22'))
        lines = o.stdout.strip().split('\n')
        assert len(lines) == len(batch), (len(lines), len(batch))
        for (c, nr), l in zip(batch, lines):
            ring, sig, nodes = l.split('\t')
            seen[c] = sig; total += 1
            k = fn(sig)
            stats[sig] = stats.get(sig, 0) + 1
            if k is not None and k >= 2:
                print('\t'.join(['depth%d' % depth, ' '.join(c), sig]), flush=True)
                newfront.append(nr)
    sys.stderr.write('depth %d: evaluated %d new rings (total %d), frontier %d\n' % (depth, len(items), total, len(newfront)))
    frontier = newfront
    if total >= MAXEVAL or not frontier: break
sys.stderr.write('signature counts (first non-N >= 1 or P): ' + str({k: v for k, v in sorted(stats.items(), key=lambda x: -x[1]) if k != 'NNNNNNNN' and not k.startswith(('LL', 'RR'))}) + '\n')
