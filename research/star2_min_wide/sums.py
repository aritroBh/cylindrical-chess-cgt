#!/usr/bin/env python3
"""sums.py: part (b).  Every position with an empty interior file is the disjoint sum of its parts (maximal runs of occupied
files).  A root has no passed pawn, so each part is itself a no-passer position with >= 1 pawn of each colour (>= 2 pawns), hence
a connected root enumerated in parts_k{k}.tsv.  With <= 7 pawns a gapped position is one of the shapes
    (2,2) (2,3) (2,4) (2,5) (3,3) (3,4)  and  (2,2,2) (2,2,3).
We ask, for target T in {0,*1,*2,*3}: does any choice of parts (class values from cylcgt, default setting) add up to T?
Equality of short games = identity of canonical forms, so  g1+g2 = T  <=>  g1 = T - g2  (a membership test, no product of big games).
Geometry (does the placement fit in 8 files / any width) is ignored: if no class combination reaches *2 there is nothing to place;
combinations that do reach a target are counted with their position multiplicities."""
import sys, time, collections, itertools
from common import *

t0 = time.time()
K = 5
classes = {}          # k -> OrderedDict: Game -> [count of mirror-reduced position classes, example]
for k in range(2, K + 1):
    cl = collections.OrderedDict()
    for line in open(f"parts_k{k}.tsv"):
        if line.startswith("#"): continue
        text, width, nw, nb, o, n, shown = line.rstrip("\n").split("\t")
        W, B = parse_pos(text); width = int(width)
        g = value_of_part(width, W, B)
        # mirror invariance of the value (rules are left-right symmetric): check it, do not assume it
        m = mirror_part(width, frozenset(W), frozenset(B))
        gm = value_of_part(*m)
        assert gm is g, ("mirror value differs", text)
        assert (cgt.outcome(g), g.nim if g.nim is not None else -1) == (o, int(n)), ("tsv mismatch", text)
        ent = cl.setdefault(g, [0, text]); ent[0] += 1
    classes[k] = cl
    print(f"k={k}: {sum(e[0] for e in cl.values())} part classes, {len(cl)} distinct cylcgt values  ({time.time()-t0:.0f}s)", flush=True)

def star(n): return cgt.nimber(n)
targets = [("0", cgt.ZERO), ("*1", star(1)), ("*2", star(2)), ("*3", star(3))]

def combos(V_list, T):
    """number of (class tuple, position tuple) choices from classes V_list (list of OrderedDict) whose sum equals T.
    Position multiplicity counts ordered placements only up to the per-part mirror reduction (indicative)."""
    # fold all but the last part into a dict {sum game: multiplicity}, then test T - g_last membership
    acc = {cgt.ZERO: 1}
    for cl in V_list[:-1]:
        nxt = collections.defaultdict(int)
        for s, ms in acc.items():
            for g, (cnt, _) in cl.items():
                nxt[cgt.add(s, g)] += ms * cnt
        acc = nxt
    class_hits = pos_hits = 0
    last = V_list[-1]
    for g, (cnt, _) in last.items():
        need = cgt.add(T, cgt.neg(g))          # s + g = T  <=>  s = T - g
        if need in acc:
            class_hits += 1; pos_hits += acc[need] * cnt
    return class_hits, pos_hits

shapes = [(2,2), (2,3), (2,4), (2,5), (3,3), (3,4), (2,2,2), (2,2,3)]
out = []
print("\nshape      pawns  " + "  ".join(f"{n:>20s}" for n, _ in targets))
for sh in shapes:
    row = []
    for name, T in targets:
        ch, ph = combos([classes[k] for k in sh], T)
        row.append(f"{ch:6d} cls {ph:11d} pos")
    print(f"{str(sh):10s} {sum(sh):3d}    " + "  ".join(f"{r:>20s}" for r in row), flush=True)
    out.append((sh, row))
print(f"elapsed {time.time()-t0:.0f}s")
