#!/usr/bin/env python3
"""stage 'gen': read candidates (json lines) and print kpp positions for the chosen roots (1 line per root).
   stage 'filt': read kpp --moves output on stdin together with the position list file (same order), compute leaks."""
import sys, json
def nm(p): return chr(96 + p[0]) + str(p[1])
def rootstrs(c, roots):
    z = [nm(p) for p in c['W']]; w = [nm(p) for p in c['B']]
    pw = ['P' + nm(p) for p in c['wp']]; pb = ['p' + nm(p) for p in c['bp']]
    out = []
    for (a, b, s) in roots:
        out.append(' '.join(['K' + z[a], 'k' + w[b]] + pw + pb + ['w' if s == 0 else 'b', '-']))
    return out
ALL8 = [(a, b, s) for a in (0, 1) for b in (0, 1) for s in (0, 1)]
if __name__ == '__main__':
    mode = sys.argv[1]
    roots = [ALL8[0], ALL8[1]] if mode == 'gen1' else ALL8
    if mode in ('gen1', 'gen8'):
        lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
        for i, line in enumerate(open(sys.argv[2])):
            if i < lo or i >= hi: continue
            c = json.loads(line)
            for s in rootstrs(c, roots): print(s)
