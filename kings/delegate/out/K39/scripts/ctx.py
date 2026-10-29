#!/usr/bin/env python3
"""K39 part 2: contexts H on files e-g of flat 7x6 (ranks 2-5), 1-2 White and 1-2 Black pawns; the 8 roots of Z + H;
the D-model prediction r(H + dud_D) by K26's dmodel.py (Theorem 3.4(a)); and the parked-kings root H + Ka1 ka6.
usage: ctx.py list            -> all contexts, one per line: "<id> <white squares> / <black squares>"
       ctx.py make IDS OUT    -> OUT.zh.in (8 roots per context), OUT.park.in (2 roots), OUT.pred.tsv (id stm pred)"""
import sys, itertools
sys.path.insert(0, '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/scripts')
import dmodel
W, H = 7, 6
SQ = [(f, r) for f in (4, 5, 6) for r in (2, 3, 4, 5)]   # 1-based ranks
nm = lambda s: "abcdefg"[s[0]] + str(s[1])
def contexts():
    out = []
    for nw in (1, 2):
        for w in itertools.combinations(SQ, nw):
            rest = [s for s in SQ if s not in w]
            for nb in (1, 2):
                for b in itertools.combinations(rest, nb):
                    out.append((w, b))
    return out
C = contexts()
if sys.argv[1] == 'list':
    for i, (w, b) in enumerate(C): print(i, " ".join(nm(s) for s in w), "/", " ".join(nm(s) for s in b))
    sys.exit()
ids = [int(x) for x in open(sys.argv[2]).read().split()]
o = sys.argv[3]
ZW, ZBK, ZP = ['b2', 'c3'], ['a4', 'b5'], 'Pa3 Pb4 pb3 pc4'
fz, fp, fr = open(o + '.zh.in', 'w'), open(o + '.park.in', 'w'), open(o + '.pred.tsv', 'w')
for i in ids:
    w, b = C[i]
    ctx = " ".join(["P" + nm(s) for s in w] + ["p" + nm(s) for s in b])
    for x in ZW:
        for y in ZBK:
            for s in 'wb': fz.write(f"K{x} k{y} {ZP} {ctx} {s} -\n")
    for s in 'wb': fp.write(f"Ka1 ka6 {ctx} {s} -\n")
    roots = [(frozenset(w), frozenset(b), None, st) for st in (0, 1)]
    res = dmodel.solve(roots, 'dud', H)
    fr.write(f"{i}\t{res[roots[0]]}\t{res[roots[1]]}\n")
