"""K55: compare za and rz on one group: usage python3 compare55.py <za.out> <rz.out> <tests file> [more za rz tests triples]
za line:  name | root | side | Z x | over y | MATCH ;  rz line: name | (w b) root 0 | (w b) root 1   (White's view)
Prints: za = rz count, za's over column checked against games55.solve, and every result where Z differs from over."""
import sys
from games55 import readT, rsolve2, G
def read_za(fn):
    d = {}; roots = []
    for l in open(fn):
        p = [x.strip() for x in l.split('|')]
        if len(p) < 6: continue
        if p[1] not in roots: roots.append(p[1])
        d[(p[0], roots.index(p[1]), p[2])] = (p[3].split()[1], p[4].split()[1])
    return d
def read_rz(fn):
    d = {}
    for l in open(fn):
        p = [x.strip() for x in l.split('|')]
        if len(p) < 3 or len(p[1]) != 2: continue
        for r in range(len(p) - 1):
            d[(p[0], r, 'w')] = p[1 + r][0]; d[(p[0], r, 'b')] = p[1 + r][1]
    return d
if __name__ == '__main__':
    args = sys.argv[1:]
    for k in range(0, len(args), 3):
        za, rz, tf = read_za(args[k]), read_rz(args[k + 1]), readT(args[k + 2])
        same = diff = missing = 0; badover = 0; zdiff = []
        for name, T in tf:
            ov = rsolve2(G['over'], T)
            for r in (0, 1):
                for s, si in (('w', 0), ('b', 1)):
                    if (name, r, s) not in za: missing += 1; continue
                    z, o = za[(name, r, s)]
                    if (name, r, s) not in rz: missing += 1
                    elif z == rz[(name, r, s)]: same += 1
                    else: diff += 1; print('  za != rz:', name, r, s, z, rz[(name, r, s)])
                    if o != ov[si]: badover += 1
                    if z != o: zdiff.append((name, 'AB'[r], s, z, o))
        print('%s: za = rz at %d results, differ at %d, missing %d; za over column vs small solver: %d differences; Z != over at %d results'
              % (args[k], same, diff, missing, badover, len(zdiff)))
        for x in zdiff: print('   Z!=over  %-22s root %s %s to move: Z %s over %s' % x)
