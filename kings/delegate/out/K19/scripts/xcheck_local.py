"""K19: validation of the local-game solver (localgame.py) against kp_p. With no confinement, no passes for the
defender, no queen clause and the mate rule, the local game of attacker A from a position with the defender to
move is exactly the P-model: A wins the local game iff A wins P. Compare on random positions, both colours of
attacker; also bounded recursion (T = 24) against the unbounded least fixed point."""
import random, subprocess, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from k19engine import *
from localgame import Local
from xcheck_p import rand_pos
HERE = os.path.dirname(os.path.abspath(__file__))
KPP = os.path.join(HERE, '..', 'kp_p')
rng = random.Random(4242)
tot = bad = bad2 = 0
nA = 0
for spec, n in [('cyl:6x5', 40), ('flat:5x5', 30), ('flat:5x4', 40)]:
    B = parse_board(spec)
    positions = [rand_pos(B, rng) for _ in range(n)]
    inp = '\n'.join(fmt_pos(B, p) for p in positions) + '\n'
    out = subprocess.run([KPP, '--board', spec, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel'],
                         input=inp, capture_output=True, text=True).stdout.splitlines()
    lines = [l for l in out if not l.startswith('[')]
    for pos, line in zip(positions, lines):
        a, b = line.split('|')[1].split()
        assert a == b
        stm = pos[5]
        D = stm
        A = 1 - stm
        # A wins P iff White-pov result is W (A white) or L (A black)
        a_wins_p = (a == 'W') if A == 0 else (a == 'L')
        L = Local(B, A, conf=None, queen=False, mate_win=True)
        lf = L.lfp(pos, False)[0]
        tot += 1
        nA += a_wins_p
        if lf != a_wins_p:
            bad += 1
            print('LFP MISMATCH', spec, fmt_pos(B, pos), 'A=', A, 'kp_p', a, 'local', lf)
        bt = L.minT(pos, 0, tmax=24) is not None
        if bt != lf:
            bad2 += 1
            print('BOUNDED MISMATCH', spec, fmt_pos(B, pos), bt, lf)
print('positions', tot, 'A wins P in', nA, '; local lfp vs kp_p mismatches', bad, '; bounded(T=24) vs lfp mismatches', bad2)
