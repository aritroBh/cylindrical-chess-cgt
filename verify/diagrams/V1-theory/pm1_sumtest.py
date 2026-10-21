"""V1 theory check: does the evidence refute "7.2{a,b,h} = +-1" when e.p. is ON?
With e.p. on the outcome is N, which is also the outcome of +-1, so the outcome alone cannot refute +-1.
Sum tests G + X, with X a single-file pawn group that never makes a passed pawn:
  if G = +-1:  G + (+-1) = 0 -> P ;  G + 1 = 1+-1 -> N ;  G + (-1) = -1+-1 -> N.
Prediction from cylcgt (8-file value + X value); observation from the independent crosscheck
minimax on a 16-file cylinder (a-d keep index, e-h -> 12-15, so h stays adjacent to a; X on file 8).
Also prints the exact canonical form of 7.1{h,a} with numbers written relative to BIG.
Run: cd /Users/aritro/Downloads/Research/Chessendgames && \
     PYTHONPATH=. .venv/bin/python verify/diagrams/V1-theory/pm1_sumtest.py
"""
import sys
sys.setrecursionlimit(1_000_000)
from cylcgt import cgt, pawns
from cylcgt.pawns import Board, Pos
from crosscheck import minimax as mm

FILES = "abcdefghijklmnopqrstuvwxyz"
G72 = "W: a2 b2 h3 / B: a6 b7 h7"
X = {"0": ([], []), "1": ([2, 4], [5]), "-1": ([4], [5, 7]), "+-1": ([2, 3], [5, 6])}
HYP_PM1 = {"0": "N", "1": "N", "-1": "N", "+-1": "P"}


def move16(sqs):
    return [f"{FILES[f if f <= 3 else f + 8]}{r}" for f, r in sqs]


def txt(w, b):
    return f"W: {' '.join(w)} / B: {' '.join(b)}"


for ep in (True, False):
    b8, b16, mb16 = Board(8, 8, True, ep), Board(16, 8, True, ep), mm.Board(16, 8, True, ep)
    pawns.RACE_RULE = "count"; pawns._value.cache_clear()
    gp = Pos.parse(G72)
    g = pawns.value(b8, gp)
    gw, gb = move16(gp.white), move16(gp.black)
    for name, (xw, xb) in X.items():
        xw = [f"i{r}" for r in xw]; xb = [f"i{r}" for r in xb]
        xv = pawns.value(b16, Pos.parse(txt(xw, xb))) if (xw or xb) else cgt.ZERO
        pred = cgt.outcome(cgt.add(g, xv))
        mm._winner.cache_clear()
        obs = mm.outcome_class(mb16, mm.parse_position(txt(gw + xw, gb + xb)))
        print(f"ep={'on ' if ep else 'off'} 7.2abh + ({name:3s}) [X value {cgt.show(xv)}]: cylcgt {pred}  "
              f"crosscheck {obs}   if G were +-1: {HYP_PM1[name]}", flush=True)

# exact form of 7.1{h,a}
pawns.RACE_RULE = "count"; pawns._value.cache_clear()
g = pawns.value(Board(8, 8, True, True), Pos.parse("W: a4 a5 h2 h3 / B: a7 h6"))
print("7.1{h,a}: Left options", [str(x.num) if x.num is not None else cgt.show(x) for x in g.L],
      " Right options", [cgt.show(x) for x in g.R], " mean", cgt.mean(g), " temp", cgt.temperature(g),
      " BIG", pawns.BIG, " cgt.BIG_DISPLAY", cgt.BIG_DISPLAY)
