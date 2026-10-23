"""Lemma 2 (wall pawns) exactly as stated in proof.tex, tested with the independent engine rg.
(b) positions without passed pawn and without e.p. flag; a wall pawn q whose files j-1..j+3 or j-3..j+1 are pattern files:
    every move of q is class L or P.
(a) positions without passed pawn (e.p. flag allowed); the player to move is the one NOT protected by the flag; a wall pawn q of that
    player with pattern files j-1,j,j+1: after any move of q the mover has no passed pawn.
Positions: all reduced-game nodes of the three families and random walks from the starts (e.p. flags allowed in the walks).
Usage: python lemma2_test.py"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph
from lemmaL_test import walkers, classify_many

def pat(S, toks, wall, n, files):
    return all((f % n) in wall and toks[f % n] == S[f % n] for f in files)

def main():
    rng = random.Random(5)
    tb = bb = ta = ba = 0
    for famname, ns in (("odd", range(17, 42, 8)), ("even", range(16, 41, 8)), ("F", range(19, 42, 7))):
        snaps = []
        for n in ns:
            S = fam.FAMILIES[famname](n); g = graph.build(S)
            snaps += [(n, S, p.split()) for p in g.pos]
        snaps += walkers(famname, 1500, rng, 7, 16, allow_ep=True)
        blocks = classify_many([" ".join(p) for n, S, p in snaps])
        for (n, S, p), blk in zip(snaps, blocks):
            if blk["passed"] != "PASSED 0 0": continue
            wall = fam.wall_files(famname, n)
            toks = blk["pos"].split()[:n]
            ept = [x for x in blk["pos"].split() if x.startswith("ep")]
            holder = None
            if ept: holder = "B" if ept[0].startswith("epW") else "W"       # epW=f: a white pawn doubled, black may capture e.p.
            for (side, code, mv, child), pp in zip(blk["mv"], blk["pp"]):
                j = int(mv.split(".")[0])
                if not ept and (pat(S, toks, wall, n, range(j - 1, j + 4)) or pat(S, toks, wall, n, range(j - 3, j + 2))):
                    tb += 1; bb += code not in "LP"
                if (not ept or side == holder) and pat(S, toks, wall, n, range(j - 1, j + 2)):
                    ta += 1; ba += pp[0 if side == "W" else 1] == "1"
    print(f"Lemma 2(b): {tb} moves of wall pawns with a 5-file pattern window, not L/P: {bb}.  Lemma 2(a): {ta} moves of wall pawns, mover obtains a passed pawn: {ba}")
    return bb + ba

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
