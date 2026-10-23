"""Second implementation of the reduced game graph, built on the project's cylcgt move generator / passed test /
race rule (pawns.moves, pawns._child), and compared edge-for-edge with the independent C engine rg.
Run from the project root:  PYTHONPATH=. .venv/bin/python research/ring_family_proof/reduced_cyl.py odd 9 17
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fam, graph
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
from difftest import norm_ep, to_tok

pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True
BIG = pawns.BIG

def to_pos(toks):
    W = set(); B = set()
    for f, t in enumerate(toks):
        w, b = fam.split_file(t)
        W |= {(f, r) for r in w}; B |= {(f, r) for r in b}
    return Pos(frozenset(W), frozenset(B))

def key(board, pos):
    return to_tok(pos, board.files)

def other(s): return "B" if s == "W" else "W"

def term(board, pos, side):
    """+1 / -1 / 0 : the position `pos`, reached by a move of `side`, is a terminal win / loss for `side`, or non-terminal.
    Uses cylcgt's passed test and, for races, its race rule (pawns._child); never computes game values."""
    wp, bp = pawns.passed(board, pos, "W"), pawns.passed(board, pos, "B")
    if wp and bp:
        v = pawns._child(board, pos, side)           # race rule: returns an integer game
        return 1 if ((v.num > 0) == (side == "W")) else -1
    if not wp and not bp: return 0
    return 1 if (wp == (side == "W")) else -1

def moves(board, pos, side):
    plain = Pos(pos.white, pos.black, None)
    lpos = plain if (pos.ep and pos.ep[2] != side) else pos
    return [norm_ep(board, c) for c in pawns.moves(board, lpos, side)]

def build(toks):
    n = len(toks); board = Board(n, 8, True, True)
    start = norm_ep(board, to_pos(toks))
    seen = {start}; stack = [start]; edges = set()
    while stack:
        pos = stack.pop()
        for side in ("W", "B"):
            for ch in moves(board, pos, side):
                t = term(board, ch, side)
                if t == 1: edges.add((key(board, pos), side, "T")); continue
                if t == -1: continue
                opp = other(side)
                if any(term(board, c2, opp) == 1 for c2 in moves(board, ch, opp)): continue
                edges.add((key(board, pos), side, key(board, ch)))
                if ch not in seen: seen.add(ch); stack.append(ch)
    return edges, {key(board, p) for p in seen}

if __name__ == "__main__":
    famname = sys.argv[1]
    for n in map(int, sys.argv[2:]):
        toks = fam.FAMILIES[famname](n)
        t0 = time.time()
        e2, nodes2 = build(toks)
        g = graph.build(toks)
        e1 = set()
        for i, es in enumerate(g.edges):
            for side, tgt, mv in es:
                e1.add((g.pos[i], side, "T" if tgt == "T" else g.pos[tgt]))
        print(f"{famname} n={n}: cylcgt-based reduced graph: {len(nodes2)} nodes, {len(e2)} (src,side,target) edges; "
              f"C engine: {g.n()} nodes, {len(e1)} edges; identical: {e1 == e2 and set(g.pos) == nodes2}  ({time.time()-t0:.0f}s)", flush=True)
