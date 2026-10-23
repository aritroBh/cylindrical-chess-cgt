"""Checks of the wall lemma (Lemma 4 of the proof) with the independent engine rg.

(1) Pure rings: the alternating walls (W3 B5)^j and (W2 B4)^j on C_{2j}, j = 3..30 (n = 6..60): every legal move of every
    pawn is POISONED (class P): the child is non-terminal and the opponent has a capture into a terminal win.
(2) In context: for every node of the reduced game graphs of the three families (n up to 41), and for random walk
    positions, every move of a DEEP pawn (its file and the three files on each side hold the wall pattern) is class P.
Usage: python lemma4_test.py
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph
from lemmaL_test import walkers, classify_many

def pure(wall, j):
    return wall * j

def check_pure():
    tot = 0
    for name, wall in (("odd-type (W3,B5)", ["W3", "B5"]), ("even-type (W2,B4)", ["W2", "B4"])):
        for j in range(3, 31):
            blocks = classify_many([" ".join(pure(wall, j))])
            codes = {}
            for side, code, mv, child in blocks[0]["mv"]:
                codes[code] = codes.get(code, 0) + 1
            assert set(codes) <= {"P"}, (name, j, codes)
            assert blocks[0]["passed"] == "PASSED 0 0"
            tot += sum(codes.values())
    print(f"(1) pure walls on C_6..C_60 (both types, 56 rings): all {tot} moves are class P, none K/T/L.")

def check_context():
    cnt = 0; deep_moves = 0; bad = 0
    texts = []; S_of = []; wall_of = {}
    for famname, ns in (("odd", range(21, 42, 4)), ("even", range(20, 41, 4)), ("F", range(23, 42, 3))):
        for n in ns:
            S = fam.FAMILIES[famname](n); wall_of[id(S)] = fam.wall_files(famname, n)
            g = graph.build(S)
            for p in g.pos:
                texts.append(p); S_of.append(S)
    blocks = classify_many(texts)
    for S, blk in zip(S_of, blocks):
        toks = blk["pos"].split(); n = len(S); wall = wall_of[id(S)]
        for side, code, mv, child in blk["mv"]:
            j = int(mv.split(".")[0])
            if all(((j + d) % n) in wall and toks[(j + d) % n] == S[(j + d) % n] for d in range(-3, 4)):
                deep_moves += 1
                if code != "P": bad += 1
        cnt += 1
    print(f"(2a) reduced-game nodes of odd/even/F rings: {cnt} nodes, {deep_moves} moves of deep pawns, not poisoned: {bad}")
    # random positions: random walks + random zone fills
    rng = random.Random(7)
    tot = 0; bad2 = 0
    for famname in ("odd", "even", "F"):
        snaps = walkers(famname, 400, rng, 7, 14)
        blocks = classify_many([" ".join(p) for n, S, p in snaps])
        for (n, S, p), blk in zip(snaps, blocks):
            if blk["passed"] != "PASSED 0 0": continue
            wall = fam.wall_files(famname, n)
            for side, code, mv, child in blk["mv"]:
                j = int(mv.split(".")[0])
                if all(((j + d) % n) in wall and p[(j + d) % n] == S[(j + d) % n] for d in range(-3, 4)):
                    tot += 1
                    if code != "P": bad2 += 1
    print(f"(2b) random-walk positions (3 families): {tot} moves of deep pawns, not poisoned: {bad2}")
    return bad + bad2

if __name__ == "__main__":
    check_pure()
    sys.exit(1 if check_context() else 0)
