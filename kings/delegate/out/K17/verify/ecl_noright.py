"""Referee: roots WITHOUT an e.p. right (both sides to move) on the given context files: compare D_whole (chess e.p.)
with D_fix (fixed root components, rights persist while another component is played), my own dgame/ecl code.
usage: ecl_noright.py <spec> <files> <maxp>"""
import sys, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from dgame import *
import ecl
spec, files, maxp = sys.argv[1], [int(x) for x in sys.argv[2].split(',')], int(sys.argv[3])
kind, dims = spec.split(':'); w, h = map(int, dims.split('x')); bd = Bd(w, h, kind == 'cyl')
alt, hss_exact, dfix = ecl.make(bd)
t0 = time.time(); n = nroots = nmulti = 0; diffs = []; hdiffs = 0
for p in ecl.contexts(bd, files, maxp):
    n += 1
    cs = ecl.comps_of(bd, p); key = tuple(sorted(cs, key=ecl.key))
    for s in 'WB':
        nroots += 1; nmulti += len(cs) >= 2
        dw = 'W' if alt(p, s) == 'W' else 'L'; df = 'W' if dfix(key, s) == 'W' else 'L'
        if dw != df:
            diffs.append((p, s, dw, df))
            if hss_exact(p, s): hdiffs += 1
print(spec, files, maxp, 'contexts', n, 'roots', nroots, 'multi', nmulti, 'D_fix!=D_whole', len(diffs), 'of which hss', hdiffs, 'time %.0f' % (time.time() - t0))
for d in diffs[:10]: print(d)
