"""Second implementation of the terminal/non-terminal split, reusing the worker's
freeze.py geometry and cylcgt's passed() (read-only imports): a placement passes the
'non-terminal' criterion if no interaction occurs at any configuration without a passer.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C7-theory/split_with_worker_code.py"""
import sys, os
sys.path.insert(0, "atlas/cylinder")
import freeze as FZ
from cylcgt import pawns
from cylcgt.pawns import Board, Pos
for text in ["W: a2 c2 / B: b7 d7", "W: a2 b3 c3 / B: a6 b5 b7"]:
    W, B = FZ.parse(text); W, B, width = FZ.trim(W, B)
    nodes = FZ.reachable(width, W, B)
    bd = Board(width, 8, False, True)
    nonterm = [(a, b) for a, b in nodes if not (pawns.passed(bd, Pos(a, b), "W") or pawns.passed(bd, Pos(a, b), "B"))]
    for wrap in (False, True):
        allc = sum(FZ.check_placement(nodes, width, *p, wrap)[0] for p in FZ.placements(width))
        nt = sum(FZ.check_placement(nonterm, width, *p, wrap)[0] for p in FZ.placements(width))
        tot = len(list(FZ.placements(width)))
        print(f"{text}: {'cyl8' if wrap else 'flat8'}  conservative (all nodes) {allc}/{tot}   non-terminal nodes only {nt}/{tot}")
    ok = FZ.check_placement(nonterm, width, 0, False, 1, 4, True)
    print("   placement o=0 no-mirror WK h5 BK f4 on cyl8, non-terminal criterion:", ok, FZ.fen(W, B, width, 0, False, 1, 4))
