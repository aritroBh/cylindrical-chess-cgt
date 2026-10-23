"""extra_checks.py -- side counts quoted in PROOF.md (section 4, 6), recomputed from my own reduced graph of P_18:
  * number of (node, side) pairs with a T-move (note: 555), number of distinct T-moves (1372), K-moves (1643);
  * nodes with an empty file (note: 427), nodes that split into >= 2 components (192), K-captures (240), K-captures
    whose child splits into >= 2 components (58).
A component = maximal cyclic run of non-empty files; a position with no empty file is one ring component.
Several readings of 'splits' are printed so that the note's numbers can be matched or not.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import myeng as M


def ncomp(pos):
    n = len(pos)
    empty = [f for f in range(n) if pos[f] == (0, 0)]
    if not empty:
        return 1
    # runs of non-empty files between consecutive empty files (cyclic)
    runs = 0
    for i, f in enumerate(empty):
        g = empty[(i + 1) % len(empty)]
        gap = (g - f) % n
        if len(empty) == 1:
            gap = n
        if gap > 1:
            runs += 1
    return runs


def main(n=18):
    G = M.Graph(M.P_start(n))
    st = G.stats()
    pairs_T = sum(1 for nd in G.order for c in (0, 1) if G.info[nd][c][0])
    print('P_%d: nodes %d, K %d, T %d, (node,side) pairs with a T-move %d' % (n, st['nodes'], st['K'], st['T'], pairs_T))
    with_empty = sum(1 for p, e in G.order if any(p[f] == (0, 0) for f in range(n)))
    split_nodes = sum(1 for p, e in G.order if ncomp(p) >= 2)
    print('nodes with an empty file %d, nodes with >=2 components %d' % (with_empty, split_nodes))
    caps = 0
    split_child = 0
    split_new = 0
    for nd in G.order:
        p, e = nd
        for c in (0, 1):
            for ch in G.info[nd][c][1]:
                if M.npawns(ch[0]) < M.npawns(p):
                    caps += 1
                    k = ncomp(ch[0])
                    if k >= 2:
                        split_child += 1
                    if k > ncomp(p):
                        split_new += 1
    print('K-captures %d; with child >=2 components %d; with more components than the parent %d' % (caps, split_child, split_new))
    # K-moves that change the file content of an empty-to-nonempty transition are impossible; check that K-captures empty a file
    emptied = 0
    for nd in G.order:
        p, e = nd
        for c in (0, 1):
            for ch in G.info[nd][c][1]:
                if M.npawns(ch[0]) < M.npawns(p):
                    if sum(1 for f in range(n) if ch[0][f] == (0, 0)) > sum(1 for f in range(n) if p[f] == (0, 0)):
                        emptied += 1
    print('K-captures that empty a file: %d' % emptied)


main(int(sys.argv[1]) if len(sys.argv) > 1 else 18)
