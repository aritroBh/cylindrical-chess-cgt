"""Re-run the project's own models in a fresh process with a chosen rule order,
compare S and W node by node over the candidate's tree, and count
non-BIG-interior nodes per rule.  Uses cylcgt/ and lemmas/common.py read-only.
Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-reproduce/engine_checks.py <rule order, e.g. opponent,mover,count>
"""
import sys
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from lemmas.common import S, W, WF, NBIG, PBIG, reachable, terminal

order = sys.argv[1].split(",")
x4 = Pos.parse("W: a2 c2 / B: b7 d7")
x8 = Pos.parse("W: a2 c2 g4 / B: b7 d7 g5")
for ep in (False, True):
    b4, b8 = Board(4, 8, False, ep), Board(8, 8, False, ep)
    for rule in order:
        vals = [cgt.show(f(b, x, rule)) for b, x in ((b4, x4), (b8, x8)) for f in (S, W, WF)]
        nodes = [y for y in reachable(b4, x4) if terminal(b4, y) is None]
        mism = sum(1 for y in nodes if S(b4, y, rule) is not W(b4, y, rule))
        nonint = sum(1 for y in nodes if cgt.le(W(b4, y, rule), NBIG) or cgt.le(PBIG, W(b4, y, rule)))
        wfdiff = sum(1 for y in nodes if WF(b4, y, rule) is not W(b4, y, rule))
        ncomp = sum(1 for y in nodes if len(pawns.components(b4, y)) > 1)
        print(f"ep={ep!s:5s} {rule:8s} S4,W4,WF4,S8,W8,WF8={vals} nodes={len(nodes)} "
              f"S!=W nodes={mism} non-interior={nonint} WF!=W nodes={wfdiff} split nodes={ncomp}")
