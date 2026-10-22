"""Auditor B: integer scan x (+) n, n = -10..10, recomputed with my own graph/games/solver, compared with
tempo_scan.jsonl; plus which classes the placements with a tempo threshold belong to."""
import json, os, sys, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K4 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

RANGE = list(range(-10, 11))
theirs = {}
for line in open(os.path.join(K4, 'tempo_scan.jsonl')):
    d = json.loads(line); theirs[d['board']] = d
bad = 0
for board in sys.argv[1:]:
    M = v_gen.build(board); G = M['G']; n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.graph')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]), ' '.join(map(str, M['succ'][i]))))
    tpath = os.path.join(v_run.WORK, tag + '.int')
    v_run.write_games(tpath, [('N%d' % (k + 20), vg.integer(k)) for k in RANGE])
    R = v_run.run_c(gpath, tpath, 0)
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes']) if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    rows = {r['placement']: r for r in map(json.loads, open(os.path.join(K4, tag + '.jsonl')))}
    nj = collections.Counter(); jat = collections.Counter(); far = 0
    jclass = collections.Counter(); jplace = collections.defaultdict(list)
    for cw, cb in quiet:
        pr = [R['N%d' % (k + 20)][cw] + R['N%d' % (k + 20)][cb] for k in RANGE]
        jumps = [k for k, a, b in zip(RANGE, pr, pr[1:]) if a != b]
        nj[len(jumps)] += 1
        for j in jumps: jat[j] += 1
        far += any(j >= 2 or j <= -3 for j in jumps)
        if jumps:
            p = M['nodes'][cw]
            pl = 'K%s P%s k%s' % (v_gen.name(G, p[1]), v_gen.name(G, p[3]), v_gen.name(G, p[2]))
            c = rows[pl]['cls']
            sg = rows[pl]['sig']; pairs = {sg[i:i+2] for i in range(0, 32, 2)}
            jclass[c if c != 'unmatched' else ('unmatched T-indep' if len(pairs) == 1 else 'unmatched T-dep')] += 1
            jplace[tuple(jumps)].append((pl, ' '.join(pr[8:13])))
    t = theirs[board]
    mine = dict(placements=len(quiet), number_of_jumps={str(k): v for k, v in sorted(nj.items())},
                jump_between_n_and_n_plus_1={str(k): v for k, v in sorted(jat.items())}, far=far)
    ok = (t['placements'] == mine['placements'] and t['number_of_jumps'] == mine['number_of_jumps']
          and t['jump_between_n_and_n_plus_1'] == mine['jump_between_n_and_n_plus_1'] and t['placements_with_a_jump_beyond_pm2'] == far)
    bad += not ok
    print(board, 'MATCHES builder scan' if ok else 'DIFFERS from builder scan', mine, 'classes of threshold placements:', dict(jclass))
    if '-v' in os.environ.get('V', ''):
        for k, v in jplace.items(): print('   jumps', k, len(v), v[:2])
print('scan mismatches:', bad)
