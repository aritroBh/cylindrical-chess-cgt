"""Auditor B check 1: my own graph/solver (stalemate = draw, T = 0) against kpsolve compiled by me
from kings/kpsolve.c with the builder's command line, plus the builder's own check1() rerun."""
import os, subprocess, sys, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K4 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

def mine(board, kpbin):
    M = v_gen.build(board); G = M['G']; n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.graph')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    tpath = os.path.join(v_run.WORK, tag + '.z')
    v_run.write_games(tpath, [('Z', vg.GAMES['0'])])
    Z = v_run.run_c(gpath, tpath, 1)['Z']
    inp = os.path.join(v_run.WORK, tag + '.kpin'); outp = os.path.join(v_run.WORK, tag + '.kpout')
    with open(inp, 'w') as f:
        for p in M['nodes']:
            f.write(v_gen.kpline(G, p) + '\n')
    cmd = ['nice', '-n', '10', kpbin, '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--threads', '2']
    with open(inp) as fi, open(outp, 'w') as fo:
        subprocess.run(cmd, stdin=fi, stdout=fo, stderr=subprocess.DEVNULL, check=True)
    lines = open(outp).read().splitlines()
    assert len(lines) == n
    diffs = 0; kpk = other = 0; nonexact = 0
    for i, line in enumerate(lines):
        a, b = line.rsplit(' | ', 1)[1].split()
        if a != b: nonexact += 1
        if a != Z[i] or b != Z[i]: diffs += 1
        if M['nodes'][i][3] >= 0 and M['nodes'][i][4] is None: kpk += 1
        else: other += 1
    print('MY check1', board, 'compared', n, '(KPK %d, other %d)' % (kpk, other), 'differences', diffs, 'non-exact kp lines', nonexact, flush=True)
    return diffs

if __name__ == '__main__':
    kp = sys.argv[1]
    total = 0
    for b in sys.argv[2:]:
        total += mine(b, kp)
    print('total differences', total)
