"""Supplementary (NOT the decisive check): run Codex's crosscheck/minimax.py on the
8x8 embedding WITH the g4/g5 pair (the worker's A4 crosscheck used the a-d pawns only
on an 8-file board). Count rule only (crosscheck has no other rule)."""
from crosscheck import minimax as mm
for ep in (True, False):
    for txt in ("W: a2 c2 / B: b7 d7", "W: a2 c2 g4 / B: b7 d7 g5"):
        for files in (4, 8):
            if files == 4 and "g4" in txt:
                continue
            p = mm.parse_position(txt)
            print(files, "files ep", ep, txt, "->", mm.outcome_class(mm.Board(files, 8, False, ep), p))
