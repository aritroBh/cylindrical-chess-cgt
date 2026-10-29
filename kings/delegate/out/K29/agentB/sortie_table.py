#!/usr/bin/env python3
"""agentB/sortie_table.py BOARD ZS FZ REPFILE OUT
For every bare group Z of REPFILE (one 'Z tokens' per line) and each side to move: every legal move m, its class
  B = king step onto a buffer file (file distance exactly 1 from F_Z), Z = king step inside F_Z, P = Z-pawn move,
and the exact P-win depth of the punisher after m (plies from the position after m, promotion = 1 ply; grp2 --depth, COMPUTED-1)
and L(m) = (depth + 1) / 2 = the number of punisher moves in the exact win, the reply r included.
Output: one line per (group, side): 'Z | stm | m:class:L m:class:L ...'.  mech2.py (K29 session 2, unchanged) supplies the move generator
(kp_p --pmodel --moves) and the move applier."""
import sys, subprocess, importlib.util
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
board, zs, fz, rep, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
sys.argv = ['mech2', board, zs, fz, '/dev/null']
spec = importlib.util.spec_from_file_location('mech2', D + 'scripts/mech2.py'); m2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)
fo = open(out, 'w')
for z in [l.strip() for l in open(rep) if l.strip() and not l.startswith('#')]:
    kids = []   # (stm, move, class, child position)
    for stm in 'wb':
        pos = '%s %s -' % (z, stm)
        mv, _ = m2.moves_of(pos)
        for x in (mv or []):
            mm = x.split(':')[0]
            p2 = m2.apply(pos, mm)
            mo = m2.MV.match(x)
            if p2 is None: kids.append((stm, mm, 'PROMO', None)); continue
            if mo.group(1) == 'K':
                c = 'B' if m2.fdist(m2.fl(mo.group(4))) == 1 else ('Z' if m2.inz(m2.fl(mo.group(4))) else 'X')
            else: c = 'P'
            kids.append((stm, mm, c, p2))
    pos_in = [k[3] for k in kids if k[3]]
    res = subprocess.run([D + 'bin/grp2', '--board', board, '--mode', 'pos', '--depth'], input='\n'.join(pos_in) + '\n', capture_output=True, text=True).stdout.splitlines() if pos_in else []
    dep = {}
    for l in res:
        if ' | ' in l: p, r = l.rsplit(' | ', 1); dep[p] = (r.split()[0], int(r.split()[-1]) if r.split()[-1].isdigit() else -1)
    for stm in 'wb':
        items = []
        for (s, mm, c, p2) in kids:
            if s != stm: continue
            if p2 is None: items.append('%s:PROMO:0' % mm); continue
            d = dep.get(p2, ('?', -1))[1]
            items.append('%s:%s:%s' % (mm, c, (d + 1) // 2 if d > 0 else '?'))
        fo.write('%s | %s | %s\n' % (z, stm, ' '.join(items))); fo.flush()
