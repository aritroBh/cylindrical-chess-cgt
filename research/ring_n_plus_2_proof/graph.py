"""Reduced game graph (via the independent engine rg) and its analysis.

Reduced game: from a node (G-position p with its e.p. flag), a move of the side to move is
  * deleted if the child is a terminal loss for the mover (the opponent alone has a passed pawn / wins the race), or
    'poisoned' (non-terminal child, but the opponent has a move to a terminal win for the opponent);
  * an edge to the terminal sink T if the child is a terminal win for the mover;
  * otherwise an edge to the child node.
Heap moves (G + *h) are not part of the graph; see solve().
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam

class Graph:
    def __init__(self):
        self.pos = []                 # list of position strings
        self.edges = []               # list of lists of (side, target(int | 'T'), move)
        self.stat = {}
    def n(self): return len(self.pos)

def build(tokens, extra=()):
    text = " ".join(tokens) + "\n"
    out = fam.run_rg("reduce", text, extra)
    g = Graph()
    for line in out.splitlines():
        if line.startswith("NODE "):
            _, i, rest = line.split(" ", 2)
            assert int(i) == len(g.pos)
            g.pos.append(rest); g.edges.append([])
        elif line.startswith("E "):
            _, side, tgt, mv = line.split(" ", 3)
            g.edges[-1].append((side, tgt if tgt == "T" else int(tgt), mv))
        elif line.startswith("STAT"):
            for kv in line.split()[1:]:
                k, v = kv.split("="); g.stat[k] = int(v)
    return g

def solve(g, H=2, root=0):
    """outcome string over h = 0..H of G + *h  (N / L / R / P), by exhaustive recursion on the reduced graph"""
    sys.setrecursionlimit(1000000)
    memo = {}
    opt = [{"W": [], "B": []} for _ in range(g.n())]
    for i, es in enumerate(g.edges):
        for side, tgt, mv in es: opt[i][side].append(tgt)
    def wins(i, h, side):
        key = (i, h, side)
        r = memo.get(key)
        if r is not None: return r
        other = "B" if side == "W" else "W"
        res = False
        for t in opt[i][side]:
            if t == "T" or not wins(t, h, other): res = True; break
        if not res:
            for h2 in range(h):
                if not wins(i, h2, other): res = True; break
        memo[key] = res
        return res
    sig = ""
    for h in range(H + 1):
        l, r = wins(root, h, "W"), wins(root, h, "B")
        sig += "N" if l and r else "L" if l else "R" if r else "P"
    return sig

def parse_pos(s):
    """position string -> (list of file tokens, ep) with ep = None or ('W'|'B', file)"""
    parts = s.split(); ep = None; toks = []
    for t in parts:
        if t.startswith("ep"):
            ep = (t[2], int(t.split("=")[1]))     # epW=f : the White pawn on file f has just double-stepped
        else: toks.append(t)
    return toks, ep

def strip_ep(s):
    return " ".join(t for t in s.split() if not t.startswith("ep"))

if __name__ == "__main__":
    fname, n = sys.argv[1], int(sys.argv[2])
    toks = fam.FAMILIES[fname](n)
    g = build(toks)
    nodes_noep = len({strip_ep(p) for p in g.pos})
    print(fname, n, "nodes", g.n(), "nodes ignoring ep", nodes_noep, "edges(nonterminal)", sum(1 for es in g.edges for e in es if e[1] != "T"),
          "terminal edges", sum(1 for es in g.edges for e in es if e[1] == "T"), g.stat, "G+*h:", solve(g, 7))
