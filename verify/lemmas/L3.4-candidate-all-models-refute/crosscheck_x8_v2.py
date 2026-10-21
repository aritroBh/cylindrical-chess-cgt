"""Supplementary only (NOT the decisive check): Codex's crosscheck/minimax.py on the
candidate, including the 8x8 embedding WITH the g4/g5 pair. Count rule only.

Usage:
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python \
      verify/lemmas/L3.4-candidate-all-models-refute/crosscheck_x8_v2.py
"""
from crosscheck import minimax as mm

for ep in (True, False):
    for txt, files in (("W: a2 c2 / B: b7 d7", 4), ("W: a2 c2 / B: b7 d7", 8),
                       ("W: a2 c2 g4 / B: b7 d7 g5", 8)):
        p = mm.parse_position(txt)
        print(f"{files} files, ep={ep}: {txt} -> {mm.outcome_class(mm.Board(files, 8, False, ep), p)}")
