"""K8v: where is a single spare move spent?  My own re-derivation of K8's mask tests with v_mask.c.
For each board:
  - strict-zugzwang nodes of the whole graph at T = 0 (mover not in check, strictly worse off than with the other side
    to move) for normal play and for the chess rule; stalemate ("forced pass") nodes (mover not in check, no chess move);
  - x (+) 1 and x (+) -1 solved in full, and again with moves in T allowed only at a chosen node set;
  - number of nodes ("states") and of quiet placements whose result differs from the full solution.
usage: v8_mask.py board ...   (writes out/mask_<tag>.json)"""
import collections, json, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
sys.path.insert(0, HERE)
import v_gen, v_games as vg, v_run

RANK = {'L': 0, 'D': 1, 'W': 2}
OUT = os.path.join(HERE, 'out')


def run_mask(gpath, tpath, mode, mask):
    mpath = os.path.join(v_run.WORK, 'mask.txt')
    with open(mpath, 'w') as f:
        f.write(''.join('1' if m else '0' for m in mask) + '\n')
    out = subprocess.run(['nice', '-n', '10', os.path.join(HERE, 'v_mask'), gpath, tpath, str(mode), mpath],
                         capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        nm, s, sw = line.split(' ')
        res[nm] = s
    os.remove(mpath)
    return res


def main(board):
    t0 = time.time()
    M = v_gen.build(board)
    n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(v_run.WORK, tag + '.gm')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]),
                                           ' '.join(map(str, M['succ'][i]))))
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes'])
             if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    tpath = os.path.join(v_run.WORK, tag + '.tm')
    v_run.write_games(tpath, [('P', vg.integer(1)), ('M', vg.integer(-1)), ('Z', vg.integer(0))])
    allm = [True] * n
    nom = [False] * n
    stm, chk, flip = M['stm'], M['incheck'], M['flip']
    deg = [len(s) for s in M['succ']]
    kpk = [p[3] >= 0 and p[4] is None for p in M['nodes']]
    stal = [(not chk[i]) and deg[i] == 0 for i in range(n)]
    out = dict(board=board, nodes=n, quiet=len(quiet))

    def zug_nodes(Z):
        zs = [False] * n
        for c in range(n):
            if flip[c] < 0:
                continue
            a, b = RANK[Z[c]], RANK[Z[flip[c]]]
            zs[c] = (a < b) if stm[c] == 0 else (a > b)
        return zs

    def diffs(A, B):
        sd = [i for i in range(n) if A[i] != B[i]]
        qd = sum(1 for (cw, cb) in quiet if A[cw] != B[cw] or A[cb] != B[cb])
        return len(sd), qd

    res = {}
    for label, mode in (('chess', 1), ('normal', 0)):
        full = v_run.run_c(gpath, tpath, mode)          # my plain solver, T in {+1, -1, 0}
        Z = full['Z']
        zs = zug_nodes(Z)
        zw = sum(1 for c in range(n) if zs[c] and stm[c] == 0)
        zb = sum(1 for c in range(n) if zs[c] and stm[c] == 1)
        sw = sum(1 for c in range(n) if stal[c] and stm[c] == 0)
        sb = sum(1 for c in range(n) if stal[c] and stm[c] == 1)
        # placements (W-to-move node of a K+P vs K placement) that are strict zugzwang with both sides to move
        zq = [(cw, cb) for (cw, cb) in quiet if zs[cw] and zs[cb]]
        r = dict(zugzwang_white=zw, zugzwang_black=zb, zugzwang_white_that_are_kpk=sum(1 for c in range(n) if zs[c] and kpk[c] and stm[c] == 0),
                 zugzwang_black_that_are_kpk=sum(1 for c in range(n) if zs[c] and kpk[c] and stm[c] == 1),
                 zugzwang_all_kpk=all(kpk[c] for c in range(n) if zs[c]), zugzwang_with_pawn=sum(1 for c in range(n) if zs[c] and M['nodes'][c][3] >= 0),
                 stalemate_white=sw, stalemate_black=sb,
                 zugzwang_quiet_placements_with_both_sides=len(zq),
                 zugzwang_nodes_not_in_a_both_sides_pair=sum(1 for c in range(n) if zs[c] and not (zs[c] and zs[flip[c]])))
        if mode == 0:
            # normal play: mask = strict-zugzwang nodes; no mask
            m_zug = zs
            ra = run_mask(gpath, tpath, 0, zs)
            rb = run_mask(gpath, tpath, 0, nom)
            for nm, lab in (('P', '+1'), ('M', '-1')):
                r['mask=zugzwang n=' + lab] = dict(pass_nodes=sum(zs), states_differ_from_full=diffs(ra[nm], full[nm])[0],
                                                   quiet_differ_from_full=diffs(ra[nm], full[nm])[1])
                r['mask=none n=' + lab] = dict(pass_nodes=0, states_differ_from_full=diffs(rb[nm], full[nm])[0],
                                               quiet_differ_from_full=diffs(rb[nm], full[nm])[1])
        else:
            # chess rule: zugzwang + stalemate nodes (forced passes)
            mz = [zs[c] or stal[c] for c in range(n)]
            ra = run_mask(gpath, tpath, 1, mz)
            for nm, lab, side in (('P', '+1', 0), ('M', '-1', 1)):
                r['chess rule mask=zugzwang+stalemate n=' + lab] = dict(
                    pass_nodes=sum(1 for c in range(n) if (zs[c] or stal[c]) and stm[c] == side),
                    states_differ_from_full=diffs(ra[nm], full[nm])[0], quiet_differ_from_full=diffs(ra[nm], full[nm])[1])
            rz = run_mask(gpath, tpath, 1, zs)
            for nm, lab, side in (('P', '+1', 0), ('M', '-1', 1)):
                r['chess rule mask=zugzwang only n=' + lab] = dict(
                    pass_nodes=sum(1 for c in range(n) if zs[c] and stm[c] == side),
                    states_differ_from_full=diffs(rz[nm], full[nm])[0], quiet_differ_from_full=diffs(rz[nm], full[nm])[1])
            # optional-pass rule: stalemated mover may claim the draw or move in T
            fo = run_mask(gpath, tpath, 4, allm)
            mo = run_mask(gpath, tpath, 4, zs)
            for nm, lab, side in (('P', '+1', 0), ('M', '-1', 1)):
                r['optional-pass rule mask=zugzwang n=' + lab] = dict(
                    pass_nodes=sum(1 for c in range(n) if zs[c] and stm[c] == side),
                    states_differ_from_full=diffs(mo[nm], fo[nm])[0], quiet_differ_from_full=diffs(mo[nm], fo[nm])[1])
            # sanity: the optional-pass rule really differs from the chess rule somewhere
            r['optional_vs_chess_full_quiet_placements_differ_at_+1'] = diffs(fo['P'], full['P'])[1]
            r['optional_vs_chess_full_quiet_placements_differ_at_-1'] = diffs(fo['M'], full['M'])[1]
        res[label] = r
    out['rules'] = res
    # compare with K8 explain / pvstats
    ex = os.path.join(BUILDER, 'explain_%s.json' % tag)
    pv = os.path.join(BUILDER, 'pvstats_%s.json' % tag)
    cmpd = {}
    if os.path.exists(ex):
        e = json.load(open(ex))
        c = res['chess']
        cn = e['critical_nodes']
        crit = {k: (cn[k], v) for k, v in dict(
            zugzwang_white=c['zugzwang_white'], zugzwang_black=c['zugzwang_black'],
            zugzwang_white_that_are_kpk=c['zugzwang_white_that_are_kpk'], zugzwang_black_that_are_kpk=c['zugzwang_black_that_are_kpk'],
            forced_pass_white=c['stalemate_white'], forced_pass_black=c['stalemate_black']).items()
            if cn.get(k) != v}
        if crit:
            cmpd['critical_nodes'] = crit
        for key, mine in (('mask_test chess rule n=+1', c['chess rule mask=zugzwang+stalemate n=+1']),
                          ('mask_test chess rule n=-1', c['chess rule mask=zugzwang+stalemate n=-1']),
                          ('mask_test optional-pass rule n=+1', c['optional-pass rule mask=zugzwang n=+1']),
                          ('mask_test optional-pass rule n=-1', c['optional-pass rule mask=zugzwang n=-1'])):
            k8 = e[key]
            m = dict(pass_allowed_at_nodes=mine['pass_nodes'], states_that_differ=mine['states_differ_from_full'],
                     quiet_placements_that_differ=mine['quiet_differ_from_full'])
            if k8 != m:
                cmpd[key] = dict(K8=k8, mine=m)
    if os.path.exists(pv):
        p = json.load(open(pv))['normal play']
        z = res['normal']
        zn = p['zugzwang_nodes']
        mine_zn = dict(total=z['zugzwang_white'] + z['zugzwang_black'], with_pawn=z['zugzwang_with_pawn'],
                       kpk_placements=z['zugzwang_quiet_placements_with_both_sides'])
        if any(zn.get(k) != v for k, v in mine_zn.items()):
            cmpd['pvstats_normal_zugzwang_nodes'] = dict(K8=zn, mine=mine_zn)
        mt = p['mask_tests_quiet_placements_that_differ_from_the_full_result']
        mine_mt = {'all zugzwang nodes': {'n=+1': z['mask=zugzwang n=+1']['quiet_differ_from_full'], 'n=-1': z['mask=zugzwang n=-1']['quiet_differ_from_full']},
                   'no spare move': {'n=+1': z['mask=none n=+1']['quiet_differ_from_full'], 'n=-1': z['mask=none n=-1']['quiet_differ_from_full']}}
        for k, v in mine_mt.items():
            if mt.get(k) != v:
                cmpd['pvstats_mask_' + k] = dict(K8=mt.get(k), mine=v)
        pc = json.load(open(pv))['chess rule']['zugzwang_nodes']
        c = res['chess']
        mine_pc = dict(total=c['zugzwang_white'] + c['zugzwang_black'], with_pawn=c['zugzwang_with_pawn'],
                       kpk_placements=c['zugzwang_quiet_placements_with_both_sides'])
        if any(pc.get(k) != v for k, v in mine_pc.items()):
            cmpd['pvstats_chess_zugzwang_nodes'] = dict(K8=pc, mine=mine_pc)
    out['K8_mismatches'] = cmpd
    out['seconds'] = round(time.time() - t0, 1)
    os.remove(gpath); os.remove(tpath)
    json.dump(out, open(os.path.join(OUT, 'mask_' + tag + '.json'), 'w'))
    print(json.dumps(out), flush=True)
    return len(cmpd)


if __name__ == '__main__':
    sys.exit(1 if sum(main(b) for b in sys.argv[1:]) else 0)
