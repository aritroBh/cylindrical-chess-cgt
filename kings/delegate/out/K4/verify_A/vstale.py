import sys, json, os
import vgraph, vgames as gm, vproduct as pr, vchess
K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for b in sys.argv[1:]:
    G = vgraph.build(b, allkpk=True)
    cv = vchess.chess_variant(G)
    res = pr.solve(G, gm.named('0'))
    d_all = sum(1 for x in range(G.n) if res[x] != cv[x])
    d_pawn = sum(1 for x in range(G.n) if res[x] != cv[x] and G.pos[x][4])
    m = json.load(open(os.path.join(K4, 'meta_%s.json' % b.replace(':', '_'))))['check1']
    print(b, 'nodes where (stalemate=loss) differs from chess: all', d_all, 'with pawn', d_pawn, '| builder stale_loss_all', m['stale_loss_all'], 'stale_loss_kpk', m['stale_loss_kpk'])
