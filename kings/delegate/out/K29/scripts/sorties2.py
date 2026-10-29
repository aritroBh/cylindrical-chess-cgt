#!/usr/bin/env python3
"""sorties2.py BOARD ZS FZ GROUPFILE OUT : for every bare group Z of GROUPFILE (first field of each line, '|'-separated) and each side to move,
every legal move m with the exact P-win depth d(m) of the punisher after it (plies, a promotion counts 1; grp2 --depth, one batched call per group),
the number of punisher moves T_P(m) = (d+1)/2, and the escape time e(m): the minimum, over the squares c on the context files nearest to F_Z (distance 2)
and ranks 2..5 (any such square could hold a context pawn), of the number of king moves (king metric, board topology, pawns of the group ignored as
obstacles only if they block the square itself) the moved king needs after m to stand on a square adjacent to c, plus 1 for the capture.  (A lower bound on
the time at which the sortie king can first touch a context pawn.)  Output lines:  Z | side | move | d | T_P(m) | e(m)
The summary line per group:  Z | T_P(w) T_P(b) |  per side the max T_P(m) | and the min over sorties of  T_P(m) - e(m)  (slack).
Needs bin/kpp (moves), bin/grp2 (depth)."""
import sys, subprocess, importlib.util, re
D = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29/'
board, zs, fz, gf, outf = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.argv = ['mech2', board, str(zs), str(fz), '/dev/null']
spec = importlib.util.spec_from_file_location('mech2', D + 'scripts/mech2.py'); m2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2)
W, H, cyl = m2.W, m2.H, m2.cyl
def kdist(a, b):
    (f0, r0), (f1, r1) = a, b
    df = abs(f0 - f1)
    if cyl: df = min(df, W - df)
    return max(df, abs(r0 - r1))
def sqs(tok): return (ord(tok[0]) - 97, int(tok[1:]) - 1)
ctxsq = [(f, r) for f in range(W) if m2.fdist(f) == 2 for r in range(1, 5)]
out = open(outf, 'w')
for line in open(gf):
    z = line.split(' | ')[0].strip()
    if not z or z.startswith('#'): continue
    summ = {}
    for stm in 'wb':
        pos = '%s %s -' % (z, stm)
        mv, _ = m2.moves_of(pos)
        if mv is None: continue
        cand = []
        for x in mv:
            mm = x.split(':')[0]
            p2 = m2.apply(pos, mm)
            cand.append((mm, p2))
        batch = [p2 for _, p2 in cand if p2]
        res = {}
        if batch:
            o = subprocess.run([D + 'bin/grp2', '--board', board, '--mode', 'pos', '--depth'], input='\n'.join(batch) + '\n', capture_output=True, text=True).stdout
            for l in o.splitlines():
                if ' depth ' in l: res[l.split(' | ')[0]] = int(l.rsplit('depth', 1)[1])
        best = []
        for mm, p2 in cand:
            if p2 is None: d = 0; tp = 0; kpos = None
            else:
                d = res.get(p2, -1); tp = (d + 1) // 2
            # moved king after m
            pc = mm[0]
            if pc == 'K':
                kk = sqs(mm[3:5])
            else:
                toks = (p2 or '').split(); kk = sqs([t for t in toks if t[0] == ('K' if stm == 'w' else 'k')][0][1:]) if p2 else None
            e = min(kdist(kk, c) for c in ctxsq) if kk else 99
            # king adjacent to c in e-1 moves ... e = king moves to reach a square adjacent to c (distance-1) then one capture
            e = max(e - 1, 0) + 1
            out.write('%s | %s | %s | %d | %d | %d\n' % (z, stm, mm, d, tp, e))
            best.append((tp, e, pc))
        if best: summ[stm] = (max(b[0] for b in best), min(b[0] - b[1] for b in best if b[2] == 'K') if any(b[2] == 'K' for b in best) else None)
    out.write('SUMMARY %s | Tw %s Tb %s | slack_w %s slack_b %s\n' % (z, summ.get('w', ('-',))[0], summ.get('b', ('-',))[0], summ.get('w', (0, '-'))[1], summ.get('b', (0, '-'))[1]))
    out.flush()
