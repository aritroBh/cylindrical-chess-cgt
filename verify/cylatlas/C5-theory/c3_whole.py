"""C5-theory: the 3-file-cylinder opponent-rule *2 rings as whole-board convention games (lemmas.common.W).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/c3_whole.py
"""
from cylcgt import cgt, pawns
from lemmas import common as C
for text in ("W: a2 b3 / B: a5 c5", "W: a4 b4 / B: a7 c6", "W: a2 b2 / B: a5 c7", "W: a2 b4 / B: b7 c7"):
    for ep in (True, False):
        b = pawns.Board(3, 8, True, ep); p = pawns.Pos.parse(text)
        out = [f"{r}: {cgt.show(C.W(b, p, r))}" for r in ("count", "mover", "opponent")]
        print(f"cyl3 {text} e.p.={'on ' if ep else 'off'}  " + " ; ".join(out))
