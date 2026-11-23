"""rgraph.py -- reduced game graph (T50 classes T/L/P/K) on the Moebius strip, its solution with nim-heaps,
the insertion map ins_c, and the node-by-node isomorphism test R_m -> R_{m+1}.  Own code (uses mgame.py only)."""
import sys
from functools import lru_cache
from mgame import Board, parse_ring, fmt

FAM = {
    'F1': (lambda m: ' '.join(['B4 W2'] * m + ['B6 W2 W3 B6 B7 W3 B7 W5'])),
    'F2': (lambda m: ' '.join(['B4 W2'] * m + ['B6 W2 W3 B6 B7 W3 B7 W5 B7'])),
    'F3': (lambda m: ' '.join(['B6 W2 W3 B6 B7 W3'] + ['B7 W5'] * m + ['W6B7'])),
}
# the files of the repeated block (first file, number of files) in F(m)
BLOCK = {'F1': lambda m: (0, 2 * m), 'F2': lambda m: (0, 2 * m), 'F3': lambda m: (6, 2 * m)}

def classify_moves(B, pos, side):
    """returns (T, L, P, K): T,L,P counts and K = list of children (deduplicated, order kept)."""
    T = L = P = 0; K = []
    for desc, ch in B.moves(pos, side):
        c = B.classify(ch, side)
        if c > 0: T += 1; continue
        if c < 0: L += 1; continue
        if any(B.classify(g, 1 - side) > 0 for _, g in B.moves(ch, 1 - side)):
            P += 1; continue
        if ch not in K: K.append(ch)
    return T, L, P, K

def reduced(ring, twist=True):
    root = parse_ring(ring); n = len(root[0]); B = Board(n, twist)
    assert not B.passers(root, 0) and not B.passers(root, 1), 'root has a passed pawn'
    nodes = {root: None}; order = [root]; i = 0
    while i < len(order):
        p = order[i]; i += 1
        info = []
        for side in (0, 1):
            T, L, P, K = classify_moves(B, p, side)
            info.append((T, L, P, K))
            for ch in K:
                if ch not in nodes: nodes[ch] = None; order.append(ch)
        nodes[p] = info
    return B, root, nodes

def solve(nodes, root, H=4):
    """outcome letters of root + *h, h = 0..H, in the reduced game (T-move wins; heap moves keep the position)."""
    memo = {}
    sys.setrecursionlimit(100000)
    def win(p, side, h):
        k = (p, side, h)
        if k in memo: return memo[k]
        T, L, P, K = nodes[p][side]
        w = T > 0 or any(not win(ch, 1 - side, h) for ch in K) or any(not win(p, 1 - side, g) for g in range(h))
        memo[k] = w; return w
    s = ''
    for h in range(H + 1):
        l, r = win(root, 0, h), win(root, 1, h)
        s += 'N' if l and r else 'L' if l else 'R' if r else 'P'
    return s

def ins(pos, c):
    cells, ep = pos
    nc = cells[:c + 1] + (cells[c + 1], cells[c]) + cells[c + 1:]
    if ep and ep[0] > c: ep = (ep[0] + 2,) + ep[1:]
    return (nc, ep)

def stats(nodes, root):
    n = len(root[0])
    K = sum(len(v[s][3]) for v in nodes.values() for s in (0, 1))
    T = sum(v[s][0] for v in nodes.values() for s in (0, 1))
    Tpairs = sum(1 for v in nodes.values() for s in (0, 1) if v[s][0])
    flagged = sum(1 for p in nodes if p[1])
    zone = sorted({f for p in nodes for f in range(n) if p[0][f] != root[0][f]})
    return dict(nodes=len(nodes), K=K, T=T, Tpairs=Tpairs, flagged=flagged, zone=zone)

def iso(nA, rootA, nB, rootB, c):
    """True iff ins_c maps nodes(A) bijectively onto nodes(B), K-children onto K-children (per side), T-flags equal."""
    if ins(rootA, c) != rootB: return False, 'root'
    if len(nA) != len(nB): return False, 'count %d %d' % (len(nA), len(nB))
    for p, info in nA.items():
        q = ins(p, c)
        if q not in nB: return False, 'node ' + fmt(p)
        for s in (0, 1):
            if (info[s][0] > 0) != (nB[q][s][0] > 0): return False, 'T ' + fmt(p)
            if set(ins(x, c) for x in info[s][3]) != set(nB[q][s][3]): return False, 'K ' + fmt(p)
    return True, 'ok'
