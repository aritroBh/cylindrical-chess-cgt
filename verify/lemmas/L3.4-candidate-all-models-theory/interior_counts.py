"""How many non-terminal nodes of the candidate's tree violate BIG-interiority
(hypothesis of Theorem 3.3(b)), per rule and e.p. setting? Project code read-only.
Run: cd <root> && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-theory/interior_counts.py"""
import sys; sys.setrecursionlimit(1_000_000)
from cylcgt import cgt
from cylcgt.pawns import Board, Pos
from lemmas.common import NBIG, PBIG, RULES, W, WF, reachable, terminal
X = Pos.parse("W: a2 c2 / B: b7 d7")
for ep in (True, False):
    b = Board(4, 8, False, ep)
    for rule in RULES:
        nodes = [z for z in reachable(b, X) if terminal(b, z) is None]
        bad = [z for z in nodes if cgt.le(W(b, z, rule), NBIG) or cgt.le(PBIG, W(b, z, rule))]
        diff = [z for z in nodes if W(b, z, rule) is not WF(b, z, rule)]
        print(f"ep={ep!s:5} {rule:8}: non-BIG-interior nodes {len(bad)}, WF!=W nodes {len(diff)}, same set: {set(bad)==set(diff)}")
