#!/usr/bin/env python3
"""gen_all.py BOARD ZS FZ [ZW ZB [PART NPARTS]]   (BOARD like cyl:7x6 or flat:7x6)
Writes, for the completeness cross-check of the candidate list, every bare group of the enumeration as a position for an
independent solver (kp_p --pmodel, ref3): kings anywhere on the files of F_Z (files ZS .. ZS+FZ-1, ranks 1..H), Z-pawns on
the files of F_Z, ranks 2..H-1 (here 2..5), at most ZW white and ZB black Z-pawns (default 2 2), at least one pawn, distinct
squares.  Both sides to move, e.p. '-'.  Kings on one square or adjacent are skipped (illegal in every solver).
PART/NPARTS splits the pawn configurations (config index mod NPARTS == PART) so that the run can be chunked.
  gen_all.py filter < solver-output : prints the groups with (White to move = L, Black to move = W) in White's view."""
import sys, itertools
if sys.argv[1] == 'filter':
    prev = None
    for l in sys.stdin:
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        pos, r = l.rsplit(' | ', 1); r = r.replace(' ', '')[:1]
        t = pos.split(); stm = t[-2]; key = ' '.join(t[:-2])
        if stm == 'w': prev = (key, r)
        elif prev and prev[0] == key and prev[1] == 'L' and r == 'W': print(key)
    sys.exit(0)
board, zs, fz = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
zw = int(sys.argv[4]) if len(sys.argv) > 4 else 2
zb = int(sys.argv[5]) if len(sys.argv) > 5 else 2
part = int(sys.argv[6]) if len(sys.argv) > 6 else 0
nparts = int(sys.argv[7]) if len(sys.argv) > 7 else 1
kind, dims = board.split(':'); W, H = map(int, dims.split('x')); cyl = kind == 'cyl'
files = [(zs + i) % W for i in range(fz)]
def name(f, r): return chr(97 + f) + str(r)
def adj(a, b):
    if a == b: return True
    df = abs(a[0] - b[0]); 
    if cyl: df = min(df, W - df)
    return df <= 1 and abs(a[1] - b[1]) <= 1
ksq = [(f, r) for f in files for r in range(1, H + 1)]
psq = [(f, r) for f in files for r in range(2, H)]
cfgs = 0; n = 0
for a in range(zw + 1):
    for ws in itertools.combinations(psq, a):
        rest = [s for s in psq if s not in ws]
        for b in range(zb + 1):
            if a + b == 0: continue
            for bs in itertools.combinations(rest, b):
                cfgs += 1
                if cfgs % nparts != part: continue
                pt = ['P' + name(*s) for s in ws] + ['p' + name(*s) for s in bs]
                occ = set(ws) | set(bs)
                for wk in ksq:
                    if wk in occ: continue
                    for bk in ksq:
                        if bk in occ or adj(wk, bk): continue
                        z = 'K%s %s k%s' % (name(*wk), ' '.join(pt[:a]), name(*bk))
                        z = z.replace('  ', ' ') + (' ' + ' '.join(pt[a:]) if b else '')
                        print(z + ' w -'); print(z + ' b -'); n += 2
sys.stderr.write('%d configs (this part %d/%d), %d positions\n' % (cfgs, part, nparts, n))
