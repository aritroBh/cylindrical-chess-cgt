#!/usr/bin/env python3
"""sample_check.py FILE.rings [...] -- check the rings emitted by enum_rings (token syntax "W4B7 B6 W2 ...") on C9, 10 pawns.

For every ring: 9 files, every file has a pawn, white/black on ranks 2..7 only, no two pawns on a square, exactly 10 pawns,
no passed pawn by (a) a literal loop over the expanded board written here and (b) the project library cylcgt
(pawns.passed on Board(9, 8, wrap=True, ep=True), no e.p. at the root).  Also: all rings of the given files have pairwise distinct
dihedral canonical forms (colours not exchanged), and the ring is the lexicographically smallest image under the 18 dihedral
elements when compared as (white-set, black-set) tuples per file in the enumerator's code order is NOT tested (code order is
internal), only distinctness of orbits.
env RING_N (default 9) and RING_P (default 10) set the cylinder size and pawn total.
run from the project root:  PYTHONPATH=. .venv/bin/python research/c9_rings/validate/sample_check.py FILES
"""
import sys, os, re, collections
sys.path.insert(0, ".")
from cylcgt import pawns

N = int(os.environ.get("RING_N", "9"))
PTOT = int(os.environ.get("RING_P", "10"))
BOARD = pawns.Board(N, 8, True, True)
TOK = re.compile(r"^(?:W([2-7]+))?(?:B([2-7]+))?$")


def parse(line):
    toks = line.split()
    assert len(toks) == N, line
    W, B = [], []
    for t in toks:
        m = TOK.match(t)
        assert m and t, "bad token %r in %r" % (t, line)
        W.append(tuple(int(c) for c in (m.group(1) or "")))
        B.append(tuple(int(c) for c in (m.group(2) or "")))
    return W, B


def literal(W, B):
    for f in range(N):
        nb = [(f - 1) % N, f, (f + 1) % N]
        for r in W[f]:
            if not any(q > r for g in nb for q in B[g]):
                return False
        for r in B[f]:
            if not any(q < r for g in nb for q in W[g]):
                return False
    return True


def canon(W, B):
    best = None
    for t in range(N):
        for refl in (0, 1):
            idx = [(t - i) % N if refl else (i + t) % N for i in range(N)]
            img = tuple((W[j], B[j]) for j in idx)
            if best is None or img < best:
                best = img
    return best


def main():
    seen = {}
    tot = 0
    for fn in sys.argv[1:]:
        cnt = collections.Counter()
        for line in open(fn):
            if not line.strip():
                continue
            W, B = parse(line)
            tot += 1
            cnt["rings"] += 1
            nw, nb = sum(map(len, W)), sum(map(len, B))
            ok = nw + nb == PTOT and all(len(W[f]) + len(B[f]) >= 1 for f in range(N))
            ok = ok and all(len(set(W[f])) == len(W[f]) and len(set(B[f])) == len(B[f]) and not (set(W[f]) & set(B[f])) for f in range(N))
            if not ok:
                cnt["BAD_STRUCTURE"] += 1
                continue
            if not literal(W, B):
                cnt["BAD_literal_has_passer"] += 1
            pos = pawns.Pos(frozenset((f, r) for f in range(N) for r in W[f]), frozenset((f, r) for f in range(N) for r in B[f]))
            if pawns.passed(BOARD, pos, "W") or pawns.passed(BOARD, pos, "B"):
                cnt["BAD_cylcgt_passed"] += 1
            c = canon(W, B)
            if c in seen:
                cnt["BAD_duplicate_orbit"] += 1
            seen[c] = fn
            cnt["split_%d+%d" % (nw, nb)] += 1
        print("%s: %s" % (fn.split("/")[-1], dict(cnt)))
    print("total rings %d, distinct orbits %d" % (tot, len(seen)))


main()
