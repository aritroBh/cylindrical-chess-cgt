"""K8v: a third, pure-Python solver for x (+) n (n an integer, spare moves for White if n > 0, for Black if n < 0),
written directly from the rule text (states (node, t); no counters, no shared code with v_prod.c / K8), used to test
v_prod.c on a few small boards, all four stalemate rules, n = -3..3, every node of the graph.
usage: v8_naive.py board ..."""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

def solve(M, n, sd):
    N = len(M['nodes']); stm = M['stm']; chk = M['incheck']; flip = M['flip']; succ = M['succ']
    win = {}   # (c, t) -> True (mover wins) / False (mover loses); absent = draw
    def moves(c, t):
        out = [(s, t) for s in succ[c]]
        if flip[c] >= 0:
            if stm[c] == 0 and t > 0:
                out.append((flip[c], t - 1))
            if stm[c] == 1 and t < 0:
                out.append((flip[c], t + 1))
        return out
    states = [(c, n) for c in range(N)]
    # all reachable states (t moves towards 0)
    seen = set(states); todo = list(states)
    while todo:
        c, t = todo.pop()
        for s in moves(c, t):
            if s not in seen:
                seen.add(s); todo.append(s)
    allm = {s: moves(*s) for s in seen}
    changed = True
    while changed:
        changed = False
        for s, mv in allm.items():
            if s in win:
                continue
            c = s[0]
            if any(win.get(m) is False for m in mv):
                win[s] = True; changed = True
            elif not mv:
                draw = (sd == 1) or (sd == 2 and stm[c] == 0) or (sd == 3 and stm[c] == 1)
                if not (draw and not chk[c]):
                    win[s] = False; changed = True
            elif all(win.get(m) is True for m in mv):
                win[s] = False; changed = True
    res = []
    for c in range(N):
        w = win.get((c, n))
        res.append('D' if w is None else ('W' if (w == (stm[c] == 0)) else 'L'))
    return ''.join(res)

bad = 0; tot = 0
for board in sys.argv[1:]:
    M = v_gen.build(board); N = len(M['nodes']); tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.gn')
    with open(gpath, 'w') as f:
        f.write('%d\n' % N)
        for i in range(N):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    tpath = os.path.join(v_run.WORK, tag + '.tn')
    ns = list(range(-3, 4))
    v_run.write_games(tpath, [('N%d' % (k + 20), vg.integer(k)) for k in ns])
    for sd in (0, 1, 2, 3):
        R = v_run.run_c(gpath, tpath, sd)
        for k in ns:
            mine = solve(M, k, sd)
            c = R['N%d' % (k + 20)]
            d = sum(a != b for a, b in zip(mine, c)); bad += d; tot += N
    os.remove(gpath); os.remove(tpath)
    print(board, 'nodes', N, 'rules 4 x n -3..3: states compared so far', tot, 'differences so far', bad, flush=True)
print('TOTAL states compared', tot, 'differences', bad)
