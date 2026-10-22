"""Auditor B: KPK positions whose value (T=0) changes when stalemate is a loss instead of a draw; plus check-1 totals."""
import os, sys, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K4 = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run
tot = [0, 0]
for board in sys.argv[1:]:
    M = v_gen.build(board); n = len(M['nodes']); tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.graph')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    tpath = os.path.join(v_run.WORK, tag + '.z'); v_run.write_games(tpath, [('Z', vg.GAMES['0'])])
    A = v_run.run_c(gpath, tpath, 1)['Z']; B = v_run.run_c(gpath, tpath, 0)['Z']
    kpk = [i for i, p in enumerate(M['nodes']) if p[3] >= 0 and p[4] is None]
    other = n - len(kpk)
    ch_kpk = sum(A[i] != B[i] for i in kpk); ch_all = sum(A[i] != B[i] for i in range(n))
    m = json.load(open(os.path.join(K4, 'meta_%s.json' % tag)))
    ok = (m['check1']['kpk'], m['check1']['other'], m['check1']['stale_loss_kpk'], m['check1']['stale_loss_all'], m['nodes'], m['edges']) == \
         (len(kpk), other, ch_kpk, ch_all, n, sum(len(s) for s in M['succ']))
    print(board, 'KPK', len(kpk), 'other', other, 'stale-changes KPK', ch_kpk, 'all', ch_all, 'edges', sum(len(s) for s in M['succ']), 'meta agrees' if ok else 'META DIFFERS: %s' % m['check1'])
    tot[0] += len(kpk); tot[1] += other
print('totals KPK', tot[0], 'other', tot[1])
