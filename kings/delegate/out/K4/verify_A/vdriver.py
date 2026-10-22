"""Verifier A, module 5: driver.  usage: vdriver.py <flat|cyl>:WxH [--kp PATH]

Computes the 32-entry signature (16 test games x 2 starters) of every quiet placement, the candidate
matches, the difference tests, the chess variant, and compares all of it with the builder's jsonl.
"""
import json
import os
import sys
import time
import vgraph
import vgames as gm
import vproduct as pr
import vchess

K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))


def log(*a):
    print('[%7.1fs]' % (time.time() - T0), *a, flush=True)


def candidate_sigs():
    cands = gm.all_candidates()
    tests = [gm.named(t) for t in gm.TESTS]
    sig = {}
    for name, v in cands.items():
        s = ''
        for t in tests:
            a, b = pr.solve_pure(gm.add(v, t))
            s += a + b
        sig[name] = s
    return cands, sig


def main():
    global T0
    T0 = time.time()
    board = sys.argv[1]
    kp = sys.argv[sys.argv.index('--kp') + 1] if '--kp' in sys.argv else None
    tag = board.replace(':', '_')
    G = vgraph.build(board)
    log(board, 'graph: nodes', G.n, 'edges', sum(map(len, G.succ)), 'quiet placements', len(G.places))
    cands, csig = candidate_sigs()
    bcand = json.load(open(os.path.join(K4, 'candidates.json')))['candidates']
    cdiff = {k: (csig.get(k), bcand.get(k)) for k in set(csig) | set(bcand) if csig.get(k) != bcand.get(k)}
    log('candidate signatures: mine', len(csig), 'builder', len(bcand), 'differ', len(cdiff))
    nodes = []
    for name, wk, p, bk in G.places:
        nodes.append((G.index[(0, wk, bk, (), 1 << p, 0, -1)], G.index[(1, wk, bk, (), 1 << p, 0, -1)]))
    sig = ['' for _ in G.places]
    for t in gm.TESTS:
        g = gm.named(t)
        ng = len(g[0])
        res = pr.solve(G, g)
        for i, (x0, x1) in enumerate(nodes):
            sig[i] += res[x0 * ng] + res[x1 * ng]
        log('test game', t, 'solved')
    bysig = {}
    for name, s in csig.items():
        bysig.setdefault(s, []).append(name)
    rows = []
    for i, (name, wk, p, bk) in enumerate(G.places):
        s = sig[i]
        dec = 'W' if set(s) == {'W'} else 'L' if set(s) == {'L'} else None
        rows.append({'placement': name, 'sig': s, 'decisive': dec, 'matched': sorted(bysig.get(s, []))})
    used = sorted({v for r in rows for v in r['matched']})
    for v in used:
        ng_game = gm.neg(cands[v])
        ng = len(ng_game[0])
        res = pr.solve(G, ng_game)
        for i, r in enumerate(rows):
            if v in r['matched']:
                x0, x1 = nodes[i]
                a, b = res[x0 * ng], res[x1 * ng]
                r.setdefault('diff', {})[v] = {'white_starts': a, 'black_starts': b,
                                                'second_player': a in 'DL' and b in 'DW'}
        log('difference test for', v)
    cv = vchess.chess_variant(G)
    for i, r in enumerate(rows):
        r['chess'] = [cv[nodes[i][0]], cv[nodes[i][1]]]
    # ---- kpsolve cross-check of the chess variant, on every graph node
    kpinfo = None
    if kp:
        lines = [vchess.pos_line(G, p) for p in G.pos]
        out = vchess.run_kpsolve(G, kp, lines)
        assert len(out) == len(lines), (len(out), len(lines))
        diffs, kpk, kpk_diffs, inexact = 0, 0, 0, 0
        examples = []
        for x, (left, a, b) in enumerate(out):
            assert left == lines[x], (left, lines[x])
            if a != b:
                inexact += 1
            haspawn = bool(G.pos[x][4])
            kpk += haspawn
            if not (a == b == cv[x]):
                diffs += 1
                kpk_diffs += haspawn
                if len(examples) < 10:
                    examples.append((lines[x], cv[x], a, b))
        kpinfo = {'compared_all_nodes': len(out), 'compared_with_pawn': kpk, 'diffs_all': diffs,
                  'diffs_with_pawn': kpk_diffs, 'inexact': inexact, 'examples': examples}
        log('kpsolve cross-check', kpinfo)
    # ---- compare with the builder's jsonl
    bl = {}
    for ln in open(os.path.join(K4, tag + '.jsonl')):
        d = json.loads(ln)
        bl[d['placement']] = d
    mine = {r['placement']: r for r in rows}
    cmp = {'board': board, 'placements_mine': len(mine), 'placements_builder': len(bl),
           'only_mine': sorted(set(mine) - set(bl))[:5], 'only_builder': sorted(set(bl) - set(mine))[:5],
           'compared': 0, 'sig_diff': 0, 'matched_diff': 0, 'decisive_diff': 0, 'diff_test_diff': 0,
           'chess_diff': 0, 'chess_diff_reversed_order_would_match': 0, 'examples': []}
    for name, r in mine.items():
        b = bl.get(name)
        if not b:
            continue
        cmp['compared'] += 1
        bad = []
        if r['sig'] != b['sig']:
            cmp['sig_diff'] += 1
            bad.append('sig')
        if r['matched'] != sorted(b['matched']):
            cmp['matched_diff'] += 1
            bad.append('matched')
        if (r['decisive'] or None) != (b['decisive'] or None):
            cmp['decisive_diff'] += 1
            bad.append('decisive')
        if r.get('diff', {}) != b.get('diff', {}):
            cmp['diff_test_diff'] += 1
            bad.append('diff')
        if r['chess'] != b['chess']:
            cmp['chess_diff'] += 1
            bad.append('chess')
        if bad and len(cmp['examples']) < 12:
            cmp['examples'].append({'placement': name, 'what': bad, 'mine': {k: r.get(k) for k in ('sig', 'matched', 'decisive', 'chess', 'diff')},
                                    'builder': {k: b.get(k) for k in ('sig', 'matched', 'decisive', 'chess', 'diff')}})
    cls = {}
    for r in rows:
        k = 'WHITE-WINS-ALL' if r['decisive'] == 'W' else 'BLACK-WINS-ALL' if r['decisive'] == 'L' else '/'.join(r['matched']) or 'unmatched'
        cls[k] = cls.get(k, 0) + 1
    bcls = {}
    for b in bl.values():
        bcls[b['cls']] = bcls.get(b['cls'], 0) + 1
    cmp.update({'classes_mine': cls, 'classes_builder': bcls, 'candidate_sig_diffs': cdiff, 'kpsolve': kpinfo,
                'seconds': round(time.time() - T0, 1)})
    json.dump(cmp, open(os.path.join(HERE, 'result_%s.json' % tag), 'w'), indent=1)
    json.dump(rows, open(os.path.join(HERE, 'rows_%s.json' % tag), 'w'))
    log('DONE', {k: cmp[k] for k in ('compared', 'sig_diff', 'matched_diff', 'decisive_diff', 'diff_test_diff', 'chess_diff')})


if __name__ == '__main__':
    main()
