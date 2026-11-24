"""K59: def48.py on the flat 8x7 hits F2..F5 placed on flat 9x7 (every translate that fits) and on flat 8x8 (as placed,
every translate that fits, and one rank up).  usage: groupsF.py <ref3m|kpp>"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
solver = sys.argv[1]
BASE = [('F2', 'Ka4 kc4 Pb2 Pf5 pb6 pf6', 'c5'), ('F3', 'Ke4 kc4 Pb2 Pb5 Pf5 pb6 pf6', 'c5'),
        ('F4', 'Kc4 ke4 Pb5 Pf2 Pf5 pb6 pf6', 'e5'), ('F5', 'Ka4 kc4 Pb2 Pe5 Pf4 pb6 pe6 pf5', 'c5')]
def shift(p, k): return ' '.join(t[0] + chr(ord(t[1]) + k) + t[2:] for t in p.split())
def up(p): return ' '.join(t[0] + t[1] + str(int(t[2:]) + 1) for t in p.split())
def maxf(p): return max(ord(t[1]) - 97 for t in p.split())
G = []
for name, p, z in BASE:
    for (W, H, var, p0, z0) in ((9, 7, 'as', p, z), (8, 8, 'as', p, z), (8, 8, 'up', up(p), z[0] + str(int(z[1:]) + 1))):
        for k in range(W):
            p2 = shift(p0, k); z2 = chr(ord(z0[0]) + k) + z0[1:]
            if maxf(p2) >= W or ord(z2[0]) - 97 >= W: break
            G.append((W, H, p2, z2, '%s_%d%d_%s_t%d' % (name, W, H, var, k)))
for W, H, p, z, tag in G:
    r = subprocess.run([sys.executable, os.path.join(HERE, 'def48.py'), solver, 'flat', str(W), str(H), 'b', p, z, tag], capture_output=True, text=True)
    sys.stdout.write(r.stdout + r.stderr); sys.stdout.flush()
