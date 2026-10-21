"""C5-theory: Elkies (1996, open problems) notes *3 = * + *2. In the textbook-test model, a 6-pawn position
*2 + * should therefore be *3. Check it directly as whole positions (cylcgt sums components).
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONPATH=. .venv/bin/python verify/cylatlas/C5-theory/star3.py
  (and with PYTHONPATH=<scratchpad>/ep-wt:. for the e.p.-aware test)
"""
from cylcgt import cgt, pawns
print("PASSED_RESPECTS_EP =", getattr(pawns, "PASSED_RESPECTS_EP", "absent -> textbook"))
for kind, n, text in [("flat", 8, "W: a2 c2 f2 / B: b7 d7 f4"), ("cyl", 8, "W: a2 c2 f2 / B: b7 d7 f4"),
                      ("flat", 6, "W: a2 c2 f2 / B: b7 d7 f4"), ("flat", 8, "W: f2 / B: f4")]:
    for rule in ("count", "mover", "opponent"):
        pawns.RACE_RULE = rule; pawns._value.cache_clear()
        b = pawns.Board(n, 8, kind == "cyl", True); p = pawns.Pos.parse(text)
        g = pawns.value(b, p)
        print(f"{kind} {n} {text} [{rule}, e.p. on]: {cgt.show(g)}  sum_safe={pawns.sum_safe(b, p)}")
