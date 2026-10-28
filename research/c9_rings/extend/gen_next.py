#!/usr/bin/env python3
"""gen_next.py OUT_CAND.tsv K SRC.tsv [SRC2.tsv ...] --exclude SOLVED.tsv ...
For every *2/*3 ring (P at h=2 or h=3) in the SRC result files insert K single-pawn files (K=1: every single token at every cut;
K=2: every ordered pair) and keep the legal root rings (no passed pawn; cross-checked against cylcgt.pawns.passed), deduplicated
up to the dihedral group (colours not exchanged).  Rings that already have a result in an --exclude file are dropped from the
candidate list (their result is reused).  Prints the counts and writes OUT_CAND.tsv (ring <TAB> provenance)."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ringlib import *
a = sys.argv[1:]
out, K = a[0], int(a[1])
rest = a[2:]
excl = []
if "--exclude" in rest:
    i = rest.index("--exclude"); excl = rest[i + 1:]; rest = rest[:i]
src = rest
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from cylcgt import pawns
def cyl_legal(ring):
    cfg = parse(ring); n = len(cfg)
    W = frozenset((f, r) for f, (w, b) in enumerate(cfg) for r in w)
    B = frozenset((f, r) for f, (w, b) in enumerate(cfg) for r in b)
    bd = pawns.Board(n, 8, True, True); p = pawns.Pos(W, B)
    return not pawns.passed(bd, p, "W") and not pawns.passed(bd, p, "B")
hits = {}
for fn in src:
    for l in open(fn):
        f = l.rstrip("\n").split("\t")
        if len(f) >= 2 and (f[1][2:3] == "P" or f[1][3:4] == "P") and f[1] != "UNRESOLVED":
            hits[canon(f[0])] = f[1]
solved = set()
for fn in excl:
    for l in open(fn):
        if l.strip():
            solved.add(canon(l.split("\t")[0]))
total = legal_n = mism = 0
cand = {}
for r in sorted(hits):
    for c, ins, new in insertions(r, K):
        total += 1
        ok = passed_free(new)
        if ok != cyl_legal(new): mism += 1
        if ok:
            legal_n += 1
            cand.setdefault(canon(new), []).append("%s@%d:%s" % (npawns(r) and "src%d" % len(r.split()), c, "+".join(ins)))
new_c = {k: v for k, v in cand.items() if k not in solved}
n0 = len(next(iter(hits)).split()) if hits else 0
print("%s: sources %d (C%d, %d pawns), insert %d: generated %d, legal %d, distinct %d, already solved %d, new %d, legality mismatches vs cylcgt %d"
      % (os.path.basename(out), len(hits), n0, npawns(next(iter(hits))) if hits else 0, K, total, legal_n, len(cand), len(cand) - len(new_c), len(new_c), mism))
with open(out, "w") as f:
    for r in sorted(new_c):
        f.write("%s\t%s\n" % (r, ";".join(new_c[r][:6])))
