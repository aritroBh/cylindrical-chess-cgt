import json, sys, os
import vgraph
K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
boards = ['3x4', '4x4', '3x5', '4x5', '5x5']
def cls(r):
    return 'WHITE-WINS-ALL' if r['decisive'] == 'W' else 'BLACK-WINS-ALL' if r['decisive'] == 'L' else '/'.join(r['matched']) or 'unmatched'
for wh in boards:
    F = json.load(open('rows_flat_%s.json' % wh)); C = json.load(open('rows_cyl_%s.json' % wh))
    cf, cc = {}, {}
    ex = {}
    for kind, rows, d in (('flat', F, cf), ('cyl', C, cc)):
        for r in rows:
            k = cls(r); d[k] = d.get(k, 0) + 1; ex.setdefault((kind, k), r['placement'])
    print('==', wh)
    for k in sorted(set(cf) | set(cc), key=lambda k: -(cf.get(k, 0) + cc.get(k, 0))):
        print('  %-18s flat %5d (%s)  cyl %5d (%s)' % (k, cf.get(k, 0), ex.get(('flat', k), '-'), cc.get(k, 0), ex.get(('cyl', k), '-')))
    # same placement, different class
    fm = {r['placement']: cls(r) for r in F}; cm = {r['placement']: cls(r) for r in C}
    common = set(fm) & set(cm)
    chg = [(p, fm[p], cm[p]) for p in sorted(common) if fm[p] != cm[p]]
    print('  placements on both boards:', len(common), 'class changes:', len(chg))
    # number of distinct signatures
    print('  distinct unmatched sigs flat/cyl:', len({r['sig'] for r in F if not r['matched'] and r['decisive'] is None}), len({r['sig'] for r in C if not r['matched'] and r['decisive'] is None}))
    ints = [r for r in F + C if set(r['matched']) & {'0', '1', '2', '-1', '-2'}]
    print('  integer-class placements:', len(ints))
# stalemate counts in my graph, to compare with the builder's meta
for b in ('flat:3x4', 'cyl:3x4', 'flat:4x4'):
    G = vgraph.build(b)
    stale_all = sum(1 for x in range(G.n) if not G.succ[x] and not G.incheck[x])
    stale_pawn = sum(1 for x in range(G.n) if not G.succ[x] and not G.incheck[x] and G.pos[x][4])
    m = json.load(open(os.path.join(K4, 'meta_%s.json' % b.replace(':', '_'))))
    print(b, 'mine stalemate nodes all/with pawn', stale_all, stale_pawn, 'builder stale_loss_all/kpk', m['check1']['stale_loss_all'], m['check1']['stale_loss_kpk'])
