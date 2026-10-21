"""Codex crosscheck/minimax.py outcome (count rule) on the candidate with and without the g4/g5 pair.
Run: PYTHONPATH=. .venv/bin/python verify/lemmas/L3.4-candidate-all-models-reproduce/crosscheck_x8.py"""
from crosscheck import minimax as mm
for ep in (True, False):
    for files, txt in ((4, "W: a2 c2 / B: b7 d7"), (8, "W: a2 c2 / B: b7 d7"), (8, "W: a2 c2 g4 / B: b7 d7 g5")):
        p = mm.parse_position(txt)
        print(files, "files ep", ep, txt, "->", mm.outcome_class(mm.Board(files, 8, False, ep), p))
