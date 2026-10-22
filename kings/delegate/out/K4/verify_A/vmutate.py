"""Verifier A, power check: deliberately wrong rules must produce signatures different from the builder's."""
import json
import os
import sys
import vgraph
import vgames as gm
import vproduct as pr

K4 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sigs(G, nodes):
    sig = ['' for _ in nodes]
    for t in gm.TESTS:
        g = gm.named(t)
        ng = len(g[0])
        res = pr.solve(G, g)
        for i, (a, b) in enumerate(nodes):
            sig[i] += res[a * ng] + res[b * ng]
    return sig


board = sys.argv[1]
G = vgraph.build(board)
nodes = [(G.index[(0, wk, bk, (), 1 << p, 0, -1)], G.index[(1, wk, bk, (), 1 << p, 0, -1)]) for _, wk, p, bk in G.places]
bl = {}
for ln in open(os.path.join(K4, board.replace(':', '_') + '.jsonl')):
    d = json.loads(ln)
    bl[d['placement']] = d['sig']
base = sigs(G, nodes)
print(board, 'baseline differs from builder:', sum(bl[G.places[i][0]] != s for i, s in enumerate(base)), 'of', len(base))
# mutation 1: T moves allowed while in check
save = list(G.incheck)
G.incheck = [False] * G.n
m1 = sigs(G, nodes)
print('  mutation (T moves allowed in check): differs from builder', sum(bl[G.places[i][0]] != s for i, s in enumerate(m1)))
G.incheck = save
# mutation 2: stalemate/no-move rule irrelevant for T=0? -> instead drop the pass: remove all T moves for White only
real_stm = G.stm
orig_flip_pred = G.flip_pred
G.flip = [(-1 if G.stm[i] == 0 else G.flip[i]) for i in range(G.n)]
G.flip_pred = [-1] * G.n
for i in range(G.n):
    if G.flip[i] >= 0:
        G.flip_pred[G.flip[i]] = i
G.incheck = [True if G.stm[i] == 0 else G.incheck[i] for i in range(G.n)]
m2 = sigs(G, nodes)
print('  mutation (White may not move in T): differs from builder', sum(bl[G.places[i][0]] != s for i, s in enumerate(m2)))
