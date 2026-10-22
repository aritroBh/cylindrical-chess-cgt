"""Solve G + *h on a dumped reduced graph (edges: position, side, move, child|TERMINAL-WIN).
A node's kept moves are exactly the listed edges (deleted moves lose at once); heap moves reduce h to any smaller value."""
import sys, functools
sys.setrecursionlimit(100000)
def load(path):
    out = {}
    root = None
    for l in open(path):
        a, side, mv, b = l.rstrip("\n").split("\t")
        if root is None: root = a
        out.setdefault(a, {"W": [], "B": []})[side].append(b)
    return root, out
def solve(path, hmax=7):
    root, g = load(path)
    @functools.lru_cache(maxsize=None)
    def wins(p, h, side):          # does `side` win moving first in (p, *h)?
        opts = g.get(p, {"W": [], "B": []})[side]
        if any(b == "TERMINAL-WIN" for b in opts): return True
        opp = "B" if side == "W" else "W"
        if any(not wins(b, h, opp) for b in opts if b != "TERMINAL-WIN"): return True
        return any(not wins(p, h2, opp) for h2 in range(h))
    sig = ""
    for h in range(hmax + 1):
        l, r = wins(root, h, "W"), wins(root, h, "B")
        sig += "N" if l and r else "L" if l else "R" if r else "P"
    return root, sig, len(g)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        root, sig, nn = solve(p)
        print(f"{p}: root {root}: outcomes of G+*h for h=0..7: {sig}   (nodes with moves: {nn})")
