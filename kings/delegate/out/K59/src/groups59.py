"""K59: run def48.py (Definition 4.8 from --moves values of one solver) on the four cyl:8x7 groups of K48 placed on
flat 8x7, at every translate that fits on the board.  usage: groups59.py <ref3m|kpp> <set>  (set: flat87, flat97 = translates; flat88 = as placed and tall version, translates)"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
solver, which = sys.argv[1], sys.argv[2]
BASE = [('T1', 'Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6', 'f5'), ('T2', 'Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6', 'f5'),
        ('T3', 'Kd4 kf4 Pb3 Pb5 Pe2 pa5 pb6 pe6', 'f5'), ('T4', 'Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6', 'a5')]
def shift(pcs, k): return ' '.join(t[0] + chr(ord(t[1]) + k) + t[2:] for t in pcs.split())
def files(pcs): return [ord(t[1]) - 97 for t in pcs.split()]
def up(pcs):  # every piece one rank up (White's distances to promotion kept; White pawns lose their first-rank double step)
    return ' '.join(t[0] + t[1] + str(int(t[2:]) + 1) for t in pcs.split())
G = []
if which.startswith('F1_'):   # the flat 8x7 hit F1 of K59: translates on flat 8x7, 9x7, and on 8x8 as placed and one rank up
    F1 = ('F1', 'Ka4 kc4 Pb2 Pe4 Pe5 pb6 pe6', 'c5')
    Wb, Hb = int(which[3]), int(which[4])
    vars_ = (('as', F1[1], F1[2]),) if Hb == 7 else (('as', F1[1], F1[2]), ('up', up(F1[1]), 'c6'))
    for var, p0, zz in vars_:
        for k in range(Wb):
            p2 = shift(p0, k); z2 = chr(ord(zz[0]) + k) + zz[1:]
            if max(files(p2)) >= Wb or ord(z2[0]) - 97 >= Wb: break
            G.append(('flat', Wb, Hb, 'b', p2, z2, 'F1_%d%d_%s_t%d' % (Wb, Hb, var, k)))
if which == 'flat88':   # flat 8x8: each group as placed (Black one rank farther from promotion) and shifted one rank up
    for name, pcs, z1 in BASE:
        for var, p0, zz in (('as', pcs, z1), ('up', up(pcs), z1[0] + str(int(z1[1:]) + 1))):
            for k in range(8):
                p2 = shift(p0, k); z2 = chr(ord(zz[0]) + k) + zz[1:]
                if max(files(p2)) >= 8 or ord(z2[0]) - 97 >= 8: break
                G.append(('flat', 8, 8, 'b', p2, z2, 'f88_%s_%s_t%d' % (name, var, k)))
elif which.startswith('flat') and not which.startswith('F1_'):
    W, H = int(which[4]), int(which[5])
    for name, pcs, z1 in BASE:
        for k in range(W):
            p2 = shift(pcs, k); z2 = chr(ord(z1[0]) + k) + z1[1:]
            if max(files(p2)) >= W or ord(z2[0]) - 97 >= W: break
            G.append(('flat', W, H, 'b', p2, z2, 'f%d%d_%s_t%d' % (W, H, name, k)))
for kind, W, H, S, pcs, z1, tag in G:
    r = subprocess.run([sys.executable, os.path.join(HERE, 'def48.py'), solver, kind, str(W), str(H), S, pcs, z1, tag],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout + r.stderr); sys.stdout.flush()
