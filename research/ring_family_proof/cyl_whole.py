"""Whole-board cylcgt value of family members (second implementation for the small cases).
Run from the project root:  PYTHONPATH=. .venv/bin/python research/ring_family_proof/cyl_whole.py odd 5 7  (sizes n..)"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam
from cylcgt import pawns, cgt
from cylcgt.pawns import Board, Pos, name

pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
pawns.components = lambda b, p: [p]           # whole-board game: no splitting into components
FILES = "abcdefghijklmnopqrstuvwxyz"

def to_pos(toks):
    W = set(); B = set()
    for f, t in enumerate(toks):
        w, b = fam.split_file(t)
        W |= {(f, r) for r in w}; B |= {(f, r) for r in b}
    return Pos(frozenset(W), frozenset(B))

if __name__ == "__main__":
    famname = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        toks = fam.FAMILIES[famname](n)
        pawns._value.cache_clear()
        t0 = time.time()
        g = pawns.value(Board(n, 8, True, True), to_pos(toks))
        print(f"{famname} n={n} pawns={fam.ntoks_pawns(toks)} whole-board cylcgt value = {cgt.show(g)} ({time.time()-t0:.1f}s)", flush=True)
