#!/usr/bin/env python3
"""sums_hits.py: list every pair of part classes (3 pawns, 4 pawns) whose cylcgt sum is *2 or *3, with the part positions.
(Companion of sums.py; the (3,4) row of its table is the only one with *2 / *3 sums.)"""
import collections, sys
from common import *
classes = {}
for k in (3, 4):
    cl = collections.OrderedDict()
    for line in open(f"parts_k{k}.tsv"):
        if line.startswith("#"): continue
        text, width, nw, nb, o, n, shown = line.rstrip("\n").split("\t")
        W, B = parse_pos(text); g = value_of_part(int(width), W, B)
        cl.setdefault(g, []).append((text, int(width)))
    classes[k] = cl
for name, T in (("*2", cgt.nimber(2)), ("*3", cgt.nimber(3))):
    print(f"== pairs (3-pawn part, 4-pawn part) with sum = {name}")
    acc = classes[3]
    for g4, plist4 in classes[4].items():
        need = cgt.add(T, cgt.neg(g4))
        if need in acc:
            print(f"  4-pawn class value {cgt.show(g4)[:90]}   ({len(plist4)} position classes up to mirror)")
            print(f"     e.g. {plist4[:4]}")
            print(f"  3-pawn class value {cgt.show(need)[:90]}  ({len(acc[need])} position classes up to mirror)")
            print(f"     e.g. {acc[need][:4]}")
            print(f"     outcome 3-part={cgt.outcome(need)} nim={need.nim}; 4-part={cgt.outcome(g4)} nim={g4.nim}")
