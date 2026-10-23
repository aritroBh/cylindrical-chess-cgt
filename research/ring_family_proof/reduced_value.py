"""Third check of the base cases: the canonical-form value of the REDUCED game, computed bottom-up with cylcgt's CGT arithmetic
(cgt.make: dominated and reversible options removed), is exactly *2.  (Reduced game = game tree of G with the L- and P-moves
deleted; T-moves are the integers +-BIG.)  By Lemma 1 the reduced game has the same outcome as G in every sum G + *h, so a value
*2 here proves G + *2 is a P-position, by a route that does not use my outcome search at all.
Run from the project root: PYTHONPATH=. .venv/bin/python research/ring_family_proof/reduced_value.py odd 5 7 9 ... """
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam
from cylcgt import pawns, cgt
from cylcgt.pawns import Board
from reduced_cyl import to_pos, moves, term, other, key
sys.setrecursionlimit(100000)

def value_of(toks):
    n = len(toks); board = Board(n, 8, True, True)
    from difftest import norm_ep
    memo = {}
    def val(pos):
        r = memo.get(pos)
        if r is not None: return r
        opts = {"W": [], "B": []}
        for side in ("W", "B"):
            opp = other(side)
            for ch in moves(board, pos, side):
                t = term(board, ch, side)
                if t == 1: opts[side].append(cgt.integer(pawns.BIG if side == "W" else -pawns.BIG)); continue
                if t == -1: continue
                if any(term(board, c2, opp) == 1 for c2 in moves(board, ch, opp)): continue
                opts[side].append(val(ch))
        g = cgt.make(opts["W"], opts["B"])
        memo[pos] = g
        return g
    return val(norm_ep(board, to_pos(toks))), len(memo)

if __name__ == "__main__":
    famname = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        t0 = time.time()
        g, nn = value_of(fam.FAMILIES[famname](n))
        print(f"{famname} n={n}: reduced game ({nn} nodes) has canonical value {cgt.show(g)}   ({time.time()-t0:.1f}s)", flush=True)
