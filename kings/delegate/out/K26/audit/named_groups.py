#!/usr/bin/env python3
"""K26 audit: the named exact groups (Z_B, its mirror, Z_C, its mirror) at their 8 roots on many boards, with kpp (--pmodel) and ref3m.
Own parser. Prints, per group and board: root values (White view) and the number of non-shuttle moves that do not lose at once ("leaks"), per solver.
usage: named_groups.py > named_groups.txt"""
import subprocess, os, sys
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin')
G = {
 'ZB':  (['b2', 'c3'], ['a4', 'b5'], 'Pa3 Pb4 pb3 pc4'),
 'ZBm': (['a3', 'b2'], ['b5', 'c4'], 'Pb4 Pc3 pa4 pb3'),
 'ZC':  (['c2', 'c3'], ['a4', 'a5'], 'Pa2 Pc4 pa3 pc5'),
 'ZCm': (['a2', 'a3'], ['c4', 'c5'], 'Pa4 Pc2 pa5 pc3'),
}
BOARDS = ['flat:7x6', 'flat:8x6', 'flat:9x6', 'flat:5x6', 'flat:7x7', 'flat:7x5', 'flat:8x8',
          'cyl:5x6', 'cyl:6x6', 'cyl:7x6', 'cyl:8x6', 'cyl:9x6', 'cyl:10x6', 'cyl:11x6', 'cyl:12x6', 'flat:10x6', 'flat:12x6',
          'cyl:8x5', 'cyl:6x7', 'cyl:7x7', 'cyl:8x7', 'cyl:9x7', 'cyl:8x8']
def run(board, lines, solver):
    if solver == 'kpp':
        cmd = [B + '/kpp', '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--pmodel', '--moves']
    else:
        b = board.replace(':', '') if board.startswith('flat') else board
        cmd = [B + '/ref3m', '--board', b, '--moves']
    o = subprocess.run(['nice', '-n', '15'] + cmd, input='\n'.join(lines) + '\n', capture_output=True, text=True).stdout.split('\n')
    return [l for l in o if ' | ' in l]
def parse(l, solver):
    p = l.split(' | ')
    stm = p[0].split()[-2]
    if solver == 'kpp':
        val = p[1].split()[0]; mv = p[2].split() if len(p) > 2 else []
    else:
        t = p[1].split(); val = t[0]; mv = t[1:]
    return stm, val, [m.rsplit(':', 1) for m in mv]
for g, (W, Bk, pawns) in G.items():
    for board in BOARDS:
        dims = board.split(':')[1]; bw, bh = map(int, dims.split('x'))
        if bh < 6 and False: pass
        lines = ['K%s k%s %s %s -' % (w, b, pawns, s) for w in W for b in Bk for s in 'wb']
        out = {}
        for solver in ('kpp', 'ref3m'):
            try:
                res = run(board, lines, solver)
            except Exception as e:
                out[solver] = ('ERR', str(e)); continue
            if len(res) != 8:
                out[solver] = ('ERR', 'got %d lines' % len(res)); continue
            vals = []; leaks = 0; nsh = []
            for l in res:
                stm, val, mv = parse(l, solver)
                vals.append(val)
                sh = set(W) if stm == 'w' else set(Bk)
                lose = 'L' if stm == 'w' else 'W'
                k = 0
                for nm, v in mv:
                    if nm[0] == 'K' and {nm[1:3], nm[3:5]} == sh: k += 1; continue
                    if v != lose: leaks += 1
                nsh.append(k)
            out[solver] = (''.join(vals), leaks, ''.join(map(str, nsh)))
        print('%-4s %-9s kpp %-28s ref3m %-28s %s' % (g, board, out.get('kpp'), out.get('ref3m'), 'AGREE' if out.get('kpp') == out.get('ref3m') else 'DIFF'), flush=True)
