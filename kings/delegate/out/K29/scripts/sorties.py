#!/usr/bin/env python3
"""sorties.py BOARD 'Z tokens' : for the bare group Z and each side to move, every legal move with the exact P-win depth of the
punisher after it (plies, promotion = 1; grp2 --depth) and T_P(m) = (depth+1)/2 = number of punisher moves.  T_P(s) = max_m T_P(m).
Output: side | move | punisher depth | T_P(m)."""
import sys, subprocess, importlib.util
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
board, z = sys.argv[1], sys.argv[2]
sys.argv = ['mech2', board, '0', '3', '/dev/null']   # reuse apply()/MV from mech2 (no R lines are read)
spec = importlib.util.spec_from_file_location('mech2', D + 'scripts/mech2.py'); m2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)
for stm in 'wb':
    pos = '%s %s -' % (z, stm)
    mv, _ = m2.moves_of(pos)
    res = []
    for x in mv:
        mm = x.split(':')[0]
        p2 = m2.apply(pos, mm)
        if p2 is None: res.append((mm, 'promotion', 0)); continue
        out = subprocess.run([D + 'bin/grp2', '--board', board, '--mode', 'pos', '--depth'], input=p2 + '\n', capture_output=True, text=True).stdout
        d = int(out.strip().split('depth')[-1]); res.append((mm, d, (d + 1) // 2))
    print('%s to move: %d moves; T_P(side) = %s' % (stm, len(res), max([r[2] for r in res]) if res else 'none (no legal move)'))
    for r in res: print('   %s  depth %s  T=%s' % r)
