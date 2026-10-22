"""K8v: strict zugzwang K+P vs K placements (T = 0: White to move strictly worse than Black to move) under the four
stalemate rules, and the overlap between rules.  usage: v8_zug_asym.py board ...  (prints one JSON line per board)"""
import json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run
RANK = {'L': 0, 'D': 1, 'W': 2}
names = {0: 'WlBl', 1: 'WdBd', 2: 'WdBl', 3: 'WlBd'}
for board in sys.argv[1:]:
    M = v_gen.build(board); G = M['G']; N = len(M['nodes']); tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.gz8')
    with open(gpath, 'w') as f:
        f.write('%d\n' % N)
        for i in range(N):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    tpath = os.path.join(v_run.WORK, tag + '.tz8')
    v_run.write_games(tpath, [('Z', vg.GAMES['0'])])
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes']) if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    Z = {sd: v_run.run_c(gpath, tpath, sd)['Z'] for sd in range(4)}
    zs = {sd: {k for k, (cw, cb) in enumerate(quiet) if RANK[Z[sd][cw]] < RANK[Z[sd][cb]]} for sd in range(4)}
    pairs = {names[sd]: {} for sd in range(4)}
    for sd in range(4):
        for k in zs[sd]:
            cw, cb = quiet[k]; p = Z[sd][cw] + Z[sd][cb]; pairs[names[sd]][p] = pairs[names[sd]].get(p, 0) + 1
    out = dict(board=board, quiet=len(quiet), zugzwang_placements={names[sd]: len(zs[sd]) for sd in range(4)}, pair_types=pairs,
               WlBl_and_WdBl=len(zs[0] & zs[2]), WlBd_and_WdBd=len(zs[3] & zs[1]), WlBl_and_WdBd=len(zs[0] & zs[1]))
    os.remove(gpath); os.remove(tpath)
    print(json.dumps(out), flush=True)
