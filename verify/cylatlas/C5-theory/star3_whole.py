"""C5-theory: the 6-pawn *2 + * position as a WHOLE-BOARD convention game (lemmas.common.W: no splitting,
first passer terminal, e.p. rights global), and with frozen-trebuchet king moves (WF).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/star3_whole.py
"""
import time
from cylcgt import cgt, pawns
from lemmas import common as C
print("PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent -> textbook"))
for kind, n, text in [("flat", 6, "W: a2 c2 f2 / B: b7 d7 f4"), ("flat", 4, "W: a2 c2 / B: b7 d7")]:
    for ep in (True, False):
        b = pawns.Board(n, 8, kind == "cyl", ep); p = pawns.Pos.parse(text)
        t = time.time()
        g = C.W(b, p, "count"); gf = C.WF(b, p, "count")
        print(f"{kind} {n} {text} e.p.={'on' if ep else 'off'} count: W = {cgt.show(g)} ; WF = {cgt.show(gf)} ({time.time()-t:.0f}s)", flush=True)
