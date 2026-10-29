#!/usr/bin/env python3
"""mech.py NAME BOARD : for every witness of data/wit_NAME.pos where Phi != Psi (data/wit_NAME.Pkp vs .Fkp), list the moves of the
deviating side to move with their P value (kp_p --pmodel --moves; White's view), so that the refuting sortie can be read off.
Output lines: 'Z | ctx | side s: Phi(s) vs Psi(s) | moves that do not lose for s: ...'"""
import sys, subprocess
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
name, board = sys.argv[1], sys.argv[2]
def rd(fn):
    return [l.rstrip('\n').rsplit(' | ', 1) for l in open(fn) if l.strip() and not l.startswith('#')]
pos = rd(D + 'wit_%s.Pkp' % name); fro = rd(D + 'wit_%s.Fkp' % name)
for i in range(0, len(pos), 2):
    for j, stm in ((i, 'w'), (i + 1, 'b')):
        ph, ps = pos[j][1].replace(' ', '')[0], fro[j][1].replace(' ', '')[0]
        if ph == ps: continue
        p = pos[j][0]
        out = subprocess.run([D + 'bin/kpp', '--board', board, '--pmodel', '--ep', 'on', '--promote', 'Q', '--moves'], input=p + '\n',
                             capture_output=True, text=True).stdout
        mv = out.strip().split(' | ')[-1].split()
        lose = 'L' if stm == 'w' else 'W'      # result (White's view) that is a loss for the mover
        good = [m for m in mv if not m.endswith(':' + lose)]
        t = p.split()
        print('%s | %s | %s to move: Phi=%s Psi=%s | non-losing moves for the mover: %s' % (' '.join(t[:-2]), '', stm, ph, ps, ' '.join(good) or 'none'))
