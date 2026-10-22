"""K8v: stalemate-with-a-spare-move ablations.  chess rule (forced pass) vs
   mode 4 = optional: the stalemated mover may claim the draw or move in T,
   mode 5 = spare-blind: no chess move and not in check = draw at once, whatever T offers.
Compared with K8's ablation_<tag>.json ('spare_blind_stalemate').  usage: v8_ablation.py board ..."""
import collections, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run, v8_chess as vc, v8_mask as vm

BUILDER = vc.BUILDER
for board in sys.argv[1:]:
    M = v_gen.build(board); N = len(M['nodes']); tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.gab')
    with open(gpath, 'w') as f:
        f.write('%d\n' % N)
        for i in range(N):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes']) if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    tpath = os.path.join(v_run.WORK, tag + '.tab')
    items = [('T%d' % k, vg.GAMES[t]) for k, t in enumerate(vg.TESTS[:11])] + [('N%d' % (k + 20), vg.integer(k)) for k in vc.NS]
    v_run.write_games(tpath, items)
    finkeys = {t: 'T%d' % k for k, t in enumerate(vg.TESTS[:11])}
    R = {'chess': v_run.run_c(gpath, tpath, 1), 'optional': vm.run_mask(gpath, tpath, 4, [True] * N), 'blind': vm.run_mask(gpath, tpath, 5, [True] * N)}
    # kpsolve-free zugzwang set: strict zugzwang under the chess rule (T = 0), as before
    Z = R['chess']['N20']
    zug = {k for k, (cw, cb) in enumerate(quiet) if vc.RANK[Z[cw]] < vc.RANK[Z[cb]]}
    out = dict(board=board, quiet=len(quiet))
    sets = {}
    for nm in ('chess', 'optional', 'blind'):
        S = vc.analyse(R[nm], quiet, finkeys, vc.NS, -20, 20)
        sens = {k for k, x in enumerate(S) if x['sens']}
        pm1 = {k for k, x in enumerate(S) if x['plus1'] or x['minus1']}
        thr = collections.Counter(t for x in S for t in x['thr'])
        out[nm] = dict(tempo_sensitive=len(sens), sensitive_at_pm1=len(pm1), thresholds={str(k): v for k, v in sorted(thr.items())},
                       tails_n_minus20_to_minus2=vc.tailcount([x['prof'][m] for m in range(-20, -1)] for x in S),
                       tails_n_2_to_20=vc.tailcount([x['prof'][m] for m in range(2, 21)] for x in S),
                       mutual_zugzwangs_also_sensitive_at_pm1=len(zug & pm1))
        sets[nm] = sens
    for nm in ('optional', 'blind'):
        out[nm]['sensitive_under_both_chess_and_this'] = len(sets['chess'] & sets[nm])
        out[nm]['sensitive_under_chess_only'] = len(sets['chess'] - sets[nm])
        out[nm]['sensitive_under_this_only'] = len(sets[nm] - sets['chess'])
    k8 = json.load(open(os.path.join(BUILDER, 'ablation_%s.json' % tag)))['spare_blind_stalemate']
    def cmp(mine):
        keys = [('tempo_sensitive', 'tempo_sensitive'), ('sensitive_at_pm1', 'sensitive_at_pm1'), ('thresholds', 'thresholds'),
                ('tails_n_minus20_to_minus2', 'tails_n_minus20_to_minus2'), ('tails_n_2_to_20', 'tails_n_2_to_20'),
                ('mutual_zugzwangs_also_sensitive_at_pm1', 'mutual_zugzwangs_also_sensitive_at_pm1'),
                ('sensitive_under_both_chess_and_this', 'sensitive_under_both_chess_and_blind'),
                ('sensitive_under_chess_only', 'sensitive_under_chess_only'), ('sensitive_under_this_only', 'sensitive_under_blind_only')]
        return [a for a, b in keys if mine.get(a) != k8.get(b)]
    out['K8_spare_blind_mismatches_vs_optional(mode4)'] = cmp(out['optional'])
    out['K8_spare_blind_mismatches_vs_blind(mode5)'] = cmp(out['blind'])
    os.remove(gpath); os.remove(tpath)
    json.dump(out, open(os.path.join(HERE, 'out', 'ablation_%s.json' % tag), 'w'))
    print(json.dumps(out), flush=True)
