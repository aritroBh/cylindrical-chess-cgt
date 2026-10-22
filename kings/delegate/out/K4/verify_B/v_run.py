"""Auditor B driver: recompute every jsonl line of a board from scratch with independent code
(v_gen.py chess graph, v_games.py test games, v_prod.c solver) and compare with the builder's jsonl.
usage: v_run.py flat:3x4 ...   (run from anywhere)"""
import json, os, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
K4 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import v_gen, v_games as vg

WORK = os.path.join(HERE, 'work'); os.makedirs(WORK, exist_ok=True)


def number(game):
    root, d = game
    names = list(d)
    ix = {k: i for i, k in enumerate(names)}
    lines = []
    for k in names:
        l, r = d[k]
        lines.append('%d %s %d %s' % (len(l), ' '.join(str(ix[x]) for x in l), len(r), ' '.join(str(ix[x]) for x in r)))
    return ix[root], lines


def write_games(path, items):
    with open(path, 'w') as f:
        f.write('%d\n' % len(items))
        for nm, g in items:
            st, lines = number(g)
            f.write('%s %d %d\n' % (nm, len(lines), st))
            f.write('\n'.join(lines) + '\n')


def run_c(gpath, tpath, sd):
    out = subprocess.run(['nice', '-n', '10', os.path.join(HERE, 'v_prod'), gpath, tpath, str(sd)],
                         capture_output=True, text=True, check=True).stdout
    res = {}
    for line in out.splitlines():
        nm, s, sw = line.split(' ')
        res[nm] = s
    return res


def main(board):
    t0 = time.time()
    M = v_gen.build(board)
    G = M['G']
    n = len(M['nodes'])
    tag = board.replace(':', '_')
    gpath = os.path.join(WORK, tag + '.graph')
    with open(gpath, 'w') as f:
        f.write('%d\n' % n)
        for i in range(n):
            f.write('%d %d %d %d %s\n' % (M['stm'][i], int(M['incheck'][i]), M['flip'][i], len(M['succ'][i]),
                                           ' '.join(map(str, M['succ'][i]))))
    quiet = [(i, M['flip'][i]) for i, p in enumerate(M['nodes'])
             if p[0] == 0 and p[4] is None and p[3] >= 0 and M['flip'][i] >= 0]
    # candidate signatures, independent
    cands = vg.candidates()
    csig = {nm: vg.signature(V) for nm, V in cands}
    # test games and chess variant
    items = [(t.replace('/', 'o').replace('+-', 'pm').replace('*', 'star') if False else 'T%d' % k, vg.GAMES[t])
             for k, t in enumerate(vg.TESTS)]
    tpath = os.path.join(WORK, tag + '.games')
    write_games(tpath, items)
    R = run_c(gpath, tpath, 0)
    sig = {}
    for (cw, cb) in quiet:
        s = ''
        for k in range(len(vg.TESTS)):
            s += R['T%d' % k][cw] + R['T%d' % k][cb]
        sig[(cw, cb)] = s
    # chess variant (T = 0, stalemate = draw)
    write_games(tpath, [('Z', vg.GAMES['0'])])
    Z = run_c(gpath, tpath, 1)['Z']
    # compare to builder's jsonl
    rows = {r['placement']: r for r in map(json.loads, open(os.path.join(K4, tag + '.jsonl')))}
    by = {}
    for nm, s in csig.items():
        by.setdefault(s, []).append(nm)
    used = set()
    mine = {}
    for (cw, cb) in quiet:
        p = M['nodes'][cw]
        pl = 'K%s P%s k%s' % (v_gen.name(G, p[1]), v_gen.name(G, p[3]), v_gen.name(G, p[2]))
        s = sig[(cw, cb)]
        dec = 'W' if set(s) == {'W'} else 'L' if set(s) == {'L'} else None
        m = by.get(s, [])
        used.update(m)
        mine[pl] = dict(cw=cw, cb=cb, sig=s, dec=dec, matched=m, chess=[Z[cw], Z[cb]])
    cn = dict(cands)
    diffs = {}
    items = [('D%d' % k, vg.neg(cn[v])) for k, v in enumerate(sorted(used))]
    write_games(tpath, items)
    DR = run_c(gpath, tpath, 0)
    for k, v in enumerate(sorted(used)):
        diffs[v] = DR['D%d' % k]
    bad = dict(rowset=0, sig=0, dec=0, matched=0, cls=0, chess=0, diff=0, diff_second=0)
    if set(rows) != set(mine):
        bad['rowset'] = len(set(rows) ^ set(mine))
    for pl, m in mine.items():
        r = rows.get(pl)
        if r is None:
            continue
        bad['sig'] += r['sig'] != m['sig']
        bad['dec'] += r['decisive'] != m['dec']
        bad['matched'] += r['matched'] != m['matched']
        cls = 'WHITE-WINS-ALL' if m['dec'] == 'W' else 'BLACK-WINS-ALL' if m['dec'] == 'L' else '/'.join(m['matched']) if m['matched'] else 'unmatched'
        bad['cls'] += r['cls'] != cls
        bad['chess'] += r['chess'] != m['chess']
        for v in m['matched']:
            a, b = diffs[v][m['cw']], diffs[v][m['cb']]
            d = r['diff'].get(v)
            if d is None or (d['white_starts'], d['black_starts']) != (a, b):
                bad['diff'] += 1
            if d is None or d['second_player'] != (a in 'DL' and b in 'DW'):
                bad['diff_second'] += 1
        bad['diff'] += set(r['diff']) != set(m['matched'])
    print(board, 'quiet placements mine/jsonl', len(mine), len(rows), 'mismatches', bad, '%.1fs' % (time.time() - t0), flush=True)
    return sum(bad.values())


if __name__ == '__main__':
    sys.exit(1 if sum(main(b) for b in sys.argv[1:]) else 0)
