"""K48 referee: run def48.py on every named group, one after another (each solver call through heavy.sh).
usage: groups.py <solver> <set: flat8 | flat9 | flat10 | cyl87>  -> one PASS/FAIL block per group on stdout"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
solver, which = sys.argv[1], sys.argv[2]
ZO = 'Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5'
def shift(pcs, k): return ' '.join(t[0] + chr(ord(t[1]) + k) + t[2:] for t in pcs.split())
G = []
if which == 'flat8':
    G += [('flat', 8, 6, 'b', ZO, 'd5', 'f8_ZO'), ('flat', 8, 6, 'b', shift(ZO, 1), 'e5', 'f8_t1'),
          ('flat', 8, 6, 'b', shift(ZO, 2), 'f5', 'f8_t2'), ('flat', 8, 6, 'b', 'Ka5 kc4 Pb2 Pe2 Pe4 pb5 pe5 pf4', 'c5', 'f8_t2refl'),
          ('flat', 8, 6, 'b', 'Kc5 ke4 Pd2 Pg2 Pg4 pd5 pg5 ph4', 'e5', 'f8_ZOrefl'),
          ('flat', 8, 6, 'w', 'Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5', 'd3', 'f8_U0'), ('flat', 8, 6, 'w', 'Ke2 kg2 Pb3 Pc2 Pf2 pc3 pc5 pf5', 'e3', 'f8_U1'),
          ('flat', 8, 6, 'w', 'Kc2 ka2 Pb2 Pe2 Pf3 pb5 pe3 pe5', 'c3', 'f8_U2')]
elif which in ('flat9', 'flat10'):
    W = int(which[4:])
    for k in range(W - 5):
        G.append(('flat', W, 6, 'b', shift(ZO, k), chr(ord('d') + k) + '5', 'f%d_t%d' % (W, k)))
elif which == 'cyl87':
    for pcs, z1, t in (('Kd4 kf4 Pa4 Pb5 Pe2 pa5 pb6 pe6', 'f5', 'c87_g1'), ('Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6', 'f5', 'c87_g2'),
                       ('Kd4 kf4 Pb3 Pb5 Pe2 pa5 pb6 pe6', 'f5', 'c87_g3'), ('Kc4 ka4 Pb2 Pe3 Pe5 pb6 pe4 pe6', 'a5', 'c87_g4'),
                       (ZO, 'd5', 'c87_ZO')):
        G.append(('cyl', 8, 7, 'b', pcs, z1, t))
for kind, W, H, S, pcs, z1, tag in G:
    r = subprocess.run([sys.executable, os.path.join(HERE, 'def48.py'), solver, kind, str(W), str(H), S, pcs, z1, tag],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout + r.stderr); sys.stdout.flush()
