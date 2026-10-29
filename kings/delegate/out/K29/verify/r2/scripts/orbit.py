#!/usr/bin/env python3
"""orbit.py CONFIG(name from K29 configs.txt) OUTFILE_PREFIX : from the K29 table (SURVIVES rows) write
 g_<cfg>_reps.txt   (representatives)  and  g_<cfg>_all.txt (all members of the classes by MY symmetry code: colour swap+rank flip, reflection of F_Z)"""
import sys, csv
R = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
V = R + 'verify/r2/data/'
cfg = {}
for l in open(R + 'scripts/configs.txt'):
    if l.startswith('#') or not l.strip(): continue
    n, b, zs, fz, dmin, suf = l.split(); cfg[n] = (b, int(zs), int(fz))
name = sys.argv[1]; b, zs, fz = cfg[name]; W, H = [int(x) for x in b.split(':')[1].split('x')]; cyl = b.startswith('cyl')
def parse(s): return [(t[0], ord(t[1]) - 97, int(t[2:])) for t in s.split()]
def key(toks): return tuple(sorted(toks))
def fmt(toks): return ' '.join('%s%s%d' % (c, chr(97 + f), r) for c, f, r in sorted(toks, key=lambda t: (t[0].lower() != 'k', t[0].islower(), t[1], t[2])))
def swap(t): return [(c.swapcase(), f, H + 1 - r) for c, f, r in t]
def refl(t):
    if not (cyl or (W == 7 and zs == 2)): return None   # reflection is a symmetry only where it maps board AND context class to themselves
    o = []
    for c, f, r in t:
        g = 2 * zs + fz - 1 - f
        g = g % W if cyl else g
        if not 0 <= g < W: return None
        o.append((c, g, r))
    return o
reps = []; allm = []
for r in csv.reader(open(R + 'data/table_all.tsv'), delimiter='\t'):
    if r[0] == name and r[5] == 'SURVIVES': reps.append(r[1])
for z in reps:
    seen = {}
    t0 = parse(z)
    for t in (t0, swap(t0), refl(t0), swap(t0) and refl(swap(t0))):
        if t is None: continue
        seen[key(t)] = t
    allm += [fmt(t) for t in seen.values()]
    if len(seen) != int([r[2] for r in csv.reader(open(R + 'data/table_all.tsv'), delimiter='\t') if r[0] == name and r[1] == z][0]):
        print('class size mismatch', z, len(seen))
open(V + 'g_%s_reps.txt' % name, 'w').write('\n'.join(reps) + '\n'); open(V + 'g_%s_all.txt' % name, 'w').write('\n'.join(allm) + '\n')
print(name, len(reps), 'classes', len(allm), 'members')
