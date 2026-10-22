"""Auditor B: the set of legal KPK positions (either side to move) = the set kpsolve does not call X."""
import os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v_gen
for board in sys.argv[2:]:
    G = v_gen.Geo(board); N = G.W * G.H
    mine, lines = set(), []
    for wk in range(N):
        for bk in range(N):
            for wp in range(N):
                if len({wk, bk, wp}) < 3: continue
                for stm in (0, 1):
                    p = (stm, wk, bk, wp, None)
                    lines.append(p)
    inp = os.path.join(HERE, 'work', board.replace(':', '_') + '.all')
    with open(inp, 'w') as f:
        for p in lines:
            f.write(v_gen.kpline(G, p) + '\n')
    out = subprocess.run(['nice', '-n', '10', sys.argv[1], '--board', board, '--ep', 'on', '--promote', 'QRBN', '--cap', '1', '--threads', '2'],
                         stdin=open(inp), capture_output=True, text=True, check=True).stdout.splitlines()
    assert len(out) == len(lines)
    kp_legal = {p for p, l in zip(lines, out) if 'X' not in l.rsplit(' | ', 1)[1].split()}
    M = v_gen.build(board)
    my_legal = {p for p in M['nodes'] if p[3] >= 0 and p[4] is None}
    print(board, 'all candidate lines', len(lines), 'kpsolve non-X', len(kp_legal), 'mine legal KPK', len(my_legal),
          'symmetric difference', len(kp_legal ^ my_legal))
